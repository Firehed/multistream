import datetime
from django.db import models

class Channel(models.Model):
	name = models.CharField(max_length=60)
	active = models.BooleanField(default=False)
	tags = models.ManyToManyField('Tag',related_name='channels',blank=True)
	logo = models.URLField(blank=True)
	preview = models.URLField(blank=True)
	game = models.CharField(max_length=60,blank=True)
	live = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.name

	def image(self):
		if self.live:
			return self.preview
		else:
			return self.logo

	def current(self):
		if len(self.tags.exclude(firstDate__gt=datetime.date.today()).exclude(lastDate__lt=datetime.date.today())) > 0:
			return True
		else:
			return False

		
class Tag(models.Model):
	name = models.CharField(max_length=30)
	active = models.BooleanField(default=False)
	index = models.IntegerField(null=True)
	firstDate = models.DateField(null=True)
	lastDate = models.DateField(null=True)

	def __unicode__(self):
		return self.name

	def slug(self):
		return self.name.replace(' ','-').lower()

	def current(self):
		c = True
		if self.firstDate:
			if self.firstDate > datetime.date.today():
				c = False

		if self.lastDate:
			if self.lastDate < datetime.date.today():
				c = False
				
		return c

