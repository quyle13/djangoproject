from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=128,unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField()
	def __unicode__(self):
		return self.name
	def save(self,*args, **kwargs):
		self.slug = slugify(self.name)
		super(Category,self).save(*args,**kwargs)

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	#URLField like CharField but designed for storing URL
	url = models.URLField()
	#IntegerField for storing Integerx`
	views = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title
class UserProfile(models.Model):
	#This line is compulsory. Link UsreProfile to a User model instance
	user = models.OneToOneField(User)

	#add some fields
	website = models.URLField(blank=True)
	#upload to attribute specifies the location to store the image
	picture = models.ImageField(upload_to="profile_images",blank=True)

	def __unicode__(self):
		return self.user.username



