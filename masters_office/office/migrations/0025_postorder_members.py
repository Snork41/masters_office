# Generated by Django 4.2.6 on 2023-11-08 18:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("office", "0024_postorder"),
    ]

    operations = [
        migrations.AddField(
            model_name="postorder",
            name="members",
            field=models.ManyToManyField(
                related_name="post_order_brigade",
                to="office.personal",
                verbose_name="Члены бригады",
            ),
        ),
    ]