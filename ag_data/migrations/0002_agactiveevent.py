# Generated by Django 2.2.11 on 2020-04-17 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ag_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AGActiveEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agevent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ag_data.AGEvent')),
            ],
        ),
    ]
