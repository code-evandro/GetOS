

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servidores', '0001_initial'),
        ('setores', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrdemDeServico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ramal', models.CharField(max_length=10)),
                ('tipo', models.CharField(max_length=100)),
                ('data', models.DateField()),
                ('relato', models.TextField()),
                ('finalizada', models.BooleanField(default=False)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('servidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens', to='servidores.servidor')),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens', to='setores.setor')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens', to='ordens.tecnico')),
            ],
        ),
    ]
