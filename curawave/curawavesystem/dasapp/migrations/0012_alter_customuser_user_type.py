# Generated by Django 5.0.2 on 2024-02-21 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dasapp', '0011_appointment_recommendedtest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'admin'), (2, 'doc')], default=1, max_length=50),
        ),
    ]
