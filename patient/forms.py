from django import forms
from .models import Patient
from django.contrib.auth.hashers import make_password
class PatientRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ['name', 'age','phone', 'password']
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Patient.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already registered")
        return phone
    def save(self, commit=True):
        patient = super().save(commit=False)
        patient.password = make_password(self.cleaned_data['password'])
        if commit:
            patient.save()
        return patient

class PatientLoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
