# Generated by Django 4.2.5 on 2023-09-18 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0007_uploadedimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]
