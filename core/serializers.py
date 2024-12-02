from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MedicalData

User = get_user_model()

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'password', 
            'age', 'gender', 'diagnosis', 'treatment', 'medication'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'id': {'read_only': True},
            'name': {'required': False},
            'age': {'required': False, 'allow_null': True},
            'gender': {'required': False, 'allow_blank': True},
            'diagnosis': {'required': False, 'allow_blank': True},
            'treatment': {'required': False, 'allow_blank': True},
            'medication': {'required': False, 'allow_blank': True},
        }

    def validate(self, data):
        if self.context.get('action') == 'signup' and not data.get('name'):
            raise serializers.ValidationError({"name": "This field is required during signup."})
        return data

    def create(self, validated_data):
        validated_data["username"] = "222"
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = [
            'user', 'test_results', 'A1', 'A2', 'A3', 'A4', 'A5', 
            'A6', 'A7', 'A8', 'A9', 'A10', 'additional_info', 
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'user': {'read_only': True},  # Automatically set
            'test_results': {'required': False},  # Optional field
            'additional_info': {'required': False},  # Optional field
            'created_at': {'read_only': True},  # Auto-handled
            'updated_at': {'read_only': True},  # Auto-handled
        }

    def create(self, validated_data):
        # Automatically associate user
        user = self.context['request'].user  # Ensure logged-in user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update instance with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# class SignUpSerializer(serializers.ModelSerializer):
#     # Making the name field required for signup
#     name = serializers.CharField(max_length=255)
    
#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}  # Don't expose the password in the response
#         }
    
#     def create(self, validated_data):
#         # Create the user and set the password
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             name=validated_data['name'], 
#             username={0}
#         )
#         return user
    


from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

from .models import MedicalData

class MedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = ['user', 'test_results', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'additional_info', 'ai_detection']
        extra_kwargs = {
            'test_results': {'required': False},  # Make this field optional
            'additional_info': {'required': False},  # Make this field optional
            'ai_detection': {'read_only': True, 'required':True},  # Automatically set
        }
