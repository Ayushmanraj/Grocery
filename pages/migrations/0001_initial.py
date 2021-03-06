# Generated by Django 3.0 on 2020-08-11 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('photo', models.ImageField(upload_to='photo/')),
                ('points_needed', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
