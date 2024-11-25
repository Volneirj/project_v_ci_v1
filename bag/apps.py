"""
Module for the configuration 
of the Bag application.
"""
from django.apps import AppConfig

class BagConfig(AppConfig):
    """
    This class is responsible for 
    setting application-specific settings
    such as the default auto field and the app's name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bag'
