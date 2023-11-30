# Generated by Django 4.2.5 on 2023-11-16 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_user_birthday_user_email_user_introduce_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="brace_total",
            field=models.IntegerField(default=0, null=True, verbose_name="牙套总数量"),
        ),
        migrations.AddField(
            model_name="user",
            name="brace_used",
            field=models.IntegerField(default=0, null=True, verbose_name="已佩戴牙套数量"),
        ),
        migrations.AddField(
            model_name="user",
            name="followup_date",
            field=models.DateField(blank=True, null=True, verbose_name="下次复诊日期"),
        ),
    ]
