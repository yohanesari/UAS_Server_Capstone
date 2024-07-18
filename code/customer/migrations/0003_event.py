# Generated by Django 5.0.3 on 2024-07-15 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_pricerule_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arguments', models.JSONField()),
                ('body', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('path', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('subject_id', models.IntegerField()),
                ('subject_type', models.CharField(max_length=50)),
                ('verb', models.CharField(max_length=50)),
            ],
        ),
    ]