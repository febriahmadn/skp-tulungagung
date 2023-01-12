from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from usom.models import Account, UnitKerja
from usom.utils import image_validation


class AccountForm(forms.ModelForm):
    unitkerja = forms.ModelChoiceField(queryset=UnitKerja.objects.all(), required=False)
    atasan = forms.ModelChoiceField(queryset=Account.objects.none(), required=False)
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
        if "atasan" in self.data:
            atasan = self.data.get("atasan", None)
            if atasan.isnumeric() and int(atasan) != 0:
                self.fields["atasan"].queryset = Account.objects.filter(
                    pk=self.data.get("atasan", None)
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
            "status_pegawai"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unitkerja"].label = "Unit Kerja"


class UploadFotoPegawai(forms.ModelForm):
    foto = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "custom-file-input"})
    )

    def clean_foto(self):
        foto = self.cleaned_data.get("foto")
        image_validation(foto)
        return self.cleaned_data["foto"]

    class Meta:
        model = Account
        fields = ("foto",)
