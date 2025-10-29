from django import forms
from .models import (
    MilkRecord,
    SleepRecord,
    PoopRecord,
    PeeRecord,
    TemperatureRecord,
    FoodRecord,
    HtmtRecord,
)


class MilkRecordForm(forms.ModelForm):
    class Meta:
        model = MilkRecord
        fields = ["time", "amount", "note"]
        widgets = {
            "time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ml",
                }
            ),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ["start_time", "end_time", "note"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class PoopRecordForm(forms.ModelForm):
    class Meta:
        model = PoopRecord
        fields = ["time", "note"]
        widgets = {
            "time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class PeeRecordForm(forms.ModelForm):
    class Meta:
        model = PeeRecord
        fields = ["time", "note"]
        widgets = {
            "time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class TemperatureRecordForm(forms.ModelForm):
    class Meta:
        model = TemperatureRecord
        fields = ["time", "temperature", "note"]
        widgets = {
            "time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "temperature": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "class": "form-control",
                    "placeholder": "℃",
                }
            ),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class FoodRecordForm(forms.ModelForm):
    class Meta:
        model = FoodRecord
        fields = ["time", "menu", "amount", "note"]
        widgets = {
            "time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "menu": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "回",
                }
            ),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class HtmtRecordForm(forms.ModelForm):
    class Meta:
        model = HtmtRecord
        fields = ["height", "weight", "date"]
        widgets = {
            "height": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "身長(cm)"}
            ),
            "weight": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "体重(kg)"}
            ),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
