from django import forms
from skp.models import SasaranKinerja

class SasaranKinerjaForm(forms.ModelForm):
    unor = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    jabatan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    unit_kerja = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    nama_atasan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    jabatan_atasan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    unit_kerja_atasan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print('masuk sini')
        # self.fields['periode_awal'].widget = forms.TextInput(attrs={'class': 'datetimepicker-input'})

    class Meta:
        model = SasaranKinerja
        fields = ('unor','jabatan','unit_kerja','nama_atasan','jabatan_atasan','unit_kerja_atasan','periode_awal','periode_akhir','pendekatan')
        # widgets = {
        #     'periode_awal': forms.TextInput(attrs={'class': 'datetimepicker-input'}),
        # }

class SKPForm(forms.ModelForm):
    unor = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    jabatan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    unit_kerja = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    nama_atasan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    jabatan_atasan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    unit_kerja_atasan = forms.CharField(max_length=255, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['periode_awal'].widget = forms.TextInput(attrs={'class': 'datetimepicker-input form-control'})
        self.fields['periode_akhir'].widget = forms.TextInput(attrs={'class': 'datetimepicker-input form-control'})
        self.fields['pendekatan'].widget.attrs['class']='form-control'
        # for f in self.visible_fields():
        #     f.field.widget.attrs['class'] = ' form-control'
    
    class Meta:
        model = SasaranKinerja
        fields = ('unor','jabatan','unit_kerja','nama_atasan','jabatan_atasan','unit_kerja_atasan','periode_awal','periode_akhir','pendekatan')
