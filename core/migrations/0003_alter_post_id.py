# Generated by Django 4.1.5 on 2023-02-05 15:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]