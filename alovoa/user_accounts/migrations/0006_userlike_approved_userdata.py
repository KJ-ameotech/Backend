# Generated by Django 4.2.5 on 2023-09-27 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0005_alter_profilepicture_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlike',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_accounts.uploadedimages')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_accounts.profile')),
            ],
        ),
    ]