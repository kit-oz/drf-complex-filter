# Generated by Django 3.1.3 on 2020-11-19 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group1', models.CharField(max_length=10)),
                ('group2', models.CharField(max_length=10)),
                ('integer', models.IntegerField()),
                ('float', models.FloatField()),
                ('date', models.DateField()),
                ('datetime', models.DateTimeField()),
                ('user', models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True)),
            ],
        ),
    ]