from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    pass

    class Meta:
        model = Room
        fields = ('name', 'password', 'image')

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mb-3', })
            field.required = False


        self.fields['name'].required = True
        self.fields['name'].label += '*'

 
