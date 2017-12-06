from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify #signal that gets triggered before or after the object is saved
from django.contrib.auth.models import User #a model that django provides

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(User, default=1) #default user is user #1 
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(null=True, blank=True, upload_to="post_images")
	slug = models.SlugField(unique=True)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse ("post:detail", kwargs={"post_slug":self.slug})

	class Meta:
		ordering = ['-title']

def create_slug(instance, new_slug = None): #default parameter. If you don't give it a value it will be none
	slug_value = slugify(instance.title)
	if new_slug is not None:
		slug_value = new_slug

	query = Post.objects.filter(slug=slug_value)
	if query.exists():
		slug_value = "%s-%s"%(slug_value, query.last().id)
		return create_slug(instance, new_slug=slug_value)
	return slug_value



def pre_save_post_function(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)	

pre_save.connect(pre_save_post_function, sender=Post) #when presave gets tirggerd by post model, call this function

class Like(models.Model):
	user=models.ForeignKey(User)
	post = models.ForeignKey(Post)
	timestamp = models.DateTimeField(auto_now_add=True)