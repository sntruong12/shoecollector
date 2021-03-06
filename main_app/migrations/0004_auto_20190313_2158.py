# Generated by Django 2.1.5 on 2019-03-14 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20190313_0317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=280)),
            ],
        ),
        migrations.AlterModelOptions(
            name='cleaning',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='cleaning',
            name='date',
            field=models.DateField(verbose_name='date of last cleaning'),
        ),
    ]
