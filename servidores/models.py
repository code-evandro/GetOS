from django.db import models
from setores.models import Setor

class Servidor(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)  # Ramal já vem pelo setor

    def __str__(self):
        return self.nome
