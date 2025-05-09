# Generated by Django 5.1.7 on 2025-04-03 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend_site', '0004_compraslentes_loja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compraslentes',
            name='custo_nota_fiscal',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='compraslentes',
            name='custo_site',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='compraslentes',
            name='custo_tabela',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='compraslentes',
            name='data_liberacao_blu',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='compraslentes',
            name='valor_pago',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
