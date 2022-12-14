from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from usom.models import Account


class AccountForm(forms.ModelForm):
    atasan = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)
    nama_lengkap = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nama Lengkap",
                "class": "form-control max-w-350px",
            }
        ),
    )
    gelar_depan = forms.CharField(
        label="Nama Lengkap",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Gelar Depan",
                "class": "form-control max-w-130px",
            }
        ),
    )
    gelar_belakang = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Gelar Belakang",
                "class": "form-control max-w-130px",
            }
        ),
    )
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )
    groups = forms.ModelMultipleChoiceField(
        label="Groups",
        queryset=Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name="Groups", is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")
        if self.instance.pk:
            self.fields["atasan"].queryset = Account.objects.all().exclude(
                pk=self.instance.pk
            )


class EditProfilPegawai(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "email",
            "unitkerja",
            "jenis_jabatan",
            "jabatan",
            "golongan",
            "eselon",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unitkerja"].label = "Unit Kerja"
