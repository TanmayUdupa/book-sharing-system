from django import forms
from .models import ShippedTo, User
from django.core.validators import MaxValueValidator, MinValueValidator

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
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
            'autofocus': True,
        }),required=True
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
    
class ReviewForm(forms.Form):
    book_title = forms.ChoiceField(required=True)
    review_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
            'autofocus': True
        }),required=True
    )
    rating = forms.DecimalField(max_digits=2, decimal_places=1,
        widget=forms.NumberInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    user_rating = forms.DecimalField(max_digits=2, decimal_places=1,
        widget=forms.NumberInput(attrs={
            'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
        }),required=True
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        del kwargs['user']
        super().__init__(*args, **kwargs)
        to_be_reviewed = ShippedTo.objects.filter(to_user = self.user, transaction_type = 'Borrowing')
        details = set()
        for shipped in to_be_reviewed:
            details.add(shipped.book_id)
        self.fields['book_title'].choices = tuple((detail.id, detail.title) for detail in details)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'profile_pic', 'address']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
                'autofocus': True,
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
            }),
            'address': forms.TextInput(attrs={
                'class': 'px-4 py-2 transition duration-300 border border-gray-300 rounded focus:border-transparent focus:outline-none focus:ring-4 focus:ring-blue-200',
            }),
        }