# Generated by Django 3.0.5 on 2020-06-26 16:07

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='short_desc',
            field=models.CharField(default='short desc', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
