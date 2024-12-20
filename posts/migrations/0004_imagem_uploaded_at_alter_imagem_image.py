# Generated by Django 5.1.2 on 2024-12-08 12:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_rename_comentarios_comentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagem',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagem',
            name='image',
            field=models.ImageField(upload_to='post_images/'),
        ),
    ]
