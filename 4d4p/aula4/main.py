import flet as ft
import requests
from connect import get_livros, get_livro_by_id, create_livro, update_livro, delete_livro
from urllib.parse import urlparse, parse_qs
from functools import partial

def main(page: ft.Page):
    page.title = "Cadastro App"
    page.window_width = 400

    # Definindo variáveis globais
    nome_input = ft.TextField(label="Nome do Produto", text_align=ft.TextAlign.LEFT)
    streaming_select = ft.Dropdown(
        options=[
            ft.dropdown.Option("AK", text="Amazon Kindle"),
            ft.dropdown.Option("F", text="Físico"),
        ],
        label="Selecione a streaming"
    )
    lista_livros = ft.ListView()

    def home_page():
        page.views.append(
            ft.View(
                "/",
                controls=[
                    nome_input,
                    streaming_select,
                    cadastrar_btn,
                    lista_livros
                ]
            )
        )

    def cadastrar(e):
        if not nome_input.value or not streaming_select.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return

        data = {
            'nome': nome_input.value,
            'streaming': streaming_select.value,
            'categorias': []  # TODO: DESENVOLVER AS CATEGORIAS
        }

        try:
            response = requests.post('http://127.0.0.1:8000/api/livros/', json=data)
            if response.status_code == 200:
                nome_input.value = ""
                streaming_select.value = None
                page.snack_bar = ft.SnackBar(ft.Text("Livro cadastrado com sucesso!"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar livro."))
            page.snack_bar.open = True
            carregar_livros()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro de conexão: {ex}"))
            page.snack_bar.open = True
        page.update()

    cadastrar_btn = ft.ElevatedButton("Cadastrar", on_click=cadastrar)

    def carregar_livros():
        lista_livros.controls.clear()
        try:
            livros = get_livros()
            for livro in livros:
                lista_livros.controls.append(
                    ft.Container(
                        ft.Text(livro['nome']),
                        bgcolor=ft.colors.BLACK12,
                        padding=15,
                        alignment=ft.alignment.center,
                        margin=3,
                        border_radius=10,
                        on_click=lambda e, livro_id=livro["id"]: page.go(f"/review?id={livro_id}")
                    )
                )
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar livros: {ex}"))
            page.snack_bar.open = True
        page.update()

    def review_page(livro_id):
        if not livro_id:
            page.go("/")
            return

        nota_input = ft.TextField(
            label="Nota (inteiro)", 
            text_align=ft.TextAlign.LEFT, 
            value="0", 
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        comentario_input = ft.TextField(
            label="Comentário", 
            multiline=True, 
            expand=True
        )

        def avaliar(e):
            try:
                nota = int(nota_input.value)
                if not (0 <= nota <= 10):
                    raise ValueError("A nota deve estar entre 0 e 10")
                
                data = {
                    'nota': nota,
                    'comentarios': comentario_input.value
                }

                response = requests.put(f'http://127.0.0.1:8000/api/livros/{livro_id}', json=data)
                if response.status_code == 200:
                    page.snack_bar = ft.SnackBar(ft.Text("Avaliação enviada com sucesso!"))
                    page.go("/")
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Erro ao enviar a avaliação."))
            except ValueError as ve:
                page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro de conexão: {ex}"))
            
            page.snack_bar.open = True
            page.update()

        avaliar_btn = ft.ElevatedButton("Avaliar", on_click=avaliar)
        voltar_btn = ft.ElevatedButton("Voltar", on_click=lambda _: page.go('/'))

        page.views.append(
            ft.View(
                "/review",
                controls=[
                    ft.Text("Review Page", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Detalhes do livro com ID: {livro_id}"),
                    nota_input,
                    comentario_input,
                    ft.Row([avaliar_btn, voltar_btn]),
                ]
            )
        )

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            home_page()
        elif page.route.startswith("/review"):
            parsed_url = urlparse(page.route)
            query_params = parse_qs(parsed_url.query)
            livro_id = query_params.get('id', [None])[0]
            review_page(livro_id)

        page.update()

    page.on_route_change = route_change
    carregar_livros()
    page.go('/')

ft.app(target=main)