# Generated by Django 3.2.5 on 2021-07-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_exam', '0009_alter_todo_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='due',
            field=models.DateField(),
        ),
    ]
