# Generated by Django 2.1.2 on 2018-11-04 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_image', models.CharField(max_length=1000)),
                ('article_title', models.CharField(max_length=5000)),
                ('article_description', models.CharField(max_length=5000)),
                ('article_url', models.CharField(max_length=5000)),
                ('article_time', models.CharField(max_length=50)),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
