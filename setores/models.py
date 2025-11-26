from django.db import models

class Setor(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=20)
    secretaria = models.CharField(max_length=100)
    ramal = models.CharField(
        max_length=10,
        blank=True,  # permite campo vazio no formulário
        null=True    # permite valor NULL no banco
    )

    def __str__(self):
        return self.nome
