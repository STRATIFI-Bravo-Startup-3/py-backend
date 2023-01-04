from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse




class Page(models.Model): 
    title = models.CharField(max_length=120) 
    slug = models.SlugField()
    #updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    #timestamp = models.DateTimeField(default=True, auto_now=False, auto_now_add=True)
    draft = models.BooleanField(default=False)
    #publish = models.DateField(auto_now=False, auto_now_add=True)
    body = models.TextField()
    1
    def __str__(self): 
        return self.title
    
    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)