# Generated by Django 2.1.2 on 2018-11-10 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20181110_0546'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, default='Ibadan', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, default='Nigeria', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='organization',
            field=models.CharField(blank=True, default='IIRO', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='08068302532', max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='archivos', verbose_name='Profile Picture'),
        ),
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, default='www.wyhh.net'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='www.wyhh.net'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, default='current location', max_length=30),
        ),
    ]