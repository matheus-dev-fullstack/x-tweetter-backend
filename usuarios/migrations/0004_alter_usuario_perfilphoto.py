# Generated by Django 5.1.2 on 2024-10-19 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_usuario_perfilphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='perfilPhoto',
            field=models.ImageField(blank=True, null=True, upload_to='perfilPhoto'),
        ),
    ]