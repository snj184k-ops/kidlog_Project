from django import forms
from .models import Child


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ["name", "birth_date", "photo"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
