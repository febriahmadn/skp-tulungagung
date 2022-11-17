from django import forms
from ..models import SasaranKinerja


class CustomFooForm(forms.ModelForm):
    class Meta:
        model = SasaranKinerja
        fields = "__all__"
