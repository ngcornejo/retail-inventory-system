# retail-inventory-system

Sistema de gestión de inventario para entornos de retail con múltiples depósitos, alertas de stock y análisis de demanda con proyecciones por día de la semana.

Desarrollado con **Python**, **Flask** y **SQLite**. Análisis de datos con **Pandas**.

---

## Características

- Gestión de productos organizados por categoría (pasillos)
- Control de stock por depósito independiente
- Alertas automáticas cuando el stock cae por debajo del umbral configurado
- Registro histórico de ventas con fecha y hora
- Métricas de rotación y demanda por producto
- Proyecciones de demanda estimada según día de la semana
- API REST documentada, consumible desde cualquier cliente o frontend

---

## Tecnologías

| Componente | Tecnología |
|---|---|
| Backend | Python 3.11+ · Flask |
| Base de datos | SQLite |
| Análisis de datos | Pandas |
| Frontend | HTML · CSS · JavaScript (vanilla) |
| Control de versiones | Git · GitHub |

---

## Estructura del proyecto

```
retail-inventory-system/
│
├── backend/
│   ├── app.py               # Entry point de Flask
│   ├── database.py          # Conexión y setup de SQLite
│   ├── models/
│   │   ├── product.py       # Modelo de producto
│   │   ├── warehouse.py     # Modelo de depósito
│   │   └── sale.py          # Modelo de venta
│   ├── routes/
│   │   ├── products.py      # Endpoints de productos
│   │   ├── warehouses.py    # Endpoints de depósitos
│   │   ├── sales.py         # Endpoints de ventas
│   │   └── analytics.py     # Endpoints de métricas y proyecciones
│   └── analytics/
│       ├── metrics.py       # Cálculo de rotación y demanda
│       └── forecast.py      # Proyecciones por día de la semana
│
├── frontend/
│   ├── index.html           # Dashboard principal
│   ├── style.css
│   └── app.js
│
├── data/
│   └── inventory.db         # Base de datos SQLite (generada automáticamente)
│
├── docs/
│   └── api.md               # Documentación de endpoints
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalación

### Requisitos previos

- Python 3.11 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/retail-inventory-system.git
cd retail-inventory-system

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar la base de datos
python backend/database.py

# 5. Ejecutar el servidor
python backend/app.py
```

El servidor queda disponible en `http://localhost:5000`.

---

## API — Referencia rápida

Documentación completa en [`docs/api.md`](docs/api.md).

### Productos

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/products` | Listar todos los productos |
| GET | `/api/products/<id>` | Obtener un producto |
| POST | `/api/products` | Crear producto |
| PUT | `/api/products/<id>` | Actualizar producto |
| DELETE | `/api/products/<id>` | Eliminar producto |

### Depósitos

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/warehouses` | Listar depósitos |
| GET | `/api/warehouses/<id>/stock` | Ver stock de un depósito |
| POST | `/api/warehouses` | Crear depósito |
| PUT | `/api/warehouses/<id>/stock` | Actualizar stock |

### Ventas

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/sales` | Registrar venta |
| GET | `/api/sales` | Historial de ventas |

### Analytics

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/analytics/metrics` | Métricas generales (rotación, demanda) |
| GET | `/api/analytics/alerts` | Productos con stock bajo |
| GET | `/api/analytics/forecast` | Proyecciones por día de la semana |

---

## Modelo de datos

### Producto

```json
{
  "id": 1,
  "name": "Leche entera 1L",
  "category": "Lácteos",
  "price": 1200.00,
  "stock_threshold": 20
}
```

### Depósito

```json
{
  "id": 1,
  "name": "Depósito Central",
  "location": "Buenos Aires"
}
```

### Stock (por depósito)

```json
{
  "warehouse_id": 1,
  "product_id": 1,
  "quantity": 150
}
```

### Venta

```json
{
  "id": 1,
  "product_id": 1,
  "warehouse_id": 1,
  "quantity": 5,
  "date": "2026-05-05T14:32:00"
}
```

---

## Analytics — Detalle

### Métricas de rotación

Calcula cuántas unidades de un producto se venden en promedio por día, basándose en el historial de ventas registrado.

### Alertas de stock

Un producto activa una alerta cuando su stock en algún depósito cae por debajo del `stock_threshold` configurado.

### Proyecciones por día de la semana

Estima la demanda esperada para cada día (lunes a domingo) usando el promedio histórico de ventas agrupado por día de la semana. Útil para planificar reposición de stock anticipadamente.

---

## Categorías de productos (pasillos)

| Categoría | Ejemplos |
|---|---|
| Lácteos | Leche, yogurt, queso |
| Carnes | Vacuna, aviar, cerdo |
| Bebidas | Gaseosas, agua, jugos |
| Panadería | Pan, galletitas, facturas |
| Limpieza | Detergente, lavandina |
| Almacén | Arroz, fideos, aceite |

> Las categorías son configurables — no están hardcodeadas en el sistema.

---

## Roadmap

- [x] Diseño de base de datos y modelos
- [x] Documentación inicial (este README)
- [ ] Implementación de modelos y base de datos
- [ ] Endpoints CRUD de productos y depósitos
- [ ] Registro de ventas
- [ ] Módulo de analytics y proyecciones
- [ ] Frontend — Dashboard
- [ ] Documentación de API (`docs/api.md`)
- [ ] Deploy en GitHub Pages (frontend estático)

---

## Autor

**Nicolás Gonzalez Cornejo**
ngcornejo15@gmail.com · [GitHub](https://github.com/TU_USUARIO)

---

*Proyecto de portfolio personal. Caso de uso hipotético inspirado en entornos de retail reales.*
