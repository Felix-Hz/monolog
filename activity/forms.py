from django import forms
from .models import ActivityModel


class ActivityForm(forms.ModelForm):
    class Meta:
        model = ActivityModel
        fields = ["name", "description", "tags", "status"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter activity name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 4,
                    "placeholder": "Describe your activity...",
                }
            ),
            "tags": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "e.g. work, personal"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
