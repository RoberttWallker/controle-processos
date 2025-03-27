# Generated by Django 5.1.7 on 2025-03-27 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SenhaTemporaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palavra_secreta', models.CharField(max_length=100)),
                ('chave_temporal', models.CharField(max_length=255, unique=True)),
                ('validade', models.DateTimeField()),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
