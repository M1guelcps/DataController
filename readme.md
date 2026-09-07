## 📁 Estrutura do Backend

O backend é organizado seguindo uma arquitetura em camadas, separando responsabilidades e facilitando a manutenção, testes e evolução da aplicação.

```text
backend/
│
├── app/
│   │
│   ├── api/
│   │   └── # Endpoints HTTP, rotas e controllers da aplicação
│   │
│   ├── core/
│   │   └── # Configurações, variáveis de ambiente, segurança e autenticação
│   │
│   ├── domain/
│   │   └── # Entidades, modelos e regras relacionadas ao domínio
│   │
│   ├── services/
│   │   └── # Regras de negócio e lógica da aplicação
│   │
│   ├── repositories/
│   │   └── # Acesso, consulta e persistência dos dados no banco
│   │
│   └── main.py
│       # Ponto de entrada da aplicação
│
└── requirements.txt
    # Dependências Python do projeto
```

### 🧩 Responsabilidade das camadas

| Diretório          | Responsabilidade                                                            |
| ------------------ | --------------------------------------------------------------------------- |
| `api/`             | Define as rotas HTTP e recebe as requisições da aplicação.                  |
| `core/`            | Centraliza configurações, segurança, autenticação e variáveis de ambiente.  |
| `domain/`          | Contém as entidades e modelos que representam o domínio da aplicação.       |
| `services/`        | Implementa as regras de negócio e coordena as operações da aplicação.       |
| `repositories/`    | Responsável pela comunicação com o banco de dados e persistência dos dados. |
| `main.py`          | Inicializa a aplicação e registra as configurações e rotas necessárias.     |
| `requirements.txt` | Lista as dependências necessárias para executar o backend.                  |

### 🔄 Fluxo da aplicação

De forma simplificada, uma requisição segue o fluxo:

```text
Cliente
   │
   ▼
 API / Rotas
   │
   ▼
 Services
   │
   ▼
 Repositories
   │
   ▼
 Banco de Dados
```

O objetivo dessa separação é evitar que regras de negócio, acesso ao banco e comunicação HTTP fiquem misturados, tornando o projeto mais organizado, testável e escalável.
