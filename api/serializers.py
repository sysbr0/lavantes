# serializers.py

from rest_framework import serializers
from .models import Message , Product_imges , Swapper_Imges

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender_name', 'email', 'subject', 'message', 'timestamp']





class Product_imgesSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Add a method to get the full URL

    class Meta:
        model = Product_imges
        fields = ['id', 'product_ham', 'image_url', 'active', 'date']  # Use 'image_url' instead of 'image'

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    




class swapper_imgesSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Add a method to get the full URL

    class Meta:
        model = Swapper_Imges
        fields = ['id',  'image_url', 'active', 'date' , 'name']  # Use 'image_url' instead of 'image'

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    



