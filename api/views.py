from django.shortcuts import render

from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView,CreateAPIView
from posts.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, CommentListSerializer, CommentCreateSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwner
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_comments.models import Comment

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView #generic API View
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response



class UserLoginAPIView(APIView):
	permission_classes = [AllowAny,]
	serializer_class = UserLoginSerializer

	def post(self, request, format=None): #login is a post request
		data = request.data #retrieve the data from the POST reque$t
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data=serializer.data #reassign it
			return Response(new_data, status=HTTP_200_OK) #successful
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserCreateView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
                content_type=ContentType.objects.get_for_model(Post), #the type of the object...which is Post
                site=Site.objects.get(id=1),
                user = self.request.user,
                user_name = self.request.user.username,
                submit_date = timezone.now()
            )


# Create your views here.
class CommentListAPIView(ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	permission_classes = [AllowAny,]

	def get_queryset(self, *args, **kwargs):
		queryset = Comment.objects.all()
		query = self.request.GET.get("query")
		if query:
			queryset = queryset.filter(
				Q(object_pk=query)|
				Q(user = query)
				).distinct()
		return queryset


class PostListAPIView(ListAPIView):
	queryset = Post.objects.all() #-- we don't need this anymore
	serializer_class = PostListSerializer
	permission_classes = [AllowAny]
	filter_backends = [SearchFilter]
	search_fields = ['title', 'content', 'author__username'] #feilds to search for

	#REPLACED BY SEARCH FIELDS :D 

	# def get_queryset(self, *args, **kwargs): #override API view getting it's queryset
	# 	queryset = Post.objects.all()
	# 	query = self.request.GET.get("query") #get the query string from the get request
	# 	if query:
	# 		queryset = queryset.filter(
	# 			Q(title__icontains=query)|
	# 			Q(content__icontains=query)
	# 			)
	# 	return queryset

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'
	permission_classes = [AllowAny]

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'
	permission_classes = [IsAuthenticated, IsAdminUser]


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    def perform_create(self, serializer):
    	serializer.save(author=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'
    permission_classes = [IsAuthenticated, IsOwner]