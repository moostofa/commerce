# Generated by Django 3.2.9 on 2021-11-04 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20211103_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid_count',
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='bid_count',
            field=models.IntegerField(default=0),
        ),
    ]