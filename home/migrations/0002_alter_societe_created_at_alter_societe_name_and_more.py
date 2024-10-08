# Generated by Django 5.1.1 on 2024-09-10 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='societe',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='name',
            field=models.CharField(max_length=150, null=True, unique=True, verbose_name='Nom du Société'),
        ),
        migrations.AlterField(
            model_name='societe',
            name='password',
            field=models.CharField(default='m1234', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='server',
            field=models.CharField(default='Srvi7dsiamb01', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='types',
            field=models.CharField(choices=[('sage100', 'Sage100'), ('x3v1', 'X3V1(AGRI)'), ('x3v2', 'X3V2(SMTP)')], default='sage100', max_length=50),
        ),
        migrations.AlterField(
            model_name='societe',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='user',
            field=models.CharField(default='reader', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='societe',
            name='value',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('societe1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_societe1', to='home.societe')),
                ('societe2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_societe2', to='home.societe')),
                ('tiers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tiers')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.type')),
            ],
        ),
    ]
