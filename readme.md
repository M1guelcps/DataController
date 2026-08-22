backend/
│
├── app/
│   ├── api/          # Onde ficarão as rotas (endpoints HTTP)
│   ├── core/         # Configurações gerais do sistema
│   ├── domain/       # Nossos modelos de dados
│   ├── services/     # Onde ficam as regras de negócio
│   ├── repositories/ # Onde ficam as chamadas para o banco de dados
│   └── main.py       # Ponto de partida da nossa API
│
└── requirements.txt  # Lista de dependências (pip freeze > requirements.txt)