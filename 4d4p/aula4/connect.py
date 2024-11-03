import requests
from typing import List, Dict, Any

def get_livros() -> List[Dict[str, Any]]:
    """
    Obtém a lista de livros da API.
    
    Returns:
        List[Dict[str, Any]]: Lista de livros ou lista vazia em caso de erro
    """
    try:
        response = requests.get('http://127.0.0.1:8000/api/livros/')
        response.raise_for_status()  # Levanta uma exceção para status codes de erro
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao obter livros: {e}")
        return []

def get_livro_by_id(livro_id: int) -> Dict[str, Any]:
    """
    Obtém um livro específico pelo ID.
    
    Args:
        livro_id (int): ID do livro

    Returns:
        Dict[str, Any]: Dados do livro ou dicionário vazio em caso de erro
    """
    try:
        response = requests.get(f'http://127.0.0.1:8000/api/livros/{livro_id}/')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao obter livro {livro_id}: {e}")
        return {}

def create_livro(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cria um novo livro.
    
    Args:
        data (Dict[str, Any]): Dados do livro a ser criado

    Returns:
        Dict[str, Any]: Dados do livro criado ou dicionário vazio em caso de erro
    """
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/livros/',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao criar livro: {e}")
        return {}

def update_livro(livro_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Atualiza um livro existente.
    
    Args:
        livro_id (int): ID do livro a ser atualizado
        data (Dict[str, Any]): Novos dados do livro

    Returns:
        Dict[str, Any]: Dados atualizados do livro ou dicionário vazio em caso de erro
    """
    try:
        response = requests.put(
            f'http://127.0.0.1:8000/api/livros/{livro_id}/',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao atualizar livro {livro_id}: {e}")
        return {}

def delete_livro(livro_id: int) -> bool:
    """
    Remove um livro.
    
    Args:
        livro_id (int): ID do livro a ser removido

    Returns:
        bool: True se o livro foi removido com sucesso, False caso contrário
    """
    try:
        response = requests.delete(f'http://127.0.0.1:8000/api/livros/{livro_id}/')
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Erro ao deletar livro {livro_id}: {e}")
        return False