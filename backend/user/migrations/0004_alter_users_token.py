# Generated by Django 5.1.2 on 2024-11-24 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_users_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Token'),
        ),
    ]
