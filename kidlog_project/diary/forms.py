from django import forms
from .models import DiaryRecord


class DiaryRecordForm(forms.ModelForm):
    class Meta:
        model = DiaryRecord
        fields = ["time", "note"]
        widgets = {
            "time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "4",
                    "placeholder": "出来事や感想の記録",
                }
            ),
        }
