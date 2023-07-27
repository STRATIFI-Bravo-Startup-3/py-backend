from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User as user
User = get_user_model()


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super().filter(draft=False).filter(publish__lte=timezone.now())


def post_upload_location(instance, filename):
    try:
        new_id = BlogPost.objects.order_by("id").last().id + 1
    except AttributeError:
        new_id = 1
    return "%s/%s" % (new_id, filename)


class BlogPost(models.Model):
    owner = models.ForeignKey(user, on_delete=models.CASCADE, related_name="posts", null=False)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=post_upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    slug = models.SlugField(unique=True, blank=True,)
    
    draft = models.BooleanField(default=False)
    content = RichTextField(config_name='default')
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True)
    
    height_field = models.IntegerField(default=0, blank=True)
    width_field = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_api_url(self):
        return reverse("posts-api:detail", kwargs={"slug": self.slug})

    def get_read_time(self):
        from html import unescape
        from django.utils.html import strip_tags

        string = self.title + unescape(strip_tags(self.content))
        total_words = len((string).split())

        read_time = round(total_words / 200)
        return read_time

    read_time = get_read_time
    
    @property
    def comments(self):
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=content_type, object_id=self.id)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    
    def __str__(self):
        return self.title

    
    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = BlogPost.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        
pre_save.connect(pre_save_post_receiver, sender=BlogPost)


# class CommentManager(models.Manager):
#     def all(self):
#         return super(CommentManager, self).filter(parent=None)

#     def filter_by_instance(self, instance):
#         return super(CommentManager, self).filter(content_object=instance).filter(parent=None)

#     def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
#         try:
#             SomeModel = model_type.model_class()
#         except AttributeError:
#             return None

#         try:
#             obj = SomeModel.objects.get(slug=slug)
#         except SomeModel.DoesNotExist:
#             return None

#         instance = self.model()
#         instance.content = content
#         instance.user = user
#         instance.content_object = obj
#         if parent_obj:
#             instance.parent = parent_obj
#         instance.save()
#         return instance


class Comment(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    replies = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    # objects = CommentManager()

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return f"Comment by {self.owner.username} on {self.post.title}"

    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('comment_delete', kwargs={'pk': self.pk})

    def children(self):
        return self.replies.all()
    
    
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Reply by {self.owner.username} on {self.comment.post.title}"

