from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Video


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video

        fields = [
            "title",
            "description",
            "category",
            "video_file",
            "thumbnail",
            "access_type",
            "price",
            "is_published",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex. : Introduction à Python",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Décris le contenu de cette vidéo...",
                "rows": 5,
            }),

            "category": forms.Select(attrs={
                "class": "form-control",
            }),

            "video_file": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "video/*",
            }),

            "thumbnail": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),

            "access_type": forms.Select(attrs={
                "class": "form-control",
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "min": "0",
                "step": "0.01",
            }),

            "is_published": forms.CheckboxInput(attrs={
                "class": "form-checkbox",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        access_type = cleaned_data.get("access_type")
        price = cleaned_data.get("price")

        if access_type == Video.AccessType.FREE:
            cleaned_data["price"] = 0

        elif access_type == Video.AccessType.PAID:
            if price is None or price <= 0:
                self.add_error(
                    "price",
                    "Une vidéo payante doit avoir un prix supérieur à 0.",
                )

        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex. : Python Programming"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Describe this category...",
                "rows": 4
            }),
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Choose a username"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Create a password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm your password"
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user