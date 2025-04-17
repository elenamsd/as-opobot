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

## ▶️ Ejecución del bot

```bash
python3 main.py
```

Una vez ejecutemos este script, el bot se quedará escuchando:

![alt text](docs/images/main.png)