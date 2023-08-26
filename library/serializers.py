from rest_framework import serializers
from .models import Books

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'title', 'description', 'price', 'shabak', 'copies_available', 'genre', 'author']
        extra_kwargs = {
            'id': {'required': False},
            'author': {'required': False},
            'title': {'required': False},
            'description': {'required': False},
            'price': {'required': False},
            'shabak': {'required': False},
            'copies_available': {'required': False},
            'genre': {'required': False},

        }