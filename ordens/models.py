from django.db import models
from django.contrib.auth.models import User
from servidores.models import Servidor
from setores.models import Setor

class Tecnico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class OrdemDeServico(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE, related_name='ordens')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='ordens')
    ramal = models.CharField(max_length=10)  # ← Preenchido automaticamente pelo setor
    tipo = models.CharField(max_length=100)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='ordens')
    data = models.DateField()
    relato = models.TextField()
    comentario_tecnico = models.TextField(blank=True, null=True)  # ← Novo campo aqui
    finalizada = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OS #{self.id} - {self.servidor.nome}"
