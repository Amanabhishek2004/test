# Generated by Django 4.2.7 on 2024-01-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0006_alter_count_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='count',
            name='subject_name',
            field=models.CharField(max_length=25, null=True),
        ),
    ]