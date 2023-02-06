# Generated by Django 4.1.6 on 2023-02-06 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O', max_length=1)),
                ('major', models.CharField(default='', max_length=16)),
                ('occupation', models.CharField(choices=[('STU', 'Student'), ('FAC', 'Faculty')], default='STU', max_length=3)),
                ('phone', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Password',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='backbone.user')),
                ('md5_pwd', models.CharField(max_length=32)),
            ],
        ),
    ]
