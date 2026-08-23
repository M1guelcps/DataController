import openpyxl
from io import BytesIO
from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository


class RelatorioService:

    @staticmethod
    def gerar_relatorio_clientes(db: Session) -> BytesIO:
        # 1. Busca os dados no banco usando o Repositório existente (Reaproveitamento)
        clientes = ClienteRepository.buscar_todos(db)

        print(f"Quantidade de clientes: {len(clientes)}")


        # 2. Carrega o modelo visual da empresa
        caminho_template = "assets/template_clientes.xlsx"

        try:
            workbook = openpyxl.load_workbook(caminho_template)
            # Pega a aba ativa (ou você poderia usar workbook["NomeDaAba"])
            planilha = workbook["clientes"]
        except FileNotFoundError:
            raise ValueError("Template de relatório não encontrado no servidor.")

        # 3. Preenche os dados a partir da linha 8
        linha_atual = 9
        for cliente in clientes:
            # openpyxl usa 1-index (linha 1, coluna 1 = A1)
            planilha.cell(row=linha_atual, column=4, value=cliente.id)
            planilha.cell(row=linha_atual, column=1, value=cliente.nome)
            planilha.cell(row=linha_atual, column=3, value=cliente.cnpj)
            planilha.cell(row=linha_atual, column=2, value=cliente.email)
            linha_atual += 1

        # 4. Salva o arquivo em memória (RAM), não no disco rígido!
        arquivo_em_memoria = BytesIO()
        workbook.save(arquivo_em_memoria)

        # Volta o "cursor" da memória para o começo do arquivo para envio pela rede
        arquivo_em_memoria.seek(0)

        return arquivo_em_memoria