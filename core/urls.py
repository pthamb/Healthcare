from django.urls        import path
from .views             import register, login, patients, patient_details, manage_doctors, doctor_details, patient_doctor_mappings, get_doctors_for_patient, remove_doctor_from_patient

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('patients/', patients, name='patients'),
    path('patients/<int:id>/', patient_details, name='patient_details'),
    path('doctors/', manage_doctors, name='manage_doctors'),
    path('doctors/<int:id>/', doctor_details, name='doctor_details'),
    path('mappings/', patient_doctor_mappings, name='patient_doctor_mappings'),
    path('mappings/<int:patient_id>/', get_doctors_for_patient, name='get_doctors_for_patient'),
    path('mappings/<int:id>/', remove_doctor_from_patient, name='remove_doctor_from_patient'),
]
