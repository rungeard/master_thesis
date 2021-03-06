# Generated by Django 4.0.2 on 2022-02-24 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('my_app', '0005_remove_nasa_tlx_ar_effort_tally_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SUS_AR',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('question1', models.SmallIntegerField(null=True)),
                ('question2', models.SmallIntegerField(null=True)),
                ('question3', models.SmallIntegerField(null=True)),
                ('question4', models.SmallIntegerField(null=True)),
                ('question5', models.SmallIntegerField(null=True)),
                ('question6', models.SmallIntegerField(null=True)),
                ('question7', models.SmallIntegerField(null=True)),
                ('question8', models.SmallIntegerField(null=True)),
                ('question9', models.SmallIntegerField(null=True)),
                ('question10', models.SmallIntegerField(null=True)),
            ],
        ),
    ]
