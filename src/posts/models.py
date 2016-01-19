from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify
# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename) # this is to specify an upload location i.e. user

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
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


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

# the below will turn our title into a url
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_receiver, sender=Post)