# Generated by Django 3.1.4 on 2021-02-28 08:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0011_auto_20210228_0734'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productlike',
            options={'verbose_name': 'CommentLike', 'verbose_name_plural': 'CommentLikes'},
        ),
        migrations.AlterUniqueTogether(
            name='productlike',
            unique_together={('user', 'product')},
        ),
    ]