from rest_framework import serializers 
from .models import About, Vision, Mission, Goal, Service



# Serializers for all the models
class AboutSerializer(serializers.ModelSerializer):

    class Meta:
        model = About
        fields = '__all__'

class VisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vision
        fields = '__all__'

class MissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mission
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'

'''class PageSerializer(serializers.Serializer): 

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
        return instance'''
    