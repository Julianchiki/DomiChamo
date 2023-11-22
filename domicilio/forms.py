from django import forms
from .models import MeasurementUnits, Categories, Elements, Inventories, Domicilies
from django.contrib.auth.models import User, Group

class AddElements(forms.Form):
    category_id = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="Selecciona una categoría", widget=forms.Select(attrs={'class': 'form-control', 'name': 'category_id'}))
    measurement_unit_id = forms.ModelChoiceField(queryset=MeasurementUnits.objects.all(), empty_label="Selecciona una unidad de medida", widget=forms.Select(attrs={'class': 'form-control', 'name': 'measurement_unit_id'}))

class FormAddElements(forms.ModelForm):
    class Meta:
        model = Elements
        fields = ['name', 'description', 'image']
    def __init__(self, *args, **kwargs):
        super(FormAddElements, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class FormEditElements(forms.ModelForm):
    class Meta:
        model = Elements
        fields = ['image']
    def __init__(self, *args, **kwargs):
        super(FormEditElements, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['readonly'] = True
    
class AddInventory(forms.Form):
    element_id = forms.ModelChoiceField(queryset=Elements.objects.all(), empty_label="Selecciona un producto", widget=forms.Select(attrs={'class': 'form-control'}))

class FormAddInventory(forms.ModelForm):
    class Meta:
        model = Inventories
        fields = ['amount', 'stock', 'price', 'expiration_date', 'lot_number']

class Assign(forms.Form):
    domicilie_id = forms.ModelChoiceField(queryset=Domicilies.objects.all(), empty_label="Selecciona un domicilio", widget=forms.Select(attrs={'class': 'form-control'}), label="Domicilio")
    
    def __init__(self, *args, **kwargs):
        super(Assign, self).__init__(*args, **kwargs)

        # Filtra los usuarios por el grupo con ID 3
        group_id = 3  # Reemplaza con el ID de tu grupo específico
        self.fields['user_id'] = forms.ModelChoiceField(
            queryset=User.objects.filter(groups__id=group_id).distinct(),
            empty_label="Selecciona un usuario",
            widget=forms.Select(attrs={'class': 'form-control'}),
            label="Domiciliario"
        )