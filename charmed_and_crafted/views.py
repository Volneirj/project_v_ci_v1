"""
Views for the Charmed and Crafted application.

This module contains custom error handlers (404, 500) and any other
application-specific view logic.
"""
from django.shortcuts import render

def handler404(request, exception): # pylint: disable=unused-argument
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)

def handler500(request):
    """ Error Handler 500 - Dataabase issues"""
    return render(request, "errors/500.html", status=500)
