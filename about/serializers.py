from rest_framework import serializers 
from .models import Page



class PageSerializer(serializers.Serializer): 

    class Meta:
        model = Page
        fields = '__all__'

    def create(self, validated_data): 
        return Page.objects.create(**validated_data)
    

    def update(self, instance, validated_data): 
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.updated = validated_data.get('updated', instance.updated)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.publish = validated_data.get('publish', instance.publish)
        instance.body = validated_data.get('body', instance.body)

        instance.save()
        return instance