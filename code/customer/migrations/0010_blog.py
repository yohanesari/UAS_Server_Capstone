# Generated by Django 5.0.3 on 2024-07-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentable', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('feedburner', models.URLField(blank=True, null=True)),
                ('feedburner_location', models.URLField(blank=True, null=True)),
                ('handle', models.CharField(max_length=255)),
                ('tags', models.CharField(max_length=255)),
                ('template_suffix', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin_graphql_api_id', models.CharField(max_length=255)),
            ],
        ),
    ]
