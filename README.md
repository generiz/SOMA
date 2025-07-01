Kon# SOMA - Sistema Organizado de Mensajería y Automatización

SOMA es un sistema modular que combina backend en FastAPI, frontend web moderno y conexión con WhatsApp Cloud API para crear chatbots automatizados con IA, pensados para distintos rubros: ventas, cobros, soporte, promociones y más.

---

## Características

- Panel web moderno (Flutter Web)
- API backend en FastAPI + SQLAlchemy
- Conexión con WhatsApp Business Cloud API
- Respuestas generadas con IA (OpenRouter / OpenAI)
- Gestión de productos, clientes, pedidos y mensajes
- Webhook funcional para recibir y responder mensajes automáticamente

---

## Estructura

```
SOMA/
├── soma_backend/        # API y lógica
│   ├── app/
│   ├── .env             # No se sube
│   ├── .env.example     # Plantilla segura
│   └── soma.db
├── soma_frontend/       # Panel web con HTML/JS
│   └── frontend/
└── README.md
```

---

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/soma.git
cd soma
```

### 2. Crear y configurar `.env` en `soma_backend/`

```env
OPENROUTER_API_KEY=sk-xxxxxx
WHATSAPP_TOKEN=EAAxxxxxx
WHATSAPP_PHONE_ID=1234567890
VERIFY_TOKEN=midetokenpersonal
```

### 3. Instalar dependencias backend

```bash
cd soma_backend
pip install -r requirements.txt
```

### 4. Iniciar backend

```bash
uvicorn app.main:app --reload
```

---

## NGROK para pruebas con WhatsApp

```bash
ngrok http 8000
```

Usar la URL generada como Webhook en Facebook Developer Console.

---

## Pendiente / Roadmap

- Panel multiusuario con configuración personalizada
- Selección de modelo IA y prompt dinámico
- Plantillas personalizadas por negocio
- Módulo de reportes y estadísticas
- Integración con pasarelas de pago

---

## Licencia

MIT © 2025 - Nicolás Pintos
