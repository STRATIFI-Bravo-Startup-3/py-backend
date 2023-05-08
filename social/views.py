from django.http import JsonResponse
import requests
from django.conf import settings
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .serializers import (TwitterHandleSerializer, 
TwitterFollowerCountSerializer, YouTubeHandleSerializer, YouTubeConnectSerializer, 
TikTokHandleSerializer, TikTokConnectionSerializer, 
InstagramHandleSerializer, InstagramConnectionSerializer,
FacebookPageSerializer, FacebookFollowerSerializer,
CustomURLSerializer, CustomSocialHandleSerializer, )
import facebook
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from tiktokapi import TikTokApi
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import TwitterHandleSerializer, TwitterFollowerCountSerializer
import tweepy

from .models import (SocialMediaHandle, CustomURL, SocialMediaPlatform,)



def get_social_handles(request):
    social_handles = SocialMediaHandle.objects.filter(user=request.user)
    data = {}
    for social_handle in social_handles:
        data[social_handle.platform.name] = {
            'followers': social_handle.followers,
            'handle': social_handle.handle
        }
    return JsonResponse(data)



#Facebook Page
class FacebookConnectionView(APIView):
    def post(self, request):
        # Extract the relevant data from the request data
        handle = request.data.get('handle')
        followers = request.data.get('followers')
        custom_url = request.data.get('custom_url')
        facebook_page_id = request.data.get('facebook_page_id')
        custom_followers = request.data.get('custom_followers')
        last_updated = request.data.get('last_updated')

        # Serialize the data
        data = {
            'handle': handle,
            'followers': followers,
            'custom_url': custom_url,
            'facebook_page_id': facebook_page_id,
            'custom_followers': custom_followers,
            'last_updated': last_updated
        }
        serializer = CustomSocialHandleSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            # Call the create method of the serializer to process the Facebook connection
            social_handle = serializer.create(serializer.validated_data)
            return Response({'message': 'Facebook connection processed successfully', 'social_handle_id': social_handle.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve all SocialMediaHandle instances with Facebook platform
        social_handles = SocialMediaHandle.objects.filter(platform='facebook')

        # Serialize the social handles
        serializer = CustomSocialHandleSerializer(social_handles, many=True)

        # Return the serialized social handles as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, social_handle_id):
        try:
            # Retrieve the SocialMediaHandle instance with the given ID
            social_handle = SocialMediaHandle.objects.get(id=social_handle_id)
        except SocialMediaHandle.DoesNotExist:
            # Return a response with 404 (Not Found) if the social handle does not exist
            return Response({'error': 'Social handle not found'}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the request data with the CustomSocialHandleSerializer
        serializer = CustomSocialHandleSerializer(social_handle, data=request.data)

        if serializer.is_valid():
            # Update the SocialMediaHandle instance with the deserialized data
            serializer.save()

            # Return a response with the updated social handle data and 200 (OK) status
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return a response with the serializer errors and 400 (Bad Request) status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, social_handle_id):
        try:
            # Retrieve the SocialMediaHandle instance with the given ID
            social_handle = SocialMediaHandle.objects.get(id=social_handle_id)
        except SocialMediaHandle.DoesNotExist:
            # Return a response with 404 (Not Found) if the social handle does not exist
            return Response({'error': 'Social handle not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the SocialMediaHandle instance
        social_handle.delete()

        # Return a response with 204 (No Content) status indicating successful deletion
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacebookPageList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        facebook_pages = SocialMediaHandle.objects.filter(platform='Facebook', user=request.user)
        serializer = FacebookPageSerializer(facebook_pages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacebookPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(platform='Facebook', user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacebookPageDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return get_object_or_404(SocialMediaHandle, pk=pk, platform='Facebook', user=self.request.user)

    def get(self, request, pk):
        facebook_page = self.get_object(pk)
        serializer = FacebookPageSerializer(facebook_page)
        return Response(serializer.data)

    def put(self, request, pk):
        facebook_page = self.get_object(pk)
        serializer = FacebookPageSerializer(facebook_page, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facebook_page = self.get_object(pk)
        facebook_page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacebookFollower(APIView):
    def post(self, request):
        serializer = FacebookFollowerSerializer(data=request.data)
        if serializer.is_valid():
            # Logic to process Facebook follower count
            # You can implement your own logic here
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Instagram
class InstagramHandleList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        instagram_handles = SocialMediaHandle.objects.filter(platform='Instagram', user=request.user)
        serializer = InstagramHandleSerializer(instagram_handles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstagramHandleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(platform='Instagram', user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstagramHandleDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return get_object_or_404(SocialMediaHandle, pk=pk, platform='Instagram', user=self.request.user)

    def get(self, request, pk):
        instagram_handle = self.get_object(pk)
        serializer = InstagramHandleSerializer(instagram_handle)
        return Response(serializer.data)

    def put(self, request, pk):
        instagram_handle = self.get_object(pk)
        serializer = InstagramHandleSerializer(instagram_handle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instagram_handle = self.get_object(pk)
        instagram_handle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InstagramConnection(APIView):
    def post(self, request):
        # Retrieve the access token from the request data
        access_token = request.data.get('access_token')

        # Validate the access token (e.g., check if it's not empty)
        if not access_token:
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Add your logic to establish the Instagram connection using the access token
        # For example, you can make API requests to Instagram API using a library like requests
        # or use a third-party library that provides an interface to the Instagram API

        # Once the Instagram connection is established, you can create/update the SocialMediaHandle instance
        social_handle = SocialMediaHandle(user=request.user, platform='Instagram', access_token=access_token)
        social_handle.save()

        # Return a response with 201 (Created) status indicating successful connection
        return Response({'message': 'Instagram connection established'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        # Retrieve the access token from the request query parameters
        access_token = request.query_params.get('access_token')

        # Validate the access token (e.g., check if it's not empty)
        if not access_token:
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Add your logic to retrieve the Instagram connection using the access token
        # For example, you can query the SocialMediaHandle model to find the matching connection
        try:
            social_handle = SocialMediaHandle.objects.get(platform='Instagram', access_token=access_token)
        except SocialMediaHandle.DoesNotExist:
            return Response({'error': 'Instagram connection not found'}, status=status.HTTP_404_NOT_FOUND)

        # You can now access the retrieved SocialMediaHandle instance and return the relevant data in the response
        # For example, you can return the user, platform, and other relevant information
        response_data = {
            'user': social_handle.user.username,
            'platform': social_handle.platform,
            # Add other relevant fields here
        }

        # Return the response data with a 200 (OK) status
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request):
        # Retrieve the access token and other update data from the request data
        access_token = request.data.get('access_token')
        # Retrieve other fields you want to update, e.g., followers count
        followers = request.data.get('followers')

        # Validate the access token (e.g., check if it's not empty)
        if not access_token:
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Add your logic to retrieve and update the Instagram connection using the access token
        # For example, you can query the SocialMediaHandle model to find the matching connection
        try:
            social_handle = SocialMediaHandle.objects.get(platform='Instagram', access_token=access_token)
        except SocialMediaHandle.DoesNotExist:
            return Response({'error': 'Instagram connection not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the relevant fields of the SocialMediaHandle instance with the provided data
        # For example, you can update the followers count
        social_handle.followers = followers
        # Update other relevant fields here

        # Save the updated SocialMediaHandle instance
        social_handle.save()

        # You can now return a success response indicating that the Instagram connection was updated
        response_data = {
            'message': 'Instagram connection updated successfully',
            # Add other relevant fields in the response
        }

        # Return the response data with a 200 (OK) status
        return Response(response_data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        # Retrieve the access token from the request data
        access_token = request.data.get('access_token')

        # Validate the access token (e.g., check if it's not empty)
        if not access_token:
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Add your logic to delete the Instagram connection using the access token
        # For example, you can query the SocialMediaHandle model to find the matching connection
        try:
            social_handle = SocialMediaHandle.objects.get(platform='Instagram', access_token=access_token)
        except SocialMediaHandle.DoesNotExist:
            return Response({'error': 'Instagram connection not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the SocialMediaHandle instance
        social_handle.delete()

        # You can now return a success response indicating that the Instagram connection was deleted
        response_data = {
            'message': 'Instagram connection deleted successfully',
            # Add other relevant fields in the response
        }

        # Return the response data with a 204 (No Content) status
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    

#Twitter API

class TwitterConnectionView(APIView):
    def post(self, request):
        serializer = TwitterFollowerCountSerializer(data=request.data)
        if serializer.is_valid():
            follower_count = serializer.validated_data.get('follower_count')

            # TODO: Add your logic to process the Twitter connection using the follower count
            # For example, you can use the follower count to authenticate with Twitter and
            # perform actions on behalf of the user

            # Once the Twitter connection is processed, you can return a success response
            # indicating that the connection was successful
            response_data = {
                'message': 'Twitter connection processed successfully',
                # Add other relevant fields in the response
            }

            # Return the response data with a 200 (OK) status
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user # Assuming user is authenticated and available in request
        try:
            # Retrieve the Twitter handle associated with the user
            social_media_handle = SocialMediaHandle.objects.get(user=user, platform='twitter')
        except SocialMediaHandle.DoesNotExist:
            # Return an error response if Twitter handle not found
            return Response({'message': 'Twitter connection not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the Twitter handle data and return in response
        serializer = TwitterHandleSerializer(social_media_handle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user # Assuming user is authenticated and available in request
        try:
            # Retrieve the Twitter handle associated with the user
            social_media_handle = SocialMediaHandle.objects.get(user=user, platform='twitter')
        except SocialMediaHandle.DoesNotExist:
            # Return an error response if Twitter handle not found
            return Response({'message': 'Twitter connection not found'}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the request data
        serializer = TwitterHandleSerializer(social_media_handle, data=request.data)
        if serializer.is_valid():
            # Update the Twitter handle data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user # Assuming user is authenticated and available in request
        try:
            # Retrieve the Twitter handle associated with the user
            social_media_handle = SocialMediaHandle.objects.get(user=user, platform='twitter')
        except SocialMediaHandle.DoesNotExist:
            # Return an error response if Twitter handle not found
            return Response({'message': 'Twitter connection not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the Twitter handle
        social_media_handle.delete()
        return Response({'message': 'Twitter connection deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class TwitterHandleList(APIView):
    def get(self, request):
        handles = SocialMediaHandle.objects.filter(platform='twitter')
        serializer = TwitterHandleSerializer(handles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TwitterHandleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(platform='twitter')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TwitterHandleDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(SocialMediaHandle, pk=pk, platform='twitter')

    def get(self, request, pk):
        handle = self.get_object(pk)
        serializer = TwitterHandleSerializer(handle)
        return Response(serializer.data)

    def put(self, request, pk):
        handle = self.get_object(pk)
        serializer = TwitterHandleSerializer(handle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        handle = self.get_object(pk)
        handle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TwitterFollowerCount(APIView):
    def post(self, request):
        serializer = TwitterFollowerCountSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the Twitter username from the request data
            username = serializer.validated_data.get('username')
            
            # Implement your logic to fetch Twitter follower count using the username
            # You can use any third-party library or API to interact with Twitter API
            # For example, you can use tweepy library to fetch the follower count
            
            # Fetch the follower count
            follower_count = 1000  # Replace with your actual logic to fetch follower count
            
            # Return the follower count as response data
            return Response({'follower_count': follower_count}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Youtube
class YouTubeConnectionView(APIView):
    def post(self, request):
        serializer = YouTubeConnectSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the YouTube channel ID or username from the request data
            channel_id = serializer.validated_data.get('channel_id')
            username = serializer.validated_data.get('username')
            
            # Implement your logic to process YouTube connection
            # You can use any third-party library or API to interact with YouTube API
            # For example, you can use google-auth and google-api-python-client libraries to authenticate and interact with YouTube API
            
            # Process the YouTube connection
            # Replace the following code with your actual logic to process the YouTube connection
            if channel_id:
                # Process the connection using channel ID
                # ...
                return Response({'message': 'YouTube connection using channel ID processed successfully.'}, status=status.HTTP_200_OK)
            elif username:
                # Process the connection using username
                # ...
                return Response({'message': 'YouTube connection using username processed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No channel ID or username provided.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Logic to retrieve YouTube connections
        # You can implement your own logic here
        connections = SocialMediaHandle.objects.filter(platform='youtube')
        serializer = YouTubeHandleSerializer(connections, many=True)
        # Build the YouTube API service
        youtube = build('youtube', 'v3', developerKey='YOUR_API_KEY')  # Replace with your API key
        
        # Define the request to retrieve video statistics
        request = youtube.videos().list(
            part='statistics',
            id='VIDEO_ID'  # Replace with the actual video ID of the YouTube connection
        )
        
        # Execute the request and retrieve the video statistics
        response = request.execute()
        
        # Extract the views from the response
        views = response['items'][0]['statistics']['viewCount']
        
        # Return the retrieved views as a response
        return Response({'views': views}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Logic to update YouTube connection
        # You can implement your own logic here
        connection = SocialMediaHandle.objects.get(pk=pk)
        serializer = YouTubeHandleSerializer(connection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Logic to delete YouTube connection
        # You can implement your own logic here
        connection = SocialMediaHandle.objects.get(pk=pk)
        connection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class YouTubeHandleList(APIView):
    def get(self, request):
        handles = SocialMediaHandle.objects.filter(platform='youtube')
        serializer = YouTubeHandleSerializer(handles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = YouTubeHandleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(platform='youtube')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YouTubeHandleDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(SocialMediaHandle, pk=pk, platform='youtube')

    def get(self, request, pk):
        handle = self.get_object(pk)
        serializer = YouTubeHandleSerializer(handle)
        return Response(serializer.data)

    def put(self, request, pk):
        handle = self.get_object(pk)
        serializer = YouTubeHandleSerializer(handle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        handle = self.get_object(pk)
        handle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Tiktok
class TikTokConnectionView(APIView):
    def post(self, request):
        serializer = TikTokConnectionSerializer(data=request.data)
        if serializer.is_valid():
            # Logic to process TikTok connection
            # You can implement your own logic here
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Logic to retrieve TikTok connections
        # You can implement your own logic here
        connections = SocialMediaHandle.objects.filter(platform='tiktok')
        serializer = TikTokHandleSerializer(connections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Logic to update TikTok connection
        # You can implement your own logic here
        connection = SocialMediaHandle.objects.get(pk=pk)
        serializer = TikTokHandleSerializer(connection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Logic to delete TikTok connection
        # You can implement your own logic here
        connection = SocialMediaHandle.objects.get(pk=pk)
        connection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TikTokHandleList(APIView):
    def get(self, request):
        handles = SocialMediaHandle.objects.filter(platform='tiktok')
        serializer = TikTokHandleSerializer(handles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TikTokHandleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(platform='tiktok')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TikTokHandleDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(SocialMediaHandle, pk=pk, platform='tiktok')

    def get(self, request, pk):
        handle = self.get_object(pk)
        serializer = TikTokHandleSerializer(handle)
        return Response(serializer.data)

    def put(self, request, pk):
        handle = self.get_object(pk)
        serializer = TikTokHandleSerializer(handle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        handle = self.get_object(pk)
        handle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#Custom Social Handle
class CustomSocialHandleList(APIView):
    def get(self, request):
        handles = SocialMediaHandle.objects.all()
        serializer = CustomSocialHandleSerializer(handles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomSocialHandleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomSocialHandleDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(SocialMediaHandle, pk=pk)

    def get(self, request, pk):
        handle = self.get_object(pk)
        serializer = CustomSocialHandleSerializer(handle)
        return Response(serializer.data)

    def put(self, request, pk):
        handle = self.get_object(pk)
        serializer = CustomSocialHandleSerializer(handle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        handle = self.get_object(pk)
        handle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomURLList(APIView):
    def get(self, request):
        urls = CustomURL.objects.all()
        serializer = CustomURLSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomURLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomURLDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(CustomURL, pk=pk)

    def get(self, request, pk):
        url = self.get_object(pk)
        serializer = CustomURLSerializer(url)
        return Response(serializer.data)

    def put(self, request, pk):
        url = self.get_object(pk)
        serializer = CustomURLSerializer(url, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        url = self.get_object(pk)
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
