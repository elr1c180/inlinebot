from django.db import models

# Create your models here.
class Article(models.Model):
    media = models.ManyToManyField('Photo',verbose_name='Медиа статьи', null=True, blank=True)
    title = models.CharField('Заголовок статьи', max_length=250)
    tags = models.CharField('Теги статьи(через запятую)', max_length=50)
    text = models.TextField('Основной текст статьи', max_length=100000)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
    
    def __str__(self):
        return self.title

class Photo(models.Model):
    image = models.FileField(upload_to='')