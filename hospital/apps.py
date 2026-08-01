from django.apps import AppConfig
import os


class HospitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital'

    # register signals
    def ready(self):
        import hospital.signals

        # Vercel bundles SQLite on a read-only filesystem. Authentication can
        # still use signed-cookie sessions, but Django's default last_login
        # receiver must not attempt to update the bundled database.
        if os.environ.get('VERCEL'):
            from django.contrib.auth.signals import user_logged_in

            user_logged_in.disconnect(dispatch_uid='update_last_login')
