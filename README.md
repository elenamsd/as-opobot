# 🤖 Repositorio de un bot de Telegram para las oposiciones

## 🛠️ Configuración del entorno

```bash
python -m venv venv
```

### 💻 Si estás en Linux/macOS:
```bash
source venv/bin/activate
```

### 🖥️ Si estás en Windows:
```bash
.\venv\Scripts\activate
```

## 📦 Instalación de dependencias

### 🚀 Instala Poetry:
```bash
pip install poetry
```

### 📥 Instala las dependencias del proyecto:
```bash
poetry install
```

## 🔑 Variables de entorno

Crea un fichero con las variables de entorno:
```bash
touch .env
```

Incluye dentro las siguientes variables:
```env
API_KEY=""
```

## 🐳 Inicializa la base de datos

```bash
docker build -t opobot-db .
```

```bash
docker run -d \
  --name opobot-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=opobot \
  -p 5432:5432 \
  opobot-db
```

Para más información sobre la base de datos, consulta el [README de la base de datos](docs/db-commands.md).

## ▶️ Ejecución del bot

```bash
python3 main.py
```

Una vez ejecutemos este script, el bot se quedará escuchando:

![alt text](docs/images/main.png)