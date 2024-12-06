from django import forms
from .models import Subscription



class SubscriptionForm(forms.ModelForm):
    """
    A form for users to subscribe to email updates.
    
    Fields:
        email: The user's email address, used to receive subscription notifications.

    Customizations:
        - Email input field includes placeholder text and additional CSS classes 
          for styling.
        - Ensures email validation and uniqueness, as defined in the Subscription model.
    """
    class Meta:
        model = Subscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control mr-2 mb-2 mb-lg-0',
                'placeholder': 'Enter your email',
                'style': 'border-radius: 0;',
            }),
        }
