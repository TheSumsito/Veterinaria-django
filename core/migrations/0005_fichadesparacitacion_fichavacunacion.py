# Generated by Django 3.0 on 2020-02-01 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_cita'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaVacunacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdFicha', models.IntegerField()),
                ('FechaVacuna', models.DateField()),
                ('FechaProxima', models.DateField()),
                ('IdMascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Mascota')),
            ],
        ),
        migrations.CreateModel(
            name='FichaDesparacitacion',
            fields=[
                ('IdFicha', models.IntegerField(primary_key=True, serialize=False)),
                ('FechaDesp', models.DateField()),
                ('Medicamento', models.CharField(max_length=50)),
                ('Dosis', models.CharField(max_length=50)),
                ('FechaProxima', models.DateField()),
                ('IdMascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Mascota')),
            ],
        ),
    ]
