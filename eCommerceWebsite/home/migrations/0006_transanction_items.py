# Generated by Django 5.0.4 on 2024-11-26 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_transanction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transanction',
            name='items',
            field=models.JSONField(default={'demo': 'demo'}),
        ),
    ]