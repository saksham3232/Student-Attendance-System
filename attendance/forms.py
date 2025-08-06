from django import forms
from .models import Student, Holiday

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'phone', 'address', 'photo']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student ID (e.g., ST001)'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Image size should not exceed 5MB')

            # Some storage backends may not populate content_type; be defensive
            content_type = getattr(photo, 'content_type', None)
            if content_type and not content_type.startswith('image/'):
                raise forms.ValidationError('Please upload a valid image file')

        return photo


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter holiday description'
            })
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            from django.utils import timezone
            if date < timezone.now().date():
                raise forms.ValidationError('Holiday date cannot be in the past')
        return date
