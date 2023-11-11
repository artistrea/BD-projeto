Crie seu venv

```bash
python3 -m venv .venv
```

ative-o

```bash
source .venv/bin/activate
```

instale as deps:

```bash
pip install -r requirements.txt
```

## RODE:

```bash
python3 -m flask --app src/app run --debug
```

Ou usando o `dev.sh` criado.

```bash
./dev.sh
```

Talvez ele não esteja funcionando como executável ainda, e neste caso precisa rodar antes de comando anterior

```bash
sudo chmod +x dev.sh
```
