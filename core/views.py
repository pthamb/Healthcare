from django.shortcuts                   import render
from django.contrib.auth.models         import User
from django.contrib.auth.hashers        import make_password
from rest_framework.response            import Response
from rest_framework.decorators          import api_view, permission_classes
from rest_framework                     import status
from rest_framework_simplejwt.tokens    import RefreshToken
from rest_framework.permissions         import IsAuthenticated
from .models                            import Patient, Doctor, PatientDoctorMapping
from .serializers                       import PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer


@api_view(['POST'])
def register(request):
    
    try:
        
        username                        = request.data.get('username')
        email                           = request.data.get('email')
        password                        = request.data.get('password')

        
        if not username or not email or not password:
            return Response({"message": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        
        hashed_password                 = make_password(password)
        user = User.objects.create(username=username, email=email, password=hashed_password)

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['POST'])
def login(request):
    
    try:
        
        username                        = request.data.get('username')
        password                        = request.data.get('password')

        
        if not username or not password:
            return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        
        user                            = User.objects.filter(username=username).first()

        if user and user.check_password(password):  
            
            refresh                     = RefreshToken.for_user(user)
            return Response({
                'refresh'               : str(refresh),
                'access'                : str(refresh.access_token)
            }, status                   = status.HTTP_200_OK)

        return Response({"message": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    




@api_view(['GET', 'POST'])  
@permission_classes([IsAuthenticated])  
def patients(request):

    if request.method       == 'GET':
       
        try:
            patients        = Patient.objects.filter(user=request.user)
            
            serializer      = PatientSerializer(patients, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method     == 'POST':
        
        try:
            data = request.data
            
            data['user']    = request.user.id  
            
            serializer      = PatientSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  
def patient_details(request, id):
    
    try:
        
        patient             = Patient.objects.filter(id=id, user=request.user).first()

        
        if not patient:
            return Response({"message": "Patient not found or you do not have access to this patient."}, status=status.HTTP_404_NOT_FOUND)

        
        if request.method   == 'GET':
            serializer = PatientSerializer(patient)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        
        elif request.method == 'PUT':
            serializer      = PatientSerializer(patient, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        elif request.method == 'DELETE':
            patient.delete()
            
            return Response({"message": "Patient deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  
def manage_doctors(request):
    
    try:
        
        if request.method == 'GET':
            doctors         = Doctor.objects.all()  
            
            serializer      = DoctorSerializer(doctors, many=True) 
             
            return Response(serializer.data, status=status.HTTP_200_OK)

        
        elif request.method == 'POST':
            data            = request.data  
            
            serializer      = DoctorSerializer(data=data)  

            if serializer.is_valid():
                serializer.save()  
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  
def doctor_details(request, id):
    
    try:
        
        doctor              = Doctor.objects.filter(id=id).first()

        if not doctor:
            
            return Response({"message": "Doctor not found or you do not have access to this doctor."}, status=status.HTTP_404_NOT_FOUND)

        
        if request.method == 'GET':
            
            serializer      = DoctorSerializer(doctor)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

       
        elif request.method == 'PUT':
            
            serializer      = DoctorSerializer(doctor, data=request.data, partial=True)  
            
            if serializer.is_valid():
                
                serializer.save() 
                 
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        elif request.method == 'DELETE':
            
            doctor.delete()
            
            return Response({"message": "Doctor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  
def patient_doctor_mappings(request):
    
    try:
        
        if request.method == 'GET':
            
            mappings        = PatientDoctorMapping.objects.all()  
            
            serializer      = PatientDoctorMappingSerializer(mappings, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        
        elif request.method == 'POST':
            
            patient_id      = request.data.get('patient_id')
            
            doctor_id       = request.data.get('doctor_id')

            
            patient         = Patient.objects.filter(id=patient_id).first()
            
            doctor          = Doctor.objects.filter(id=doctor_id).first()

            if not patient:
                return Response({"message": "Patient not found."}, status=status.HTTP_400_BAD_REQUEST)
            if not doctor:
                return Response({"message": "Doctor not found."}, status=status.HTTP_400_BAD_REQUEST)

            
            mapping         = PatientDoctorMapping(patient=patient, doctor=doctor, user=request.user)
            mapping.save()

            
            serializer      = PatientDoctorMappingSerializer(mapping)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_doctors_for_patient(request, patient_id):
    
    try:
        
        patient             = Patient.objects.filter(id=patient_id).first()

        if not patient:
            return Response({"message": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        
        mappings            = PatientDoctorMapping.objects.filter(patient=patient)

        
        if not mappings:
            return Response({"message": "No doctors assigned to this patient."}, status=status.HTTP_404_NOT_FOUND)

        
        serializer          = PatientDoctorMappingSerializer(mappings, many=True)

        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
def remove_doctor_from_patient(request, id):
    
    try:
        
        if request.method == 'DELETE':
            
            mapping = PatientDoctorMapping.objects.filter(id=id).first()

            if not mapping:
                return Response({"message": "Mapping not found."}, status=status.HTTP_404_NOT_FOUND)

            
            if mapping.user != request.user:
                return Response({"message": "You do not have permission to remove this doctor."}, status=status.HTTP_403_FORBIDDEN)

            
            mapping.doctor = None
            mapping.save()  
            return Response({"message": "Doctor removed from patient successfully."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)