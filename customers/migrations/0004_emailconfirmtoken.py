# Generated by Django 4.1 on 2022-08-13 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_alter_user_patronymic'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfirmToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='токен')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользоватлеь')),
            ],
            options={
                'verbose_name': 'Токен подтверждения email',
                'verbose_name_plural': 'Токены подтверждения email',
            },
        ),
    ]
