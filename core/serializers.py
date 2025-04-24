from rest_framework         import serializers
from .models                import Patient, Doctor, PatientDoctorMapping

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Patient
        fields              = ['id', 'user', 'first_name', 'last_name', 'date_of_birth', 'address', 'phone_number']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Doctor
        fields              = '__all__'

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model               = PatientDoctorMapping
        fields              = '__all__'
