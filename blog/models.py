from django.db import models
from users.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.conf import settings
# Create your models here.

# class Categories(models.Model):
#     Category = models.TextField()

class BlogPost(models.Model):
    owner=models.OneToOneField(User, on_delete=models.CASCADE ,related_name = "posts")
    title = models.CharField(max_length=35, blank=True)
    body = RichTextField(config_name='default') #a library that allows you to format your blog, text and images
    created_at = models.DateTimeField(blank=True,auto_now_add=True)
    #slug = models.SlugField(unique=True)  
    Category = models.TextField()

    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-post-detail', kwargs = {'slug': self.slug})

class Comments(models.Model):
    owner=models.OneToOneField(User, on_delete=models.CASCADE, related_name = "comments")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.post.title)

