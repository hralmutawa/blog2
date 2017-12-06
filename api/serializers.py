from rest_framework import serializers
from posts.models import Post
from django_comments.models import Comment
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	token = serializers.CharField(read_only=True, allow_blank=True)

	def validate(self, data): #override the validate data
		user_obj=None
		username = data.get('username')
		password = data.get('password')

		if username == '':
			raise serializers.ValidationError("A username is required") #validationError for message

		user = User.objects.filter(username=username)
		if user.exists():
			user_obj = user.first()
		else:
			raise serializers.ValidationError("This username does not exist")

		if user_obj:
			if not user_obj.check_password(password): #password validation, password method from user model returns true or false
				raise serializers.ValidationError("Incorrect credentials, please try again")
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(user_obj) #generating a token, assigning it to the user
		token = jwt_encode_handler(payload) #encoding the token generated for the user
		data['token'] = token #tokennnnn
		return data



class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={"input_type":"password"}, write_only=True) #hasing the password -- not returning it in the response
	class Meta:
		model = User
		fields = ['username','password']


	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username) #creating user object
		new_user.set_password(password)
		new_user.save()
		return validated_data


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'username', 'first_name', 'last_name']

class PostListSerializer(serializers.ModelSerializer):
	person = serializers.SerializerMethodField() #custom value in a field
	detail_page = serializers.HyperlinkedIdentityField(
		view_name="api:detail",
		lookup_field = "slug",
		lookup_url_kwarg="post_slug" #correlates to what is in the view
		)
	class Meta:
		model = Post
		fields = ['title', 'author', 'slug', 'content','publish', 'detail_page', 'person']

	def get_person(self, obj): #get has to matc the method field. Receives object. Self just has the request a method FIELD. the field is the person
		return str(obj.author.username)



class PostDetailSerializer(serializers.ModelSerializer):
    #user = serializers.SerializerMethodField()
    author = UserSerializer()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','author','title', 'slug', 'content','publish','draft', 'image', 'comments']

    # def get_user(self, obj): now that we have a userserializer, we don't need this
    #     return str(obj.author.username)

    def get_comments(self, obj):
        comment_queryset = Comment.objects.filter(object_pk=obj.id)
        comments = CommentListSerializer(comment_queryset, many=True).data
        return comments

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'content','publish','draft']

class CommentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ["object_pk","user", "comment", "submit_date"] #object pk is the id of the post that it is related to

class CommentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment 
		fields = ["object_pk","comment"]

