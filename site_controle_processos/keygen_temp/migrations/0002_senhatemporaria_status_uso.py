# Generated by Django 5.1.7 on 2025-04-14 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keygen_temp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='senhatemporaria',
            name='status_uso',
            field=models.TextField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='inativo'),
            preserve_default=False,
        ),
    ]
