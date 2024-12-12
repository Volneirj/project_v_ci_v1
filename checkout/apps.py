from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Configuration for the Checkout application.

    This class defines application-specific settings and setups
    signals for the Checkout app.
    """
    name = 'checkout'

    def ready(self):
        import checkout.signals
