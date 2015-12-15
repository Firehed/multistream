import copy,datetime,re
from twitchapi import TwitchAPI
from site_specific_settings import CLIENT_ID

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader, RequestContext

from models import *

MAX_STREAMS = 8
STREAM = 'stream'
CHAT = 'chat'

class Rect(object):
	def __init__(self, dim, pos):
		self.dim = {'x': dim[0], 'y': dim[1]}
		self.pos = {'x': pos[0], 'y': pos[1]}
	def scale(self, factor):
		obj = self.__class__([self.dim['x'], self.dim['y']], [self.pos['x'], self.pos['y']])
		obj.dim = dict([(k, int(v / factor)) for k,v in obj.dim.items()])
		obj.pos = dict([(k, int(v / factor)) for k,v in obj.pos.items()])
		return obj
	def overlapping(self,other_chat):
		return self.pos == other_chat.pos
	def __repr__(self):
		return '<%s %s %s>' % (self.__class__.__name__, (self.dim['x'], self.dim['y']), (self.pos['x'], self.pos['y']))

class Stream(Rect):
	def __init__(self, dim, pos):
		Rect.__init__(self, dim, pos)
		self.objtype = STREAM

class Chat(Rect):
	def __init__(self, dim, pos):
		Rect.__init__(self, dim, pos)
		self.objtype = CHAT

class Layout(object):
	def __init__(self, objs):
		self.streams = [x for x in objs if x.objtype == STREAM]
		self.chats = [x for x in objs if x.objtype == CHAT]
		if len(self.chats) < len(self.streams) and len(self.chats) > 0:
			self.chats = [copy.deepcopy(self.chats[((c+1) % len(self.chats))-1]) for c in range(len(self.streams))]
		for chat in self.chats:
			chat.overlapped_chats = [c for c in self.chats if c.overlapping(chat)]
	def objects(self):
		return self.streams + self.chats
	def scale(self, factor):
		return Layout([obj.scale(factor) for obj in self.objects()])
	def scale_x(self, width):
		factor = self.max_x() * 1.0 / width
		return self.scale(factor)
	def assign_tags(self, stream_tags):
		if len(stream_tags) > len(self.streams):
			stream_tags = stream_tags[:len(self.streams)]
		else:
			stream_tags = stream_tags + [None]*(len(self.streams)-len(stream_tags))
		if len(self.chats) > 0:
			for stream, chat, stream_tag in zip(self.streams, self.chats, stream_tags):
				stream.tag = stream_tag
				chat.tag = stream_tag
		else:
			for stream, stream_tag in zip(self.streams, stream_tags):
				stream.tag = stream_tag
	def assign_indexes(self):
		if len(self.chats) > 0:
			self.has_chat = True
			for i, stream, chat in zip(range(len(self.streams)), self.streams, self.chats):
				stream.index = i
				chat.index = i
		else:
			self.has_chat = False
			for i, stream in zip(range(len(self.streams)), self.streams):
				stream.index = i
	def max_x(self):
		return max([obj.dim['x'] + obj.pos['x'] for obj in self.objects()])
	def max_y(self):
		return max([obj.dim['y'] + obj.pos['y'] for obj in self.objects()])

def _initialize_layouts(layouts):
	for i,layout in enumerate(layouts):
		layout.scaled_thumb = layout.scale_x(140)
		layout.scaled_tiny = layout.scale_x(50)
		layout.index = i
		layout.assign_indexes()
	d_layout_groups = {}
	for layout in layouts:
		num_streams = len(layout.streams)
		if num_streams not in d_layout_groups:
			d_layout_groups[num_streams] = []
		d_layout_groups[num_streams].append(layout)
	groups = []
	for num_streams in range(min(d_layout_groups.keys()), max(d_layout_groups.keys()) + 1):
		groups.append(d_layout_groups[num_streams])
	return groups
		

STREAM_LAYOUTS = [
	# Object sizes are in percent.
	# 1 stream
	Layout([
		Stream((75,100),(0,0)),
		Chat((25,100),(75,0)),
	]),
	Layout([
		Stream((100,60),(0,0)),
		Chat((100,40),(0,60)),
	]),
	Layout([
		Stream((100,100),(0,0)),
	]),
	# 2 streams
	Layout([
		Stream((70,50),(0,0)), Chat((30,100),(70,0)),
		Stream((70,50),(0,50)), 
	]),
	Layout([
		Stream((50,58),(0,0)), Stream((50,58),(50,0)),
		Chat((50,42),(0,58)), Chat((50,42),(50,58)),
	]),
	Layout([
		Stream((100,50),(0,0)),
		Stream((100,50),(0,50)),
	]),
	# 3 streams
	Layout([
		Stream((75,65),(0,0)), Chat((25,100),(75,0)),
		Stream((37,35),(0,65)), Stream((38, 35),(37,65)),
	]),
	Layout([
		Stream((50, 50),(0,0)), Stream((50,50),(50,0)), 
		Stream((50, 50),(0,50)), Chat((50, 50),(50,50)),
	]),
	Layout([
		Stream((100,60),(0,0)),
		Stream((50,40),(0,60)), Stream((50, 40),(50,60)),
	]),
	# 4 streams
	Layout([
		Stream((75,65),(0,0)), Chat((25,65),(75,0)),
		Stream((33,35),(0,65)), Stream((34,35),(33,65)), Stream((33,35),(67,65)),
	]),
	Layout([
		Stream((37,50),(0,0)), Stream((38,50),(37,0)), Chat((25,100),(75,0)),
		Stream((37,50),(0,50)), Stream((38,50),(37,50)),
	]),
	Layout([
		Stream((50,50),(0,0)), Stream((50,50),(50,0)),
		Stream((50,50),(0,50)), Stream((50,50),(50,50)),
	]),
	# 5 Streams
	Layout([
		Stream((37,60),(0,0)), Stream((38,60),(37,0)), Chat((25,60),(75,0)),
		Stream((33,40),(0,60)), Stream((34,40),(33,60)), Stream((33,40),(67,60)),
	]),
	Layout([
		Stream((33,50),(0,0)), Stream((34,50),(33,0)), Stream((33,50),(67,0)),
		Stream((33,50),(0,50)), Chat((34,50),(33,50)), Stream((33,50),(67,50)),
	]),
	Layout([
		Stream((50,60),(0,0)), Stream((50,60),(50,0)), 
		Stream((33,40),(0,60)), Stream((34,40),(33,60)), Stream((33,40),(67,60)),
	]),
	# 6 Streams
	Layout([
		Stream((33,33),(0,0)), Stream((34,33),(33,0)), Chat((33,100),(67,0)),
		Stream((33,34),(0,33)), Stream((34,34),(33,33)), 
		Stream((33,33),(0,67)), Stream((34,33),(33,67)),
	]),
	Layout([
		Stream((33,50),(0,0)), Stream((34,50),(33,0)), Stream((33,50),(67,0)),
		Stream((33,50),(0,50)), Stream((34,50),(33,50)), Stream((33,50),(67,50)),
	]),
	# 7 Streams!
	Layout([
		Stream((25,50),(0,0)), Stream((25,50),(25,0)), Stream((25,50),(50,0)), Stream((25,50),(75,0)),
		Stream((25,50),(0,50)), Stream((25,50),(25,50)), Stream((25,50),(50,50)), Chat((25,50),(75,50)),
	]),
	Layout([
		Stream((50,50),(25,0)), Chat((50,50),(25,50)),
		Stream((25,33),(0,0)), Stream((25,34),(0,33)), Stream((25,33),(0,67)),
		Stream((25,33),(75,0)), Stream((25,34),(75,33)), Stream((25,33),(75,67)),
	]),
	Layout([
		Stream((33,60),(0,0)), Stream((34,60),(33,0)), Stream((33,60),(67,0)),
		Stream((25,40),(0,60)), Stream((25,40),(25,60)), Stream((25,40),(50,60)), Stream((25,40),(75,60)),
	]),
	# 8 Streams !!
	Layout([
		Stream((33,33),(0,0)), Stream((34,33),(33,0)), Stream((33,33),(67,0)),
		Stream((33,34),(0,33)),	Stream((34,34),(33,33)), Stream((33,34),(67,33)),
		Stream((33,33),(0,67)), Stream((34,33),(33,67)), Chat((33,33),(67,67)),
	]),
	Layout([
		Stream((25,50),(0,0)), Stream((25,50),(25,0)), Stream((25,50),(50,0)), Stream((25,50),(75,0)),
		Stream((25,50),(0,50)), Stream((25,50),(25,50)), Stream((25,50),(50,50)), Stream((25,50),(75,50)),
	]),

]
LAYOUT_GROUPS = _initialize_layouts(STREAM_LAYOUTS)



def index(request, streams_url=''):
	
	has_blanks = False
	old_url_format = False
	
	if streams_url != '':
		streams = streams_from_url(streams_url)
				
	else:
		old_url_format = True
		streams = []
		has_blanks = False
		for x in range(MAX_STREAMS):
			stag = request.GET.get('s%d' % (x,), None)
			if stag is not None:
				stag = stag.strip()
				if stag == '':
					has_blanks = True
				else:
					streams.append(stag)
					
	if len(streams)!=len(set(streams)):
		has_duplicates = True
	else:
		has_duplicates = False

	if (streams and old_url_format) or has_duplicates:
		return HttpResponseRedirect('/' + settings.URL_INFIX + 'edit/%s' % ('/'.join(remove_duplicates(streams)).lower()))

	#since we're using 'pop' in the template
	if streams:
		streams.reverse()
		
	tags = [x for x in Tag.objects.filter(active=True).order_by('index') if x.current()]
	channels = [x for x in Channel.objects.filter(active=True) if x.current()]
	
	c = RequestContext(request, {
		'num_streams': range(MAX_STREAMS),
		'layout_groups': LAYOUT_GROUPS,
		'channels': channels,
		'tags': tags,
		'streams': streams,
		'client_id': CLIENT_ID,
	})
	t = loader.get_template('index.html')
	return HttpResponse(t.render(c))



def view_streams(request, streams_url=''):
	
	has_blanks = False
	old_url_format = False
	
	if streams_url != '':
		streams = streams_from_url(streams_url)
		layout_index = layout_from_url(streams_url)
		if layout_index == -1:
			layout_index = default_layout(len(streams))
			has_blanks = True
				
	else:
		old_url_format=True
		streams = []
		layout_index = int(request.GET.get('layout', 0))
		
		for x in range(MAX_STREAMS):
			stag = request.GET.get('s%d' % (x,), None)
			if stag is not None:
				stag = stag.strip()
				if stag == '':
					has_blanks = True
				else:
					streams.append(stag)
					
		if layout_index == '':
			layout_index = default_layout(len(streams))
			
	if len(streams)!=len(set(streams)):
		has_duplicates = True
	else:
		has_duplicates = False

	if not streams:
		return HttpResponseRedirect('/' + settings.URL_INFIX)
	if has_blanks or old_url_format or has_duplicates:
		return HttpResponseRedirect('/' + settings.URL_INFIX + '%s/layout%s/' % ('/'.join(remove_duplicates(streams)).lower(), layout_index))
		
	if len(streams) > MAX_STREAMS:
		num_streams = MAX_STREAMS
	else:
		num_streams = len(streams)

	layout_group = copy.deepcopy(LAYOUT_GROUPS[num_streams - 1])
	for layout in layout_group:
		layout.assign_tags(streams)

	c = RequestContext(request, {
		'layout_groups': LAYOUT_GROUPS,
		'layout_group': layout_group,
		'use_live_embeds' : settings.USE_LIVE_EMBEDS,
		'use_flash_player' : settings.USE_FLASH_PLAYER,
		'edit_url': '/' + settings.URL_INFIX + 'edit/%s/' % ('/'.join(streams).lower()),
		'client_id': CLIENT_ID,
	})
	t = loader.get_template('view.html')
	return HttpResponse(t.render(c))


def view_tag(request, tag = ''):
	tag = tag.rstrip('/').replace('-', ' ').lower()
	tags = Tag.objects.filter(active=True,name__iexact=tag)
	
	if len(tags) == 1 and tags[0].current():
		channels = [x.name for x in tags[0].channels.filter(active=True,live=True)][:MAX_STREAMS]
		
		if len(channels):
			return HttpResponseRedirect('/' + settings.URL_INFIX + '%s/layout%s/' % ('/'.join(channels).lower(), default_layout(len(channels))))
		else:
			return HttpResponseRedirect('/' + settings.URL_INFIX + '#featured/' + tag.replace(' ', '-') + '/')
	else:
		return HttpResponseNotFound('"%s": Tag Not Found.' % tag)


#Run this via a cron job. i.e., curl http://localhost/multistream/ms-update_streams/
def update_streams(request):

	twitch = TwitchAPI()
	channels = [x for x in Channel.objects.filter(active=True) if x.current()]
	channel_list = [channel.name for channel in channels]

	live_streams = twitch.get_streams(channel_list)

	if type(live_streams).__name__ == 'dict':
		for channel in channels:
			if channel.name in live_streams.keys():
				channel.live = True
				channel.preview = live_streams[channel.name]["preview"]["medium"]
				if live_streams[channel.name]["game"]:
					channel.game = live_streams[channel.name]["game"]
				else:
					channel.game = ""
			else:
				channel.live = False

			channel.save()

		return HttpResponse("\n".join(live_streams.keys()))
	else:
		return HttpResponse("twitchapi not responding")

def update_channels(request):
	twitch = TwitchAPI()
	channels = [x for x in Channel.objects.filter(active=True) if x.current()]
	
	for channel in channels:
		t_channel = twitch.get_channel(channel.name)
		if t_channel:
			if t_channel["logo"]:
				channel.logo = t_channel["logo"]
			else:
				channel.logo = "";
			channel.save()

	return HttpResponse("\n".join([c.name for c in channels]))

def live_now(request):
	channel_q = request.GET.get('channel',0)
	if not channel_q:
		channels = [x for x in Channel.objects.filter(active=True,live=True) if x.current()]
		kbmod = Channel.objects.filter(name__iexact='kbmod')
		c = RequestContext(request, {
			'channels': channels,
			'kbmod' : kbmod[0],
		})
	else:
		try:
			channel = Channel.objects.get(name=channel_q)
		except:
			return HttpResponseNotFound("'" + channel_q + "' channel not found")

		c = RequestContext(request, {
			'channel': channel,
		})
		
	t = loader.get_template('live_now.html')
	r = HttpResponse(t.render(c))
	r['Access-Control-Allow-Origin'] = '*'
	return r
	

def get_object(request,obj_type=None,obj_tag=None,obj_index=-1):
	
	if (obj_type == 'stream' or obj_type == 'chat' or obj_type == 'both') and obj_index >= 0 and obj_tag != '':
		t = loader.get_template('object.html')
		
		c = RequestContext(request, {
			'obj': {
				'objtype' : obj_type,
				'index' : obj_index,
				'tag' : obj_tag,
			},
			'use_live_embeds' : settings.USE_LIVE_EMBEDS,
			'use_flash_player' : settings.USE_FLASH_PLAYER,
		})
		return HttpResponse(t.render(c))
		
	else:
		return HttpResponse("Error: Object type, index, or tag missing or invalid.")



#utility junk

def streams_from_url(streams_url):
	return [x for x in streams_url.split("/")[:MAX_STREAMS] if x != '' and x[:6] != 'layout']
	
def layout_from_url(streams_url):
	layout_pattern = re.compile(r"layout=?([0-9][0-9]?)", re.IGNORECASE)
	layout_matches = layout_pattern.search(streams_url)
	if layout_matches:
		layout_num = layout_matches.group(1)
	else:
		layout_num = -1
		
	return int(layout_num)

def default_layout(stream_count=1):
	return LAYOUT_GROUPS[stream_count - 1][0].index


def remove_duplicates(seq):
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if not (x in seen or seen_add(x))]
