

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordens', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemdeservico',
            name='comentario_tecnico',
            field=models.TextField(blank=True, null=True),
        ),
    ]
