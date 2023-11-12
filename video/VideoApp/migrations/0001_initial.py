# Generated by Django 4.2.7 on 2023-11-12 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RenderVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='Статус')),
                ('loadDate', models.DateTimeField(auto_now_add=True)),
                ('renderDate', models.DateTimeField(blank=True, null=True)),
                ('video_author', models.CharField(max_length=255)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos/%Y/%m/%d/')),
            ],
        ),
    ]
