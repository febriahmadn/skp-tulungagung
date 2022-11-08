from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from skp.models import SasaranKinerja

class SasaranKinerjaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print('masuk sini')
        # self.fields['periode_awal'].widget = forms.TextInput(attrs={'class': 'datetimepicker-input'})

    class Meta:
        model = SasaranKinerja
        fields = '__all__'
        # widgets = {
        #     'periode_awal': forms.TextInput(attrs={'class': 'datetimepicker-input'}),
        # }
