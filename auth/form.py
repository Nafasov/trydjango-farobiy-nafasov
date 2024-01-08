from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class MyUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'exampleFormControlInput1',
            'name': 'username',
            'placeholder': 'Username'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputPassword',
            'name': 'password',
            'placeholder': 'Password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputPassword2',
            'name': 'password2',
            'placeholder': 'Confirm password'
        })


class MyAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'exampleFormControlInput1',
            'name': 'username',
            'placeholder': 'Username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputPassword',
            'name': 'password',
            'placeholder': 'Password'
        })