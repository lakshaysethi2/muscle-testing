from django import forms

from .models import User


class ProfileEditForm(forms.Form):
    """Form for editing the user profile (bio, testing_method, avatar)."""

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "w-full rounded-lg border-gray-300 shadow-sm "
                "focus:border-indigo-500 focus:ring-indigo-500",
                "placeholder": "A few words about yourself...",
            }
        ),
    )

    testing_method = forms.ChoiceField(
        choices=User.TestingMethod.choices,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "w-full rounded-lg border-gray-300 shadow-sm "
                "focus:border-indigo-500 focus:ring-indigo-500",
            }
        ),
    )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "w-full text-sm text-gray-500 "
                "file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 "
                "file:text-sm file:font-semibold file:bg-indigo-50 "
                "file:text-indigo-700 hover:file:bg-indigo-100",
            }
        ),
    )
