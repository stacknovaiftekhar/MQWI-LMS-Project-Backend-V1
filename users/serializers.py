from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Teacher, Student
from enrolls.serializers import EnrollmentSerializer


GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

class TeacherSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Teacher
        fields = ['id', 'fullname', 'name_bn', 'email', 'username', 'password', 'gender', 'bio', 'expertise', 'image']

    def create(self, validated_data):
        # Extract User-Related Fields
        email = validated_data.pop('email')
        username = validated_data.pop('username', None)  # Optional if using as mobile
        password = validated_data.pop('password')

        # Use Email as Username if Username is not Supplied
        user = User.objects.create_user(
            username=email if not username else username,
            email=email,
            password=password
        )

        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        user = instance.user

        # Extract User-Related Data Safely
        user_data = validated_data.pop('user', {})

        email = user_data.get('email')
        if email:
            user.email = email

        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)

        user.save()

        # Update Teacher Model Fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        fields['enrollments'] = EnrollmentSerializer(many=True, read_only=True)
        return fields


class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True, required=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, write_only=True)
    username = serializers.CharField(validators=[])  # Disable UniqueValidator
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")  # for confirmation

    class Meta:
        model = User
        fields = ['fullname', 'email', 'gender', 'username', 'password', 'password2', 'is_staff', ]

    # --- FULLNAME VALIDATION ---
    def validate_fullname(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Full Name must contain only Letters and Spaces.")
        return value

    # --- EMAIL VALIDATION ---
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This Email Address is already Registered.")
        return value

    # --- USERNAME (MOBILE) VALIDATION ---
    def validate_username(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile Number must contain only Digits.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This Mobile Number (Username) is already Registered.")
        return value

    # --- PASSWORD MATCH VALIDATION ---
    def validate(self, data):
        # Check password length
        if len(data['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 Characters long."})        
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not Match."})
        return data

    def create(self, validated_data):
        fullname = validated_data.pop('fullname')
        gender = validated_data.pop('gender')
        is_staff = validated_data.get('is_staff', False)
        validated_data.pop('password2')  # Remove since not in User model

        # user = User.objects.create_user(**validated_data)
        # Secure user creation
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_staff=is_staff
        )

        # Create Profile (Teacher/Student)
        if user.is_staff:
            Teacher.objects.create(user=user, fullname=fullname, gender=gender)
        else:
            Student.objects.create(user=user, fullname=fullname, gender=gender)

        return user