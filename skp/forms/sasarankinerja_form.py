from django import forms
from django.contrib import messages
from django.utils.safestring import mark_safe

from skp.models import SasaranKinerja
from skp.utils import string_to_int
from usom.models import Account, UnitKerja


class SasaranKinerjaForm(forms.ModelForm):
    pegawai = forms.ModelChoiceField(queryset=Account.objects.none(), required=False)
    pejabat_penilai = forms.ModelChoiceField(
        queryset=Account.objects.none(), required=False
    )
    jenis_jabatan = forms.ChoiceField(
        choices=SasaranKinerja.JenisJabatan.choices, required=False
    )
    unor = forms.ModelChoiceField(queryset=UnitKerja.objects.none(), required=False)
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
        if self.instance.pk:
            user = self.instance.pegawai

        self.fields["pegawai"].initial = user.id
        self.fields["pegawai"].queryset = Account.objects.filter(id=user.id)
        self.fields["pegawai"].widget = forms.HiddenInput()

        self.fields["jenis_jabatan"].widget = forms.HiddenInput()
        if user.jenis_jabatan:
            self.fields["jenis_jabatan"].initial = string_to_int(
                SasaranKinerja.JenisJabatan, user.get_jenis_jabatan_display()
            )
        else:
            messages.add_message(
                request, messages.ERROR, "Jenis Jabatan Kosong".title()
            )
        self.fields["nama"].initial = user.get_complete_name()
        if user.jabatan:
            self.fields["jabatan"].initial = user.jabatan if user.jabatan else "---"
        else:
            messages.add_message(request, messages.ERROR, "Jabatan Kosong".title())
            # return redirect(reverse_lazy("admin:skp_sasarankinerja_changelist"))

        self.fields["unit_kerja"].initial = (
            user.unitkerja.unitkerja if user.unitkerja else "---"
        )
        if user.unitkerja:
            self.fields["unor"].widget = forms.HiddenInput()
            self.fields["unor"].initial = user.unitkerja.id if user.unitkerja else None
            self.fields["unor"].queryset = UnitKerja.objects.filter(
                id=user.unitkerja.id
            )
        else:
            messages.add_message(request, messages.ERROR, "Unit Kerja Kosong".title())
            # return redirect(reverse("admin:skp_sasarankinerja_changelist"))

        self.fields["pejabat_penilai"].widget = forms.HiddenInput()
        if user.atasan:
            self.fields["pejabat_penilai"].initial = user.atasan.id
            self.fields["pejabat_penilai"].queryset = Account.objects.filter(
                id=user.atasan.id
            )

            self.fields["nama_atasan"].initial = user.atasan.get_complete_name
            self.fields["jabatan_atasan"].initial = (
                user.atasan.jabatan if user.atasan.jabatan else "---"
            )
            self.fields["unit_kerja_atasan"].initial = (
                user.atasan.unitkerja.unitkerja if user.atasan.unitkerja else "---"
            )
            # self.fields["pejabat_penilai"].initial = user.atasan.id
            # self.fields["pejabat_penilai"].queryset = Account.objects.filter(
            #     id=user.atasan.id
            # )
            # self.fields["pejabat_penilai"].widget = forms.HiddenInput()

    def clean(self):
        periode_awal = self.cleaned_data.get("periode_awal", None)
        periode_akhir = self.cleaned_data.get("periode_akhir", None)
        pegawai = self.cleaned_data.get("pegawai", None)
        find_skp = SasaranKinerja.objects.filter(
            pegawai=pegawai,
            periode_awal__gte=periode_awal,
            periode_akhir__lte=periode_akhir,
            status=SasaranKinerja.Status.PERSETUJUAN
        )
        if find_skp.exists:
            raise forms.ValidationError(
                mark_safe("Mohon maaf, Sasaran Kinerja Pegawai pada periode {} - {} telah digunakan.<br>Silahkan menggunakan periode diluar periode {} - {}".format(
                    periode_awal.strftime("%d/%m/%Y"),
                    periode_akhir.strftime("%d/%m/%Y"),
                    periode_awal.strftime("%d/%m/%Y"),
                    periode_akhir.strftime("%d/%m/%Y"),
                ))
            )

        if periode_awal.year != periode_akhir.year:
            raise forms.ValidationError("Tahun Periode Tidak Sama".title())

        if periode_awal > periode_akhir:
            raise forms.ValidationError(
                "periode akhir lebih dahulu dari pada tanggal awal".title()
            )

        return self.cleaned_data

    class Meta:
        model = SasaranKinerja
        fields = (
            "unor",
            # "pejabat_penilai",
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
