# Generated by Django 4.2.5 on 2023-09-26 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0004_alter_subscription_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepicture',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
