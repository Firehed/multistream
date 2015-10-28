import json, urllib2
from site_specific_settings import CLIENT_ID

class TwitchAPI:
	def __init__(self):
		self.client_id = CLIENT_ID #Add your Twitch API client ID here
		self.api_url_base = 'https://api.twitch.tv/kraken/'
		self.url_params = ''
		self.api_headers = {
			'Accept': 'application/vnd.twitchtv.v3+json',
			'Client-ID': self.client_id,
		}
		self.DEBUG = True

	def request(self,command,params=False):

		full_url = self.api_url_base + command
		if params:
			for key in params.keys():
				if "?" in full_url:
					full_url += "&"
				else:
					full_url += "?"
				if type(params[key]).__name__ == 'list':
					full_url += key + "=" + ",".join(params[key])
				else:
					full_url += key + "=" + params[key]

		if self.DEBUG:
				print full_url
					
		try:
			req = urllib2.Request(url=full_url,headers=self.api_headers)
			response = urllib2.urlopen(req)
			jsontext = response.read()
		except:
			if self.DEBUG:
				print 'twitchapi not responding'
			return False
		
		jsontext = jsontext.replace('":,"','":"","')
		jsontext = jsontext.replace("\\'","'")
		twitch_json = json.loads(jsontext)

		if command == "streams":
			result = twitch_json.get('streams')
			if result:
				result_dict = { r["channel"]["name"]: r for r in result }
				if self.DEBUG:
					print '\n'.join(result_dict.keys())
				return result_dict
			else:
				if self.DEBUG:
					print 'no streams live'
				return {}
		else:
			return twitch_json
	
		


	def get_streams(self,channels):

		if type(channels).__name__ == 'list':
			return self.request("streams",{"channel": channels})
		else:
			return self.request("streams",{"channel": [channels]})


	def get_channel(self,channel):
		return self.request("channels/" + channel)
		
