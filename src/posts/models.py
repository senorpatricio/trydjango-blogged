from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename) # this is to specify an upload location i.e. user

class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    content = models.TextField()
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    #there are many types of fields. reference on docs.djangoproject.com

    def __unicode__(self):
    	return self.title

    def __str__(self):
    	return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={"id": self.id})
        # return "/posts/%s/" %(self.id)

    # class Meta:
    #     ordering = ["-timestamp", "-updated"]
    # this will order it by newest first