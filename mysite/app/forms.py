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
    profile_pic = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }), required=True
    )

class AddBookForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    author = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    isbn = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    genre_id = forms.ChoiceField(choices = ((4, "Fiction"), 
                                            (5, "Mystery"), 
                                            (6, "Fantasy"), 
                                            (7, "Biography"), 
                                            (8, "Romance"),
                                            (9, "Horror"),
                                            (10, "Science Fiction"),
                                            (11, "Historical"),
                                            (12, "Thriller"),
                                            (13, "Adventure")), required=True)
    publication_year =  forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    cover_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }), required=True
    )
    condition_desc = forms.ChoiceField(choices = (("GOOD", "Good"), 
                                            ("ACCEPTABLE", "Acceptable"), 
                                            ("POOR", "Poor")), required=True)