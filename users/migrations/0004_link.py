# Generated by Django 4.0.3 on 2022-04-11 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_carmodel_trim_carmodel_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_link', models.URLField()),
                ('shortened_link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
