# Generated by Django 3.2.5 on 2024-07-25 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20240724_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
        migrations.AddField(
            model_name='vote',
            name='choices',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.choice'),
        ),
    ]
