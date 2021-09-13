from reviews.models import Title, Genre, Category # Review
from users.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
#from api_yamdb.settings import DEFAULT_FROM_EMAIL


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleUpdateCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True, required=False)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug', required=False)

    class Meta:
        model = Title
        fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(read_only=True,
#                                           slug_field='username')
#     title = serializers.SlugRelatedField(read_only=True, slug_field='pk')
#
#     class Meta:
#         model = Review
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Неверный ник-нейм')
        return value


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    confirmation_code = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username'),
            confirmation_code=default_token_generator
        )
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()