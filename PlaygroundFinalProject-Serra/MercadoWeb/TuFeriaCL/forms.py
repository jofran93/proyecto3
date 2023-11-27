from django import forms
from .models import Post, UserProfile, Item
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password  # Importa la función de validación de contraseña
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm # Esta incluye la lógica necesaria para validar el nombre de usuario y la contraseña y permitir el inicio de sesión.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    username = forms.CharField(label='Nombre de usuario', max_length=30, required=True,
    help_text='Requerido. Máximo 30 caracteres. Letras, dígitos y @/./+/-/_ solamente.')

    class Meta:
        model = UserProfile
        fields = ['username', 'full_name', 'email', 'phone_number', 'profile_picture']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError('\n'.join(e.messages))
        return password
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return confirm_password
    
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        
        self.fields.pop('username')
        self.fields.pop('password')
        
        self.fields['user'] = forms.CharField(
            label="Nombre de usuario",
            widget=forms.TextInput(attrs={'autofocus': True}),
        )
        self.fields['password'] = forms.CharField(
            label="Contraseña",
            strip=False,
            widget=forms.PasswordInput,
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('user')
        password = cleaned_data.get('password')

        # Verificar la autenticación utilizando UserProfile
        try:
            user_profile = UserProfile.objects.get(user__username=username)
            if not user_profile.check_password(password):
                raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
        except UserProfile.DoesNotExist:
            raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username', 'password',
            Submit('submit', 'Iniciar sesión')
        )
        
        
        

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['user', 'name', 'price', 'description', 'photo', 'quantity_available']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'item', 'status']
        
