# passwords.py
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'

    def __init__(self):
        # Garante que o diretório db existe
        self.DB_DIR.mkdir(exist_ok=True)

    def save(self) -> None:
        table_path = self.DB_DIR / f'{self.__class__.__name__}.txt'
        try:
            with open(table_path, 'a') as arq:
                values = [str(value) for value in self.__dict__.values()]
                arq.write("|".join(values) + '\n')
        except IOError as e:
            raise IOError(f"Erro ao salvar no arquivo: {e}")

    @classmethod
    def get(cls) -> List[Dict[str, Any]]:
        table_path = cls.DB_DIR / f'{cls.__name__}.txt'
        try:
            if not table_path.exists():
                return []

            with open(table_path, 'r') as arq:
                lines = arq.readlines()

            results = []
            attributes = list(vars(cls()).keys())

            for line in lines:
                if line.strip():  # Ignora linhas vazias
                    values = line.strip().split('|')
                    result = dict(zip(attributes, values))
                    results.append(result)

            return results
        except IOError as e:
            raise IOError(f"Erro ao ler o arquivo: {e}")

class Password(BaseModel):
    def __init__(self, domain: str = None, password: str = None, expire: bool = False):
        super().__init__()
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()
        self.expire = 1 if expire else 0
