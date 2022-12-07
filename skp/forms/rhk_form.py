from django import forms

from skp.models import RencanaHasilKerja
from usom.models import UnitKerja


class RHKJPTForm(forms.ModelForm):
    unor = forms.ModelChoiceField(
        queryset=UnitKerja.objects.all(), required=False, label="Unit Kerja"
    )

    class Meta:
        model = RencanaHasilKerja
        fields = (
            "skp",
            "klasifikasi",
            "unor",
            "jenis",
            "rencana_kerja",
            "penugasan_dari",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["jenis"].label = "Jenis RHK"
        self.fields["skp"].widget = forms.HiddenInput()
        self.fields["klasifikasi"] = forms.ChoiceField(
            required=False,
            choices=[("", "---------")] + RencanaHasilKerja.Klasifikasi.choices,
            widget=forms.Select(attrs={"onchange": "onChangeKlasifikasi($(this))"}),
        )


class RHKJFJAForm(forms.ModelForm):
    induk = forms.ModelChoiceField(
        queryset=RencanaHasilKerja.objects.all(),
        required=False,
        label="Hasil Kerja Atasan yang Diintervensi",
    )

    class Meta:
        model = RencanaHasilKerja
        fields = (
            "induk",
            # 'unor',
            "jenis",
            "rencana_kerja",
            # 'penugasan_dari',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
