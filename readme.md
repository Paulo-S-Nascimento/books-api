
# 📚 Books API com Observabilidade

API simples de livros desenvolvida em **Python puro**, sem frameworks, com **monitoramento via Prometheus** e **visualização no Grafana**. Projeto da atividade prática de observabilidade.

---

## 👤 Desenvolvedor

- [Paulo Sergio Nascimento Gomes - 37022263]

---

## 🧠 Objetivo

Construir uma API simples instrumentada com métricas para o **Prometheus**, permitindo análise e acompanhamento no **Grafana**, aplicando conceitos de observabilidade.

---

## 🚀 Funcionalidades da API

- 🔗 **GET /** — Verifica se a API está no ar.
- ❤️ **GET /health** — Verifica o status de saúde da API.
- 📚 **GET /books** — Retorna uma lista de livros.
- 🔍 **GET /books/{id}** — Retorna um livro específico pelo ID.
- ➕ **POST /books** — Adiciona um novo livro (armazenado em memória).
- 📊 **GET /metrics** — Exposição das métricas para o Prometheus.

---

## 📈 Métricas Expostas

- 🔢 **Total de requisições** (por método e endpoint).
- ⏱️ **Tempo de resposta (latência)** por endpoint.
- ❌ **Total de erros** por endpoint.

---

## 🐳 Arquitetura com Docker Compose

O ambiente Docker Compose é composto por:

- ⚙️ **API** — Aplicação Python.
- 📥 **Prometheus** — Coleta de métricas.
- 📊 **Grafana** — Dashboard para visualização dos dados.

---

## 🗂️ Estrutura do Projeto

```
📁 ci_cd/
├── api/
│   └── main.py
├── prometheus/
│   └── prometheus.yml
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

- Python + prometheus_client
- Prometheus
- Grafana
- Docker + Docker Compose

---

## ▶️ Como Executar

1. Suba os containers:

```bash
docker-compose up --build
```

2. Acesse os serviços:

- API: [http://localhost:8000](http://localhost:8000)
- Métricas: [http://localhost:8000/metrics](http://localhost:8000/metrics)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)  
  (Login: **admin**, Senha: **admin**)

---