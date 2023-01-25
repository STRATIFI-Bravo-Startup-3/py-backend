from django.db import models
from users.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    return "%s/%s" %(new_id, filename)


# class Category(models.Model):
#     name = models.CharField(max_length=100, blank=False, default='')
#     owner = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
#     posts = models.ManyToManyField('BlogPost', related_name='categories', blank=True)

#     class Meta:
#         verbose_name_plural = 'categories'

class BlogPost(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE ,related_name = "posts")
    title = models.CharField(max_length=35, blank=True)
    slug = models.SlugField(unique=True, blank=True)  
    draft = models.BooleanField(default=False)
    content = RichTextField(config_name='default') #a library that allows you to format your blog, text and images
    created_at = models.DateTimeField(blank=True,auto_now_add=True)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True)
    
    # Category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to="upload_location", 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0,blank=True,)
    width_field = models.IntegerField(default=0,blank=True,)
    

    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('blog-post-detail', kwargs = {'slug': self.slug})
    
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
        instance = self
        qs = Comments.objects.filter_by_instance(instance)
        return qs

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

    
#Comments
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
    
    
class Comments(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content     = models.TextField()
    parent      = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    

    objects = CommentManager()

    def __unicode__(self):  
        return str(self.user.username)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})
        
    def children(self): #replies
        return Comments.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


    
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.post.title)

