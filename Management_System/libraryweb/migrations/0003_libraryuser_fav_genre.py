# Generated by Django 4.2.4 on 2024-11-29 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryweb', '0002_libraryuser_delete_libnumcounter_alter_rating_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryuser',
            name='fav_genre',
            field=models.TextField(blank=True, help_text='Favorite genres, separated by commas.', null=True),
        ),
    ]
