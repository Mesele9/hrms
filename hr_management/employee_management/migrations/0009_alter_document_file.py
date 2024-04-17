# Generated by Django 4.2.11 on 2024-04-17 02:47

from django.db import migrations, models
import employee_management.utils


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0008_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=employee_management.utils.document_upload_to),
        ),
    ]