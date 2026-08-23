import pandas as pd
from io import BytesIO
from typing import List
from app.domain.cliente_schema import ClienteCreate


class ExcelImportService:

    @staticmethod
    def extrair_clientes(file_content: bytes) -> List[ClienteCreate]:
        # 1. Carrega o arquivo em memória usando o Pandas
        try:
            df = pd.read_excel(BytesIO(file_content),engine="pyxlsb")
        except Exception:
            raise ValueError("Não foi possível ler o arquivo. Verifique se é um Excel válido.")

        # 2. Padroniza as colunas (tudo minúsculo e sem espaços) para evitar erros bobos do usuário
        df.columns = [str(col).strip().lower() for col in df.columns]

        # 3. Valida se a planilha tem o que precisamos
        colunas_obrigatorias = ['nome', 'cnpj', 'email']
        for col in colunas_obrigatorias:
            if col not in df.columns:
                raise ValueError(f"O arquivo Excel precisa ter uma coluna chamada '{col}'.")

        # 4. Trata valores nulos (transforma NaN em strings vazias)
        df = df.fillna("")

        # 5. Converte as linhas do Excel em objetos Pydantic validados
        clientes_extraidos = []
        for index, row in df.iterrows():
            # Ignora linhas totalmente vazias
            if not row['nome'] and not row['cnpj']:
                continue

            cliente = ClienteCreate(
                nome=str(row['nome']),
                cnpj=str(row['cnpj']),
                email=str(row['email'])
            )
            clientes_extraidos.append(cliente)

        return clientes_extraidos