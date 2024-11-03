from django.contrib import admin
from ninja import ModelSchema, Schema, Schema
from .models import Categorias, Livros

# Register your models here.
admin.site.register(Categorias)
admin.site.register(Livros)

class LivroSchema(ModelSchema):
    class Meta:
       model = Livros
       fields = ['nome', 'streaming', 'categorias']


@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Livros)
class LivrosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'streaming', 'nota', 'get_categorias')
    list_filter = ('streaming', 'categorias')
    search_fields = ('nome', 'comentarios')
    filter_horizontal = ('categorias',)

    def get_categorias(self, obj):
        return ", ".join([categoria.nome for categoria in obj.categorias.all()])
    get_categorias.short_description = 'Categorias'
