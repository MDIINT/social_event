# Generated by Django 3.0.7 on 2020-07-06 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_submit_cancel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submit',
            old_name='Submitter',
            new_name='submitted_user',
        ),
    ]