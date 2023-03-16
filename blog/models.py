from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    draft = models.BooleanField(default=False)
    content = RichTextField(config_name='default')
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True)
    image = models.ImageField(upload_to=post_upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
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
        return Comment.objects.filter(content_type=content_type, object_id=self.id, parent=None)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    
    
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

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None

class Comment(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    

    objects = CommentManager()

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return f'Comment by {self.owner.username} on {self.content_object}'

    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('comment_delete', kwargs={'pk': self.pk})

    def children(self):
        return self.replies.all()

    @property
    def is_parent(self):
        return not self.parent