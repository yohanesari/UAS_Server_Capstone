# Generated by Django 5.0.3 on 2024-07-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='codes_count',
            new_name='usage_count',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='completed_at',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='failed_count',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='imported_count',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='logs',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='price_rule',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='started_at',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='status',
        ),
        migrations.AddField(
            model_name='discount',
            name='code',
            field=models.CharField(choices=[('SUMMERSALE100OFF', 'SUMMERSALE100OFF'), ('SUMMERSALE50OFF', 'SUMMERSALE50OFF'), ('ENDSALE20OFF', 'ENDSALE20OFF'), ('ENDSALE50OFF', 'ENDSALE50OFF')], default='SUMMERSALE100OFF', max_length=100),
        ),
    ]