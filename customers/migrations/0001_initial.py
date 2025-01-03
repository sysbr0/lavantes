# Generated by Django 5.1.1 on 2025-01-02 20:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Costomers",
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
                ("name", models.TextField()),
                ("image", models.URLField(blank=True, null=True)),
                ("tex", models.BigIntegerField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("number", models.CharField(max_length=255, null=True)),
                ("is_company", models.BooleanField(default=0)),
                ("company", models.TextField(blank=True, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "token",
                    models.CharField(default=uuid.uuid4, max_length=36, unique=True),
                ),
                (
                    "profile_image",
                    models.ImageField(blank=True, null=True, upload_to="costomers/"),
                ),
                (
                    "balanceTr",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "balanceUsd",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_customers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
    ]
