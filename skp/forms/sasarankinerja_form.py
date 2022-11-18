from django import forms
from skp.models import SasaranKinerja
from usom.models import Account, UnitKerja
from skp.utils import string_to_int


class SasaranKinerjaForm(forms.ModelForm):
    pegawai = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)
    pejabat_penilai = forms.ModelChoiceField(
        queryset=Account.objects.all(), required=False
    )
    unor = forms.ModelChoiceField(queryset=UnitKerja.objects.all(), required=False)
    nama = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    jabatan = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    unit_kerja = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    nama_atasan = forms.CharField(
        initial="---",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    jabatan_atasan = forms.CharField(
        initial="---",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    unit_kerja_atasan = forms.CharField(
        initial="---",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.request

        user = request.user
        self.fields["pegawai"].initial = user.id
        self.fields["pegawai"].queryset = Account.objects.filter(id=user.id)
        self.fields["pegawai"].widget = forms.HiddenInput()

        self.fields["jenis_jabatan"].initial = string_to_int(
            SasaranKinerja.JenisJabatan, user.get_jenis_jabatan_display()
        )
        self.fields["jenis_jabatan"].widget = forms.HiddenInput()

        self.fields["nama"].initial = user.get_complete_name
        self.fields["jabatan"].initial = user.jabatan if user.jabatan else "---"
        self.fields["unit_kerja"].initial = (
            user.unitkerja.unitkerja if user.unitkerja else "---"
        )
        if user.unitkerja:
            self.fields["unor"].initial = user.unitkerja.id if user.unitkerja else None
            self.fields["unor"].widget = forms.HiddenInput()
            self.fields["unor"].queryset = UnitKerja.objects.filter(
                id=user.unitkerja.id
            )

        if user.atasan:
            self.fields["nama_atasan"].initial = user.atasan.get_complete_name
            self.fields["jabatan_atasan"].initial = (
                user.atasan.jabatan if user.atasan.jabatan else "---"
            )
            self.fields["unit_kerja_atasan"].initial = (
                user.atasan.unitkerja.unitkerja if user.atasan.unitkerja else "---"
            )
            self.fields["pejabat_penilai"].initial = user.atasan.id
            self.fields["pejabat_penilai"].queryset = Account.objects.filter(
                id=user.atasan.id
            )
            self.fields["pejabat_penilai"].widget = forms.HiddenInput()
        # self.fields['nama'].initial = user.last().get_complate_name()
        # self.fields['nama'].initial = user.last().get_complate_name()

        # print('masuk sini')
        # self.fields['periode_awal'].widget = forms.TextInput(attrs={'class': 'datetimepicker-input'})

    class Meta:
        model = SasaranKinerja
        fields = (
            "unor",
            "pejabat_penilai",
            "pegawai",
            "jenis_jabatan",
            "nama",
            "jabatan",
            "unit_kerja",
            "nama_atasan",
            "jabatan_atasan",
            "unit_kerja_atasan",
            "periode_awal",
            "periode_akhir",
            "pendekatan",
        )
        # widgets = {
        #     'periode_awal': forms.TextInput(attrs={'class': 'datetimepicker-input'}),
        # }


class SKPForm(forms.ModelForm):
    unor = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    jabatan = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    unit_kerja = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    nama_atasan = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    jabatan_atasan = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    unit_kerja_atasan = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["periode_awal"].widget = forms.TextInput(
            attrs={"class": "datetimepicker-input form-control"}
        )
        self.fields["periode_akhir"].widget = forms.TextInput(
            attrs={"class": "datetimepicker-input form-control"}
        )
        self.fields["pendekatan"].widget.attrs["class"] = "form-control"
        # for f in self.visible_fields():
        #     f.field.widget.attrs['class'] = ' form-control'

    class Meta:
        model = SasaranKinerja
        fields = (
            "unor",
            "jabatan",
            "unit_kerja",
            "nama_atasan",
            "jabatan_atasan",
            "unit_kerja_atasan",
            "periode_awal",
            "periode_akhir",
            "pendekatan",
        )
