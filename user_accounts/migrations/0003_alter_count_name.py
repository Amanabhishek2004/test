# Generated by Django 4.2.7 on 2023-11-11 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_attendance_student_alter_student_name'),
        ('user_accounts', '0002_count_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='count',
            name='name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.student'),
        ),
    ]
