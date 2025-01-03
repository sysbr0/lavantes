# Generated by Django 5.1.1 on 2025-01-02 20:26

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
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
                ("name", models.CharField(max_length=100)),
                ("position", models.CharField(blank=True, max_length=100, null=True)),
                ("age", models.IntegerField(blank=True, null=True)),
                (
                    "tc",
                    models.CharField(blank=True, max_length=11, null=True, unique=True),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("created_by", models.IntegerField(blank=True, null=True)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.BooleanField(default=True)),
                ("E_salary", models.IntegerField(default=0)),
                ("balance", models.IntegerField(blank=True, null=True)),
                ("is_working", models.BooleanField(default=True)),
                (
                    "phone",
                    models.CharField(blank=True, max_length=10, null=True, unique=True),
                ),
                (
                    "phone_2",
                    models.CharField(blank=True, max_length=10, null=True, unique=True),
                ),
                (
                    "rfid_address",
                    models.CharField(blank=True, max_length=50, null=True, unique=True),
                ),
                ("isAdmin", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="EmployeePayment",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("note", models.TextField(default="None")),
                (
                    "payment_token",
                    models.UUIDField(editable=False, null=True, unique=True),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="employe.employee",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Salary",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("effective_date", models.DateField(default=django.utils.timezone.now)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="employe.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
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
                ("date", models.DateField()),
                ("status", models.CharField(blank=True, max_length=10, null=True)),
                ("ispyed", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_attandec",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="employe.employee",
                    ),
                ),
            ],
            options={
                "unique_together": {("employee", "date")},
            },
        ),
    ]
