# Generated by Django 2.1.7 on 2019-05-06 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_auto_20190506_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ctfsubmit',
            old_name='submit_subject',
            new_name='submit_ctf',
        ),
    ]