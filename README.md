# PINGME - Chat en Red con WebSockets y Flet  

## 📝 Descripción del Proyecto  
**PINGME** es una aplicación de chat en red que utiliza:  
- **WebSockets** para comunicación en tiempo real.  
- **Flet** para la interfaz gráfica moderna.  

### Estructura del Proyecto  
```plaintext
PINGME/
├── core/                # Lógica central de la aplicación
│   ├── controller/      # Controladores para manejar la lógica de 
│   ├── models/          # Modelos de datos
│   ├── state/           # Estado global de la aplicación
│   ├── views/           # Vistas/interfaz de usuario
|   └── __init__.py      # Archivo de inicialización del paquete
├── config.py            # Configuración de la aplicación
├── main.py              # Punto de entrada principal
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

## ⚙️ Requisitos Previos

    Python 3.11 o superior.

## 🛠️ Instalación con Entornos Virtuales

> ### 1. Usando venv

#### Crear entorno virtual
`python -m venv venv`

#### Activar entorno (Linux/Mac)
`source venv/bin/activate`

#### Activar entorno (Windows)
`.\venv\Scripts\activate`

#### Instalar dependencias
`pip install -r requirements.txt`

> ### 2. Usando virtualenvwrapper

#### Instalar virtualenv si no está instalado
`pip install virtualenvwrapper`

#### Crear entorno virtual
`mkvirtualenv pingme
`

#### Activar entorno
`workon pingme
`

#### Instalar dependencias
`pip install -r requirements.txt
`
> ### 3. Usando conda (Anaconda/Miniconda)

#### Crear entorno virtual
`conda create --name pingme python=3.11.10
`
#### Activar entorno
`conda activate pingme
`
#### Instalar dependencias
`pip install -r requirements.txt
`

## 🚀 Ejecutar la Aplicación

`python main.py`

La aplicación iniciará:

 - Servidor WebSocket.

 - Interfaz gráfica Flet.

## ⚡ Configuración

Ajusta parámetros de conexión y otros en:

    ⚙️ config.py

## ✨ Características

    💬 Chat en tiempo real con WebSockets.

    🎨 Interfaz gráfica moderna con Flet.

    👥 Soporte para múltiples usuarios.

    🔔 Notificaciones en tiempo real.

    📜 Historial de mensajes con DB.

    📝 Logs de los errores en la appicación
