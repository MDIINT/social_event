# Generated by Django 3.0.7 on 2020-07-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventing', '0007_auto_20200701_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='trailer',
            field=models.FileField(blank=True, null=True, upload_to='event_trailers', verbose_name='پیش نمایش'),
        ),
    ]
