# Generated by Django 3.2.5 on 2021-07-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
