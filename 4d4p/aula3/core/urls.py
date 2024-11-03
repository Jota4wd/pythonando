from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from livros.api import livros_router

api = NinjaAPI(
    title="API de Livros",
    version="1.0.0",
    description="API para gerenciamento de livros e suas categorias",
)

# Registra as rotas
api.add_router("/livros/", livros_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  # todas as rotas da API estarão sob /api/
]
