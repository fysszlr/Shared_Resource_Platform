# Generated by Django 5.0.7 on 2024-12-02 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_answers_creatorid_alter_answers_rewardid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='commentId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
