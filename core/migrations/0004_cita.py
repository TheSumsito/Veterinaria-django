# Generated by Django 3.0 on 2020-01-31 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_delete_cita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('IdCita', models.IntegerField(primary_key=True, serialize=False)),
                ('Descripcion', models.CharField(max_length=50)),
                ('Fecha', models.DateField()),
                ('Hora', models.TimeField()),
                ('Estado', models.BooleanField()),
                ('IdMascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Mascota')),
                ('IdTipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TipoConsulta')),
            ],
        ),
    ]
