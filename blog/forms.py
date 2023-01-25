from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from pagedown.widgets import PagedownWidget
from .models import BlogPost

#Post
class BlogPostForm(forms.ModelForm):
    content = RichTextUploadingField()
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]

#Comment
class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)



