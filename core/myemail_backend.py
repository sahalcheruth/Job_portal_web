from django.core.mail.backends.smtp import EmailBackend
import ssl

class CustomEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):  # Fix here: __init, not init
        super().__init__(*args, **kwargs)
        self.local_hostname = 'localhost'
        self.debug_level = 0

    def open(self):
        if self.connection:
            return False

        connection_class = self.connection_class

        try:
            self.connection = connection_class(
                self.host, self.port,
                timeout=self.timeout,
                local_hostname=self.local_hostname
            )
            self.connection.set_debuglevel(self.debug_level)
            self.connection.starttls(context=ssl._create_unverified_context())

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception as e:
            if not self.fail_silently:
                raise e
            return False