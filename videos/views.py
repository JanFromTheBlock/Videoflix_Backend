from django.shortcuts import render
from rest_framework.authtoken.views import APIView, Response
from videos.models import Video
from .serializers import VideoSerializer

class VideoView(APIView):
    #authentication_classes = [authentication.TokenAuthentikation]
    permission_classes = []
    
    def get(self, request, format=None):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)