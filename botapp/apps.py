from django.apps import AppConfig

class SimplechatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'botapp'
    verbose_name = 'Simple Chatbot'
    
    def ready(self):
        """
        Import signals when the app is ready.
        """
        import botapp.signals