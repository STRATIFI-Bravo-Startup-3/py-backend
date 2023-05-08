from rest_framework.response import Response 
from rest_framework.views import APIView 
from .models import About, Vision, Mission, Goal, Service 
from .serializers import AboutSerializer, VisionSerializer, MissionSerializer, GoalSerializer, ServiceSerializer
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from users.models import User

# My own imports for the rest_framework api_view
from django.http import JsonResponse
# If you using the api_view decorator in your view. You can then define permissions like below:
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions



def Home(request):
    return HttpResponse("the home page goes here")
    #return render(request, "", )

# APIOverview Urls
@ api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def apiOverview(request):
    api_urls = {
        'About': '/aboutus/',
        'Vision': '/vision/',
        'Mission': '/mission/',
        'Goal': '/goal/',
        'Service': '/service/',
    }

@ api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def about(request):
    abouts = About.objects.all()
    serializer = AboutSerializer(abouts, many=True)
    return Response(serializer.data)

    return HttpResponse("the About us page goes here")
    #return render(request, "", )


@ api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def vision(request):
    visions = Vision.objects.all()
    serializer = VisionSerializer(vissions, many=True)
    return Response(serializer.data)

    return HttpResponse("the Our Vission page goes here")
    #return render(request, "", )

@ api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def mission(request):
    missions = Mission.objects.all()
    serializer = MissionSerializer(missions, many=True)
    return Response(serializer.data)

    return HttpResponse("the Our Mission page goes here")
    #return render(request, "", )

@ api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def goal(request):
    goals = Goal.objects.all()
    serializer = GoalSerializer(goals, many=True)
    return Response(serializer.data)

    return HttpResponse("the Our Goal page goes here")
    #return render(request, "", )

@ api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def service(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

    return HttpResponse("the Our Service page goes here")
    #return render(request, "", )

'''
class PageView(APIView): 
    def get(self, request):  
        pages = Page.objects.all() 
        serializer = PageSerializer(pages, many=True)
        return Response({"pages": serializer.data})
    
    def post(self, request):  
        page = request.data.get('page') 
        serializer = PageSerializer(data=page) 
        if serializer.is_valid(raise_exception=True): 
            page_saved = serializer.save() 
        return Response({"success": "Page'{}' created successfully".format(page_saved)})

    def put(self, request, pk): 
        saved_page = get_object_or_404(Page.objects.all, pk=pk) 
        data =request.data.get('page') 
        serializer = PageSerializer(instance=saved_page, data=data, partial=True)
        if serializer.is_valid(raise_exception=True): 
            page_saved = serializer.save() 
        return Response({"success": "Page'{}' updated successfully".format(page_saved)})
    
    def delete(self, request, pk): 
        page = get_object_or_404(Page.objects.all(), pk=pk) 
        page.delete() 
        return Response ({"message":"Page with id'{}' has been deleted.".format(pk)})'''

