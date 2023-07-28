from django.apps import AppConfig


class ArticlePanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'article_panel'

    verbose_name = 'Панель редактирования статей'
