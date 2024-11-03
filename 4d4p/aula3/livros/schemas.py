from ninja import ModelSchema, Schema
from typing import List, Optional
from .models import Livros, Categorias

class CategoriaSchema(ModelSchema):
    class Meta:
        model = Categorias
        fields = ['id', 'nome']

class LivroSchema(ModelSchema):
    categorias: List[int]

    class Meta:
        model = Livros
        fields = ['nome', 'streaming', 'categorias']

class LivrosViewSchema(ModelSchema):
    categorias: List[CategoriaSchema]

    class Meta:
        model = Livros
        fields = ['id', 'nome', 'streaming', 'categorias', 'nota', 'comentarios', 'criado_em', 'atualizado_em']

class AvaliacaoSchema(ModelSchema):
    nota: Optional[int]
    comentarios: Optional[str]

    class Meta:
        model = Livros
        fields = ['nota', 'comentarios']

class FiltrosSortear(Schema):
    nota_minima: Optional[int] = None
    categorias: Optional[int] = None
    reler: bool = False
