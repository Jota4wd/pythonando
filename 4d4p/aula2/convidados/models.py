from django.db import models
from noivos.models import Convidados as ConvidadosNoivos

class Acompanhantes(models.Model):
    convidado = models.ForeignKey(ConvidadosNoivos, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome