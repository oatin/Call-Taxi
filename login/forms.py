from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser
from home.models import TaxiDriver

class CustomSignupForm(UserCreationForm):
    class_name_input = "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"class": class_name_input}))
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={"class": class_name_input})  # Use Select widget for dropdown
    )

    license_number = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={"class": class_name_input}))
    car_model = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": class_name_input}))
    car_plate = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": class_name_input}))

    class Meta:
        model = CustomUser
        fields = ['role', 'username', 'password1', 'password2' , 'phone_number']

    def save(self, commit=True):
        user = super(CustomSignupForm, self).save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.role = self.cleaned_data['role']
        
        if commit:
            user.save()

        # สร้างข้อมูล TaxiDriver หากเลือก role เป็นคนขับ
        if user.role == 'driver':
            TaxiDriver.objects.create(
                user=user,
                license_number=self.cleaned_data['license_number'],
                car_model=self.cleaned_data['car_model'],
                car_plate=self.cleaned_data['car_plate']
            )
        return user