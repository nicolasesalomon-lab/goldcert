# GoldCert — Sistema de Certificaciones (v1)

Gestión integral de **certificaciones** para Seguridad Eléctrica (SE), Eficiencia Energética (EE), ENACOM e INAL.  
Incluye **backend API** (Flask + PostgreSQL + Alembic) y **frontend** (Vite + React + TypeScript), todo **dockerizado** y listo para desarrollo local en Windows.

---

## ✨ Funcionalidad clave (estado actual)

- **Modelo único de Certificado** para SE/EE/ENACOM/INAL.
- **Ámbito del certificado** (solo SE/EE):
  - `tipo` → *sin* auditoría de fábrica.
  - `marca` → *requiere* auditoría de fábrica **vigente** al emitir **y** para mantener la vigencia (si cae, el certificado pasa a `suspendido`; si vuelve a haber auditoría vigente y el certificado no venció, regresa a `vigente`). ✅
- **No permite superposiciones** de vigencias del mismo certificado. ✅
- **Editar fechas**: se puede ajustar `fecha_vencimiento` al crear y luego corregirla. ✅
- **Estados automáticos** de certificado: `vigente`, `próximo a vencer` (umbrales 30/60/**90**/180/365 días), `vencido`, `suspendido`. ✅
- **Alertas**: in‑app (configurables más adelante). Bloqueos **hard** en acciones críticas; el sistema sugiere crear tareas pero no las crea automáticamente. ✅
- **Wizard guiado** de emisión:
  1) Subida de **test report** (CB/ensayo), etiquetas, manuales, **mapa de modelos**, **declaración de identidad**.
  2) Validación del OCC (IRAM/TÜV/…).
  3) Recepción y carga del **certificado** final.
  4) **Fábrica obligatoria** en todos los certificados; si `marca`, además exige auditoría vigente. ✅
- **DJ (Declaración Jurada)**: generación a partir de plantilla provista (DJC.pdf) y vínculo de modelos. ✅
- **Roles**: `Admin`, `Analista`, `Consulta`. ✅
- **Productos** vinculados a **Proveedor**; Proveedor → N **Fábricas** (0..1 auditoría vigente por fábrica). ✅
- **API documentada** con Swagger UI. ✅

> Nota: Email para alertas queda para etapa siguiente; hoy solo in‑app (configurable luego).

---

## 🧱 Estructura de carpetas (v1)

```
/v1
  backend/
    app/
      routes/          # endpoints Flask
      models/          # SQLAlchemy
      schemas/         # Marshmallow
      migrations/      # Alembic (env.py es parcheado por setup.ps1)
    Dockerfile
  frontend/
    src/
      pages/ components/ hooks/ lib/
    .env.example
docker-compose.yml
setup.ps1              # orquestación: down/build/up/wait/migrate/seed
```

---

## 🚀 Puesta en marcha (Windows)

### Requisitos
- **Docker Desktop** actualizado
- **Node.js 22+** y **npm**
- **PowerShell** (con políticas para scripts si hiciera falta)

### Backend (Docker)
Desde la raíz del proyecto `v1`:
```powershell
cd C:\goldcert\v1
.\setup.ps1 -Rebuild
```
Este script:
1) **Parchea** `backend\app\migrations\env.py` (evita el `KeyError: 'formatters'` de Alembic).  
2) `docker compose down -v && build && up -d` **siempre anclado** a `C:\goldcert\v1`.  
3) Espera a que la **DB** esté `healthy` con `docker inspect`.  
4) Ejecuta `flask db upgrade` y `python seed.py`.

**Swagger UI:** http://localhost:5000/swagger-ui  
**Health:** http://localhost:5000/api/health  
**Credenciales seed:** `admin@test.com / admin` (rol Admin) + catálogo de tipos (SE/EE/ENACOM/INAL).

### Frontend (Vite + React + TS)
```powershell
cd C:\goldcert\v1\frontend
copy .env.example .env
npm install
npm run dev
```
Abrí http://localhost:5173

> `VITE_API_URL` viene en `.env.example` apuntando a `http://localhost:5000/api`.

---

## 🔐 Variables de entorno (backend, referencia)

Si corres backend fuera de Docker:
```
DATABASE_URL=postgresql+psycopg://goldcert:goldcert@localhost:5432/goldcert
JWT_SECRET_KEY=cambia-esto-en-produccion
CORS_ORIGINS=http://localhost:5173
```
Con Docker, `docker-compose.yml` y `setup.ps1` ya inyectan `DATABASE_URL` al contenedor `backend`.

---

## 🧪 Pruebas rápidas de API (PowerShell)

```powershell
# Login (Admin)
$login = Invoke-RestMethod -Method POST `
  -Uri http://localhost:5000/api/auth/login `
  -ContentType application/json `
  -Body (@{email="admin@test.com";password="admin"} | ConvertTo-Json)

$token = "$($login.access_token)"
$headers = @{ Authorization = "Bearer $token" }

# Crear proveedor
Invoke-RestMethod -Method POST `
  -Uri http://localhost:5000/api/providers/ `
  -Headers $headers -ContentType application/json `
  -Body (@{nombre="Proveedor Demo";contacto_email="demo@proveedor.com"} | ConvertTo-Json)

# Crear producto (seleccionando proveedor por ID)
Invoke-RestMethod -Method POST `
  -Uri http://localhost:5000/api/products/ `
  -Headers $headers -ContentType application/json `
  -Body (@{nombre="Freidora";categoria="Cocina";marca="Goldmund";origen="CN";proveedor_id=1} | ConvertTo-Json)

# Crear certificado (SE por marca: exige fabrica y auditoría vigente)
Invoke-RestMethod -Method POST `
  -Uri http://localhost:5000/api/certificates/ `
  -Headers $headers -ContentType application/json `
  -Body (@{
      producto_id=1; tipo_certificacion="SE"; ambito_certificado="marca";
      modelo_proveedor_id=1; fabrica_id=1;
      fecha_emision="2025-08-01"; fecha_vencimiento="2027-08-01"
    } | ConvertTo-Json)

# Listar alertas
Invoke-RestMethod -Method GET -Uri http://localhost:5000/api/alerts -Headers $headers
```

> Recordá: `Authorization: Bearer <token>` (sin comillas).

---

## 🗃️ Modelo de datos (resumen)

- **Proveedor** (`id`, `nombre`, `contacto_*`)  
  ↳ **Fábrica** (`id`, `proveedor_id`, `direccion`)  
  ↳ **AuditoriaFabrica** (`id`, `fabrica_id`, `fecha_auditoria`, `fecha_vencimiento`)
- **Producto** (`id`, `nombre`, `categoria`, `marca`, `origen`, `proveedor_id`)  
- **ModeloProveedor** (`id`, `producto_id`, `codigo_proveedor`) — “type” base (AFD700)  
- **ModeloProducto** (`id`, `modelo_proveedor_id`, `codigo_goldmund`) — variantes estéticas  
- **VariacionEstetica** y **VariacionModelos** (agrupación estética N..N)  
- **TipoCertificacion** (`SE`, `EE`, `ENACOM`, `INAL`)  
- **Certificado** (`producto_id`, `tipo_certificacion`, `ambito_certificado`, `modelo_proveedor_id`, `fabrica_id`, `tipo_ensayo`, `test_report`, `fecha_emision`, `fecha_vencimiento`)  
- **DeclaracionJurada** y **DeclaracionModelos** (Plantilla DJ + modelos asociados)

**Reglas clave**:
- **Sin solapamientos** de vigencias del mismo certificado.  
- **SE/EE**: `ambito_certificado` = `tipo` o `marca`; **ENACOM/INAL** no dependen de auditoría (ambito `NULL`).  
- **Marca**: requiere **auditoría de fábrica vigente**; si no hay auditoría vigente, estado `suspendido`.  
- Estados automáticos + **alertas** a 30/60/90/180/365 días.  
- Bloqueos **hard** según estado (el sistema sugiere crear tareas; no las crea solo).

---

## 🛠️ Comandos útiles

```powershell
# reconstruir todo
cd C:\goldcert\v1
.\setup.ps1 -Rebuild

# logs backend en vivo
docker compose --project-directory C:\goldcert\v1 logs backend -f

# migraciones manuales
docker compose --project-directory C:\goldcert\v1 exec -T backend flask db upgrade

# seed manual
docker compose --project-directory C:\goldcert\v1 exec -T backend python seed.py
```

---

## 🧯 Troubleshooting

- **DB not healthy / timeout**  
  ```powershell
  docker compose --project-directory C:\goldcert\v1 up -d
  docker compose --project-directory C:\goldcert\v1 ps
  ```
- **Alembic `KeyError: 'formatters'`**  
  Ejecutá `.\setup.ps1 -Rebuild` para reescribir `env.py` limpio.
- **`npm` no reconocido / scripts bloqueados**  
  Instalá Node o habilitá ejecución:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
- **Vite: `Port 5173 is already in use`**  
  `npm run dev -- --port 5174`
- **401/“Invalid token”**  
  Re‑login y usá header exacto `Authorization: Bearer <token>`.

---

## 🧭 Roadmap inmediato

- Configuración UI de umbrales/alertas y canales (sumar **email**).  
- Reportes/exportaciones (CSV/Excel).  
- Ajustes de permisos (RBAC fino).  
- Mejora de wizard con checklist y validaciones adicionales.

---

## 🤝 Contribuir

1) Branch desde `main`.  
2) Commits atómicos.  
3) PR con pasos de prueba, capturas y logs.

---

## 🔒 Seguridad

- No commitear secretos reales.  
- Rotar `JWT_SECRET_KEY` para cada entorno.  
- Respaldar el volumen `v1_db_data` si hay datos valiosos.

---

## 📄 Licencia

Privado — uso interno GoldCert.
