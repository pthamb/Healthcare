from django.db      import models

class Patient(models.Model):
    user            = models.ForeignKey('auth.User', on_delete=models.CASCADE)  
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    date_of_birth   = models.DateField()
    address         = models.TextField()
    phone_number    = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    

class Doctor(models.Model):
    name            = models.CharField(max_length=255)
    specialization  = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    

class PatientDoctorMapping(models.Model):
    patient         = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor          = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    user            = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    assigned_date   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name}"
