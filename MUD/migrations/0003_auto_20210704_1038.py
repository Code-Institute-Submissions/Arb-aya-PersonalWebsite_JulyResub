# Generated by Django 3.2 on 2021-07-04 09:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MUD', '0002_character_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, max_length=1204, null=True, upload_to='items')),
                ('item_type', models.CharField(choices=[('weapon', 'Weapon'), ('armour', 'Armour'), ('shield', 'Shield')], default='shield', max_length=50)),
                ('slot', models.CharField(choices=[('head', 'Head'), ('body', 'Body'), ('main_hand', 'Main Hand'), ('off_hand', 'Off Hand'), ('both_hands', 'Both Hands')], default='off_hand', max_length=50)),
                ('width', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('height', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField()),
                ('cost', models.DecimalField(decimal_places=0, max_digits=4)),
                ('rarity', models.CharField(choices=[('common', 'Common'), ('unusual', 'Unusual'), ('rare', 'Rare'), ('epic', 'Epic')], default='common', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='gold',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='character',
            name='inventory_size',
            field=models.IntegerField(default=4, validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AddField(
            model_name='character',
            name='points',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='agility',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='dexterity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='hp',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='mp',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='character',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='character',
            name='strength',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.CreateModel(
            name='ItemSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastSpaceIndex', models.CharField(default='-1', max_length=2)),
                ('currentSpaceIndex', models.CharField(default='-1', max_length=2)),
                ('equipped', models.BooleanField(default=False)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='items', to='MUD.character')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', related_query_name='settings', to='MUD.item')),
            ],
        ),
    ]