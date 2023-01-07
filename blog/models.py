from django.db import models
from users.models import User
# Create your models here.

class BlogPost(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE ,related_name = "posts")
    title = models.CharField(max_length=35, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(blank=True,auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return 'Comment by {}'.format(self.user.username)


class Comments(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name = "comments")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.user.username)

