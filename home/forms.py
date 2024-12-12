"""
Forms file to hangle all related home page forms
Subscription
Contact us
"""

from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    """
    A form for users to subscribe to email updates.

    Fields:
        email: The user's email address,
        used to receive subscription notifications.

    Customizations:
        - Email input field includes placeholder
        text and additional CSS classes for styling.
        - Ensures email validation and uniqueness,
        as defined in the Subscription model.
    """
    class Meta:
        """
        Add style and place holders to the form
        """
        model = Subscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control mr-2 mb-2 mb-lg-0',
                'placeholder': 'Enter your email',
                'style': 'border-radius: 0;',
            }),
        }


class ContactUsForm(forms.Form):
    """
    A form for users to send inquiries via the Contact Us page.

    Fields:
        - name: User's full name.
        - email: User's email address for responses.
        - subject: The subject of the inquiry.
        - message: Detailed message or inquiry from the user.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Your Full Name',
                'style': 'border-radius: 0;',
            }),
        label="Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Your Email Address',
                'style': 'border-radius: 0;',
            }),
        label="Email"
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Subject',
                'style': 'border-radius: 0;',
            }),
        label="Subject"
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'style': 'border-radius: 0;',
            }),
        label="Message"
    )
