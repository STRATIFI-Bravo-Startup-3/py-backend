from rest_framework.response import Response 
from rest_framework.views import APIView 
from .models import Page 
from .serializers import PageSerializer

from django.shortcuts import render, HttpResponse

def Home(request):
    return HttpResponse("the home page goes here")
    #return render(request, "", )

def Aboutus(request):
    return HttpResponse("the About us page goes here")
    #return render(request, "", )


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
        return Response ({"message":"Page with id'{}' has been deleted.".format(pk)})

