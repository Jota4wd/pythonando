from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categorias(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Livros(models.Model):
    FISICO = 'F'
    KINDLE = 'AK'

    STREAMING_CHOICES = [
        (FISICO, 'Físico'),
        (KINDLE, 'Amazon Kindle')
    ]

    nome = models.CharField(max_length=50)
    streaming = models.CharField(
        max_length=2,
        choices=STREAMING_CHOICES,
        default=FISICO
    )
    nota = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    comentarios = models.TextField(null=True, blank=True)
    categorias = models.ManyToManyField(
        Categorias,
        related_name='livros'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome
