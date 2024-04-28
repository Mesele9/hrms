# Generated by Django 4.2.11 on 2024-04-28 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0013_employee_address_employee_education_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(choices=[('educational_document', 'Educational Document'), ('kebele_id', 'Kebele ID'), ('employment', 'Employement Letter'), ('promotion', 'Promotions Letter'), ('demotion', 'Demotion Letter'), ('first_warning', 'First Warning'), ('second_warning', 'Second Warning'), ('third_warning', 'Third Warning'), ('final_warning', 'Second Warning'), ('termination', 'Termination Letter')], max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='education_level',
            field=models.CharField(blank=True, choices=[('Master', "Master's Degree"), ('Degree', "Bachelor's Degree"), ('Diploma', 'Diploma'), ('Certificate', 'Certificate'), ('Grade', 'Grade')], max_length=20, null=True),
        ),
    ]