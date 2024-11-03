# password_views.py
import string
import secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from typing import Union, Tuple, Optional

class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_letters + string.digits
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys'

    def __init__(self, key: Union[str, bytes]):
        self.KEY_DIR.mkdir(exist_ok=True)

        try:
            if isinstance(key, str):
                key = key.encode()
            self.fernet = Fernet(key)
        except Exception as e:
            raise ValueError(f"Chave inválida: {e}")

    @classmethod
    def _get_random_string(cls, length: int = 25) -> str:
        return ''.join(secrets.choice(cls.RANDOM_STRING_CHARS) for _ in range(length))

    @classmethod
    def create_key(cls, archive: bool = False) -> Tuple[bytes, Optional[Path]]:
        try:
            key = Fernet.generate_key()
            if archive:
                return key, cls.archive_key(key)
            return key, None
        except Exception as e:
            raise RuntimeError(f"Erro ao criar chave: {e}")

    @classmethod
    def archive_key(cls, key: bytes) -> Path:
        try:
            file_name = f'key_{cls._get_random_string(5)}.key'
            file_path = cls.KEY_DIR / file_name

            while file_path.exists():
                file_name = f'key_{cls._get_random_string(5)}.key'
                file_path = cls.KEY_DIR / file_name

            with open(file_path, 'wb') as f:
                f.write(key)

            return file_path
        except Exception as e:
            raise IOError(f"Erro ao arquivar chave: {e}")

    def encrypt(self, value: Union[str, bytes]) -> bytes:
        try:
            if isinstance(value, str):
                value = value.encode('utf-8')
            return self.fernet.encrypt(value)
        except Exception as e:
            raise RuntimeError(f"Erro na criptografia: {e}")

    def decrypt(self, value: Union[str, bytes]) -> str:
        try:
            if isinstance(value, str):
                value = value.encode('utf-8')
            return self.fernet.decrypt(value).decode()
        except InvalidToken:
            return 'Token inválido'
        except Exception as e:
            return 'Token inválido'
