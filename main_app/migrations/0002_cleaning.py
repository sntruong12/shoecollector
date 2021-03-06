# Generated by Django 2.1.5 on 2019-03-13 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cleaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('part', models.CharField(choices=[('P', 'partially'), ('C', 'completely')], default='P', max_length=1)),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Shoe')),
            ],
        ),
    ]
