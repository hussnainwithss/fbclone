# Generated by Django 3.2.4 on 2021-06-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0011_alter_city_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='education',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='education',
            name='school',
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='organization',
            name='city',
        ),
        migrations.AlterUniqueTogether(
            name='work',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='work',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='education',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='education',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='hometown',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='work',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='work',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Education',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.DeleteModel(
            name='Work',
        ),
    ]
