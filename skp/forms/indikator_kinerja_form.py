from django import forms
from skp.models import IndikatorKinerjaIndividu


class IndikatorForm(forms.ModelForm):
    # induk = forms.ModelChoiceField(queryset=RencanaHasilKerja.objects.all(), required=False, label="Hasil Kerja Atasan yang Diintervensi")
    class Meta:
        model = IndikatorKinerjaIndividu
        # fields = (
        #     'induk',
        #     # 'unor',
        #     'jenis',
        #     'rencana_kerja',
        #     # 'penugasan_dari',
        # )
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
