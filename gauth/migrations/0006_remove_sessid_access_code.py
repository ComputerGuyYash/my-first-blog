# Generated by Django 2.2.3 on 2019-07-05 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gauth', '0005_sessid_access_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessid',
            name='access_code',
        ),
    ]