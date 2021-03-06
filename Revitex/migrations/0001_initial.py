# Generated by Django 3.2.5 on 2021-09-04 12:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='centre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default='', max_length=30, unique=True)),
                ('description', models.TextField(default='Pas de description disponible')),
                ('image_pres', models.ImageField(upload_to='')),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=9)),
                ('adresse', models.CharField(default="pas d'adresse", max_length=100)),
                ('likes', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('heure_ouverture', models.TimeField(default='9:00')),
                ('heure_fermeture', models.TimeField(default='17:00')),
            ],
            options={
                'permissions': (('gerer_centre', 'Gérer son centre'),),
            },
        ),
        migrations.CreateModel(
            name='controle_Technique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('controle_techniques', models.CharField(default='Véhicules léger', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=30)),
                ('document', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='email_Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='features_centre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='image_gallerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='num_memoire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='service_centre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='titre_Proprieté',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre_proprieté', models.CharField(default='Véhicules léger', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ville',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('slots_restant', models.IntegerField()),
                ('centre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Revitex.centre')),
                ('controleTechnique', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Revitex.controle_technique')),
                ('gestionnaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Slots',
            },
        ),
        migrations.CreateModel(
            name='randez_vous',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(default=0, unique=True)),
                ('Date', models.DateTimeField(blank=True, null=True)),
                ('état', models.CharField(choices=[('E', 'En attente'), ('V', 'Validé'), ('A', 'Annulé')], default='E', max_length=30)),
                ('GSM', models.CharField(max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Veuillez utiliser le format: '0XXXXXXXXX'.", regex='^0\\d{9,15}$')])),
                ('email', models.EmailField(max_length=254, null=True)),
                ('TitrePropriété', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Revitex.titre_proprieté')),
                ('centre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Revitex.centre')),
                ('controleTechnique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Revitex.controle_technique')),
                ('gestionnaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Randez-vous',
            },
        ),
        migrations.CreateModel(
            name='quota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cota_par_jour', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('centre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Revitex.centre')),
                ('controleTechnique', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Revitex.controle_technique')),
                ('gestionnaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='centre',
            name='Controles_dispo',
            field=models.ManyToManyField(to='Revitex.controle_Technique'),
        ),
        migrations.AddField(
            model_name='centre',
            name='Titre_dispo',
            field=models.ManyToManyField(blank=True, to='Revitex.titre_Proprieté'),
        ),
        migrations.AddField(
            model_name='centre',
            name='features',
            field=models.ManyToManyField(to='Revitex.features_centre'),
        ),
        migrations.AddField(
            model_name='centre',
            name='gestionnaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='centre',
            name='img_gallerie',
            field=models.ManyToManyField(to='Revitex.image_gallerie'),
        ),
        migrations.AddField(
            model_name='centre',
            name='services',
            field=models.ManyToManyField(to='Revitex.service_centre'),
        ),
        migrations.AddField(
            model_name='centre',
            name='ville',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Revitex.ville'),
        ),
        migrations.CreateModel(
            name='Appels_offre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=300)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(default='Pas de description disponible')),
                ('image', models.ImageField(upload_to='')),
                ('popularité', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('document', models.ManyToManyField(to='Revitex.Documents')),
                ('villes', models.ManyToManyField(to='Revitex.ville')),
            ],
        ),
    ]
