from django.apps import AppConfig
import os


class ShortenerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shortener"

    def ready(self):
        # Preventing running ready() function twice
        run_once = os.environ.get("CMDLINERUNNER_RUN_ONCE")
        if run_once is not None:
            return
        os.environ["CMDLINERUNNER_RUN_ONCE"] = "True"
        print("Starting Expired URL Deletion Job ...")
        from shortener.backends import scheduler

        scheduler.start()
