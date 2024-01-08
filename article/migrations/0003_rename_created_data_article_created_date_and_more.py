# Generated by Django 4.2.7 on 2023-11-24 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_created_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='created_data',
            new_name='created_date',
        ),
        migrations.AddField(
            model_name='article',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
