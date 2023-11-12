from django.db import models

class RenderVideo(models.Model):
    name = models.CharField(max_length=255) # Название ролика
    status = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Статус', default=0.0) # Статус обработки
    loadDate = models.DateTimeField(auto_now_add=True) # Дата загрузки видео
    renderDate = models.DateTimeField(null=True, blank=True) # Дата оканчания обработки
    video_author = models.CharField(max_length=255) # Человек, загрузившый видео
    video_file = models.FileField(upload_to="videos/%Y/%m/%d/", null=True, blank=True) # Файл видео

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Видео для рендеринга'
        verbose_name_plural = 'Видео для рендеринга'
