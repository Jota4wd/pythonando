# template.py
from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).resolve().parent.parent))

from model.passwords import Password
from views.password_views import FernetHasher

def save_password():
    try:
        passwords = Password.get()
        if not passwords:
            key, path = FernetHasher.create_key(archive=True)
            print('\nSua chave foi criada. ATENÇÃO: Guarde-a em local seguro!')
            print(f'Chave: {key.decode("utf-8")}')
            if path:
                print(f'Chave salva em: {path}')
        else:
            key = input('Digite sua chave de criptografia: ').strip()
            if not key:
                print("A chave não pode estar vazia")
                return

        domain = input('Domínio: ').strip()
        password = input('Senha: ').strip()

        if not domain or not password:
            print("Domínio e senha não podem estar vazios")
            return

        fernet = FernetHasher(key if isinstance(key, bytes) else key.encode())
        encrypted_password = fernet.encrypt(password).decode('utf-8')

        password_obj = Password(domain=domain, password=encrypted_password)
        password_obj.save()
        print("\nSenha salva com sucesso!")

    except Exception as e:
        print(f"\nErro ao salvar senha: {e}")

def view_password():
    try:
        domain = input('Domínio: ').strip()
        key = input('Digite sua chave de criptografia: ').strip()

        if not domain or not key:
            print("Domínio e chave não podem estar vazios")
            return

        try:
            fernet = FernetHasher(key.encode())
        except Exception:
            print("Chave inválida. Certifique-se de usar a chave correta.")
            return

        data = Password.get()

        found = False
        for entry in data:
            if domain.lower() in entry['domain'].lower():
                decrypted = fernet.decrypt(entry['password'])
                if decrypted != 'Token inválido':
                    print(f'\nDomínio: {entry["domain"]}')
                    print(f'Senha: {decrypted}')
                    found = True
                else:
                    print("\nChave incorreta para este domínio.")
                    return

        if not found:
            print('\nNenhuma senha encontrada para esse domínio.')

    except Exception as e:
        print(f"\nErro ao recuperar senha: {e}")

def main():
    while True:
        print("\n=== Menu ===")
        print("1 - Salvar nova senha")
        print("2 - Visualizar senha")
        print("3 - Sair")

        action = input("\nEscolha uma opção: ").strip()

        if action == "1":
            save_password()
        elif action == "2":
            view_password()
        elif action == "3":
            print("\nEncerrando programa...")
            break
        else:
            print("\nOpção inválida!")
