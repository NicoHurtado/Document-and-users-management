from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Estudiante

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Solo letras, números y @/./+/-/_.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>TU contraseña no puede ser muy parecida a tu usuario.</li><li>Tu contraseña tiene que tener 8 caracteres.</li><li>Tu contraseña no puede ser una contraseña usualmente usada.</li><li>Tu contraseña no puede consistir únicamente en números.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirma contraseña'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña de antes, para confirmar.</small></span>'




# Create Add Record Form
class AddRecordForm(forms.ModelForm):
	cedula = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Cedula", "class":"form-control"}), label="")
	nombre = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Nombre", "class":"form-control"}), label="")
	apellido = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Apellido", "class":"form-control"}), label="")
	edad = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Edad", "class":"form-control"}), label="")
	

	class Meta:
		model = Estudiante
		exclude = ("user",)
