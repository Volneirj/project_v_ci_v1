from django.core.mail.backends.smtp import EmailBackend

class CustomEmailBackend(EmailBackend):
    """
    Custom email backend extending Django's SMTP email backend.
    Provides additional customization for opening connections to the SMTP server.
    """
    def open(self):
        """Open a connection to the email server."""
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(
                self.host, self.port, timeout=self.timeout
                )
            self.connection.ehlo()
            if self.use_tls:
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if self.fail_silently:
                return False
            raise
