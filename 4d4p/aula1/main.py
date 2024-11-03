# main.py
import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao sys.path de forma mais robusta
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from templates.template import main as template_main

def main():
    try:
        print("=== Gerenciador de Senhas ===")
        template_main()
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        print("\nFim da execução")

if __name__ == '__main__':
    main()
