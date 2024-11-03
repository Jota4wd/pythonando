from typing import List, Optional
from ninja import Router, Query
from django.shortcuts import get_object_or_404
from .models import Livros, Categorias
from .schemas import LivroSchema, LivrosViewSchema, AvaliacaoSchema, FiltrosSortear
from django.db.models import Q

livros_router = Router()

@livros_router.get("/", response={200: List[LivrosViewSchema]})
def get_livros(request):
    """Retorna todos os livros cadastrados"""
    livros = Livros.objects.all().prefetch_related('categorias')
    return livros

@livros_router.get("/{livro_id}", response={200: LivrosViewSchema, 404: dict})
def get_livro(request, livro_id: int):
    """Retorna um livro específico pelo ID"""
    try:
        livro = get_object_or_404(Livros, id=livro_id)
        return 200, livro
    except:
        return 404, {"message": "Livro não encontrado"}

@livros_router.post('/', response={201: LivrosViewSchema, 400: dict})
def create_livro(request, livro_schema: LivroSchema):
    """Cria um novo livro"""
    try:
        livro = Livros.objects.create(
            nome=livro_schema.nome,
            streaming=livro_schema.streaming
        )

        for categoria_id in livro_schema.categorias:
            categoria = get_object_or_404(Categorias, id=categoria_id)
            livro.categorias.add(categoria)

        livro.save()
        return 201, livro
    except Exception as e:
        return 400, {"message": f"Erro ao criar livro: {str(e)}"}

@livros_router.put('/{livro_id}', response={200: dict, 404: dict, 400: dict})
def avaliar_livro(request, livro_id: int, avaliacao_schema: AvaliacaoSchema):
    """Avalia um livro existente"""
    try:
        livro = get_object_or_404(Livros, id=livro_id)
        livro.comentarios = avaliacao_schema.comentarios
        livro.nota = avaliacao_schema.nota
        livro.save()
        return 200, {"message": "Avaliação realizada com sucesso"}
    except Livros.DoesNotExist:
        return 404, {"message": "Livro não encontrado"}
    except Exception as e:
        return 400, {"message": f"Erro ao avaliar livro: {str(e)}"}

@livros_router.delete('/{livro_id}', response={200: dict, 404: dict})
def deletar_livro(request, livro_id: int):
    """Remove um livro"""
    try:
        livro = get_object_or_404(Livros, id=livro_id)
        livro.delete()
        return 200, {"message": f"Livro {livro_id} removido com sucesso"}
    except:
        return 404, {"message": "Livro não encontrado"}

@livros_router.get('/sortear/', response={200: LivrosViewSchema, 404: dict})
def sortear_livro(request, filtros: Query[FiltrosSortear]):
    """Sorteia um livro com base nos filtros fornecidos"""
    livros = Livros.objects.all()

    if not filtros.reler:
        livros = livros.filter(nota__isnull=True)
    if filtros.nota_minima:
        livros = livros.filter(nota__gte=filtros.nota_minima)
    if filtros.categorias:
        livros = livros.filter(categorias__id=filtros.categorias)

    livro = livros.order_by('?').first()

    if livro:
        return 200, livro
    return 404, {'message': 'Nenhum livro encontrado com os critérios especificados'}
