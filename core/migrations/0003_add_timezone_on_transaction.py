# Generated by Django 4.2.5 on 2023-10-04 04:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_create_transaction_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="timezone",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]