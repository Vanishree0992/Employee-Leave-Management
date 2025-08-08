from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["reason"]
        widgets = {
            "reason": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
        }
