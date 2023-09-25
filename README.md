# Projeto de Bancos de Dados

## Estrutura do Projeto

```
├── bd                              <- PostgreSQL
    ├── docker-compose.yml          <- Rodar o banco de dados
    ├── docker-entrypoint-initdb.d/ <- Scripts de criação do banco de dados
├── frontend                        <- Frontend típico em Svelte
├── backend                         <- Backend típico em Flask

```

## Rodando o Projeto

### Banco de Dados

Para rodar o banco de dados, basta executar o comando:

```bash
docker-compose up
```

Para reiniciar o banco de dados do absoluto zero, é necessário limpar os volumes do docker:

```bash
docker-compose down --volumes
```

### Frontend

Para rodar o frontend, basta instalar os pacotes necessários:

```bash
cd frontend
npm install
```

E então rodar o projeto:

```bash
npm run dev
```

### Backend

Para rodar o backend, basta instalar os pacotes necessários:

```bash
cd backend
pip install -r requirements.txt
```

E então rodar o projeto:

```bash
python app.py
```
