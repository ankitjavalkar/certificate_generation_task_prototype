# Generated by Django 4.1.7 on 2023-03-21 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_form', '0002_tasklog_alter_participantdetails_participant_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='task_id',
            field=models.CharField(max_length=255),
        ),
    ]
