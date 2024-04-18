import cv2
from django.http import HttpResponse, HttpResponseServerError, StreamingHttpResponse
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, VideoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Video
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
import cv2
import threading

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class AllVideosListCreate(generics.ListAPIView):
    queryset=Video.objects.all()
    serializer_class=VideoSerializer
    permission_classes=[AllowAny]



class VideoListCreate(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Video.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class VideoByBucketIdAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, bucket_id):
        try:
            video = Video.objects.get(bucket_id=bucket_id)
            serializer = VideoSerializer(video)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            return Response({'message': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VideoDelete(generics.DestroyAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Video.objects.filter(author=user)

class VideoEdit(generics.UpdateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class UpdateVideoTitleView(generics.RetrieveUpdateAPIView):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  
        new_title = request.data.get('title')
        print(new_title)
        instance.title = new_title
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    



class VideoSearchAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
            search_term = self.kwargs.get('search_term')
            queryset = Video.objects.filter(title__icontains=search_term)
            return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        self.connections = self.connections+1
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
    
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def generate_video_frames(camera):
    while True:
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            break
class VideoStreamAPIView(generics.GenericAPIView):
    permission_classes=[AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            cameraObject = VideoCamera()
            return StreamingHttpResponse(generate_video_frames(cameraObject), content_type="multipart/x-mixed-replace;boundary=frame")
        except Exception as e:
            return HttpResponse("Failed to stream video: {}".format(str(e)))
      