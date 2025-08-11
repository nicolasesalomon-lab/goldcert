# GoldCert – Sistema de Gestión de Certificaciones

Este proyecto provee una API sencilla en Flask y un frontend en Angular (pendiente).

## Puesta en marcha

1. Copiá `.env.example` a `.env` y ajustá los valores necesarios.
2. Ejecutá:

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:5000` y la base de datos en `localhost:5432`.

## Estructura

```
backend/    API Flask
frontend/   Aplicación Angular (en construcción)
```

## Dependencias principales

- Python 3.11
- Flask
- SQLAlchemy
- PostgreSQL
