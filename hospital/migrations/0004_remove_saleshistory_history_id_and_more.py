# Generated by Django 4.1.7 on 2023-05-13 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_saleshistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleshistory',
            name='history_id',
        ),
        migrations.AlterField(
            model_name='saleshistory',
            name='content',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='saleshistory',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'ACT'), (2, 'BEST_CASE'), (3, 'PIPELINE'), (4, 'OPP')], default=1),
        ),
    ]
