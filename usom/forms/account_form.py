from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class AccountForm(forms.ModelForm):
    nama_lengkap = forms.CharField(label="",required=True, widget=forms.TextInput(attrs={'placeholder':"Nama Lengkap"}))
    gelar_depan = forms.CharField(label="Nama Lengkap",required=True, widget=forms.TextInput(attrs={'placeholder':"Gelar Depan"}))
    gelar_belakang = forms.CharField(label="",required=True, widget=forms.TextInput(attrs={'placeholder':"Gelar Belakang"}))
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )
    groups = forms.ModelMultipleChoiceField(
        label='Groups', 
        queryset=Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Groups',
            is_stacked=False 
        )
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")