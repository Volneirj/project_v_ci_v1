from .forms import SubscriptionForm

def subscription_form(request):
    """
    Add the subscription form to the context globally.
    """
    return {'subscription_form': SubscriptionForm()}