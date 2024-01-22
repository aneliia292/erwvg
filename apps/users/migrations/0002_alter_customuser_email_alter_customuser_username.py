# Generated by Django 5.0 on 2024-01-21 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=30, unique=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(max_length=30, verbose_name="Username"),
        ),
    ]