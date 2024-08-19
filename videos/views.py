from django.shortcuts import render
from rest_framework.authtoken.views import APIView, Response
from videos.models import Video
from .serializers import VideoSerializer, SingleVideoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.views.decorators.cache import cache_page
from videoflix_backend import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VideoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, format=None):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
class SingleVideoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, format=None):
        videoId = request.query_params.get("video_id")  # Hier ändern
        id_exists = Video.objects.filter(pk=videoId).exists()
        if id_exists:
            singleVideo = Video.objects.get(pk=videoId)
            serializer = SingleVideoSerializer(singleVideo)
            return Response(serializer.data)
        else:
            errors = {}
            errors['username'] = "das gewünschte Video ist aktuell nicht verfügbar"
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST) 
            
        
