# Generated by Django 3.1.3 on 2020-12-22 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booksapp', '0002_booksinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BooksImgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(default='default.png', max_length=255)),
                ('image_path', models.CharField(default='upload/media/books/', max_length=255)),
                ('douban_url', models.CharField(blank=True, max_length=255, null=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='booksapp.booksinfo')),
            ],
        ),
    ]
