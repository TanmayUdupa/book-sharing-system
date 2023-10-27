from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
            'autofocus': True
        }),required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )


class SignUpForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
            'autofocus': True,
        }),required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }), required=True
    )
