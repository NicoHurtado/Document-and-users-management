# Generated by Django 4.2.4 on 2024-03-26 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doc_management', '0003_alter_estudiante_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='image',
            field=models.ImageField(blank=True, default='Doc_management\\estudiantes\\images\\DSC_1379.JPG', null=True, upload_to='estudiantes/images/'),
        ),
    ]
