from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views import View
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CarModel, Link
from .serializers import UserSerializer, TokenObtainPairSerializer, CarSerializer, LinkSerializer
from rest_framework.response import Response
# from .models import Message
from .permissions import AuthorAllStaffAllButEditOrReadOnly
# from .serializers import MessageSerializer


class RegisterView(APIView):

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class CarAPIView(APIView):

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = CarModel.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = CarSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


class ShortenerListAPIView(ListAPIView):
    queryset=Link.objects.all()
    serializer_class=LinkSerializer


class ShortenerCreateApiView(CreateAPIView):
    serializer_class=LinkSerializer


class Redirector(View):
    def get(self,request, shortener_link, *args, **kwargs):
        shortener_link=settings.HOST_URL+'/'+self.kwargs['shortener_link']
        redirect_link=Link.objects.filter(shortened_link=shortener_link).first().original_link
        return redirect(redirect_link)

from rest_framework import viewsets




class MessageViewSet(viewsets.ModelViewSet):

    permission_classes = [AuthorAllStaffAllButEditOrReadOnly] # Custom permission class used

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)