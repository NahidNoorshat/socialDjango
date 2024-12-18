# Generated by Django 4.1.5 on 2023-02-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_post_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Likepost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("post_id", models.CharField(max_length=500)),
                ("username", models.CharField(max_length=50)),
            ],
        ),
    ]
