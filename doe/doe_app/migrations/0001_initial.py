# Generated by Django 3.2.7 on 2021-10-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('headers', models.TextField()),
                ('types', models.TextField()),
                ('data', models.TextField()),
            ],
        ),
    ]
