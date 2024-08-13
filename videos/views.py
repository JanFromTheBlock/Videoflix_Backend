from django.shortcuts import render
from rest_framework.authtoken.views import APIView, Response
from videos.models import Video
from .serializers import VideoSerializer, SingleVideoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class VideoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
class SingleVideoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
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
            
        
