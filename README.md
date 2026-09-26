# DataOps Taller — Pipeline de Datos para una Tienda en Línea

**Autora:** María Leyva
**Materia:** Enfoque DataOps

---

## 1. Descripción del proyecto

Este repositorio implementa un pipeline de datos con prácticas de DataOps para una tienda en línea simulada. El pipeline:

1. **Extrae** los datos de ventas de una base de datos SQLite, que simula PostgreSQL.
2. **Limpia y transforma** los datos: elimina duplicados, maneja valores nulos y calcula métricas como las ventas totales por categoría y mes.
3. **Entrena** un modelo de regresión lineal para predecir las ventas del próximo mes.
4. **Genera un reporte** en formato CSV con las ventas agregadas.
5. **Se ejecuta automáticamente** con GitHub Actions en cada push a `main` o a ramas `feature/*`.

Además del código, el proyecto versiona los **datos** con DVC y los **esquemas** con migraciones SQL, y crea **snapshots** periódicos de la base de datos. Con esto se busca un *versionamiento holístico* que garantice la reproducibilidad.

### Tecnologías

| Componente | Herramienta |
|---|---|
| Lenguaje | Python 3.12 |
| Base de datos | SQLite |
| Procesamiento | pandas |
| Modelo | scikit-learn (regresión lineal) + joblib |
| Pruebas | pytest, pytest-cov |
| Análisis estático | pylint, black, bandit |
| CI/CD | GitHub Actions |
| Versionamiento de código | Git + GitHub |
| Versionamiento de datos | DVC |

---

## 2. Instalación

### Requisitos previos
- Python 3.12 (compatible con 3.9+)
- Git
- Git Bash (en Windows) o una terminal Unix

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/kataleyva/dataops-taller-maria-leyva.git
cd dataops-taller-maria-leyva

# 2. Crear y activar el entorno virtual
python -m venv venv
source venv/Scripts/activate      # Windows (Git Bash)
# source venv/bin/activate        # Linux / macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Generar la base de datos simulada
python scripts/create_db.py

# 5. Ejecutar el pipeline completo
python -m src.train

# 6. Ejecutar las pruebas
pytest -v
```

> **Nota:** la base de datos (`data/ventas.db`) **no** se versiona con Git. Se regenera con `scripts/create_db.py`, que usa una semilla fija para producir siempre los mismos datos, o se descarga con `dvc pull`.

---

## 3. Estructura del repositorio

```
dataops-taller-maria-leyva/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline de CI/CD (GitHub Actions)
├── data/                        # Datos (ignorados por Git, versionados con DVC)
│   └── snapshots/               # Copias fechadas de la base de datos
├── migrations/                  # Scripts SQL de migración de esquema
├── models/                      # Modelo entrenado (model.pkl)
├── notebooks/
│   └── exploracion.ipynb        # Análisis exploratorio de datos
├── scripts/
│   ├── create_db.py             # Genera la base SQLite con datos simulados
│   └── create_snapshot.py       # Crea snapshots de la base de datos
├── src/
│   ├── __init__.py
│   ├── extract.py               # Extracción de datos desde SQLite
│   ├── transform.py             # Limpieza, métricas y agregación
│   ├── train.py                 # Entrenamiento del modelo
│   └── utils.py                 # Funciones auxiliares (exportar CSV)
├── tests/
│   ├── __init__.py
│   ├── test_transform.py        # Pruebas unitarias
│   ├── test_data_quality.py     # Pruebas de esquema y calidad de datos
│   └── test_integration.py      # Pruebas de integración
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

### ¿Qué se excluye de Git? (`.gitignore`)

| Patrón | Motivo |
|---|---|
| `venv/`, `env/` | Los entornos virtuales dependen de cada máquina y se recrean con `requirements.txt`. |
| `*.csv`, `*.db`, `data/*` | Los datos pueden ser grandes y cambian con frecuencia. Se versionan con **DVC**, no con Git. |
| `!data/*.dvc`, `!data/.gitignore` | Excepciones: los archivos `.dvc` son punteros livianos (hashes) que **sí** deben ir en Git. |
| `models/*.pkl` | El modelo se genera en el pipeline y se publica como artefacto de CI. |
| `.env` | Credenciales y configuración sensible. |
| `.ipynb_checkpoints/`, `__pycache__/` | Archivos temporales generados automáticamente. |

---

## 4. Flujo de trabajo con Git

### Estrategia de ramas

- **`main`**: rama estable. Solo recibe cambios mediante Pull Request, después de que el pipeline de CI pasa.
- **`feature/<nombre>`**: ramas de característica para desarrollar funcionalidades nuevas de forma aislada (por ejemplo, `feature/pipeline-inicial`).

```
main ──●───────────────────────●──── (merge vía Pull Request)
        \                     /
         ●──●──●──●──●──●──●─      feature/pipeline-inicial
```

### Convención de commits

Se usan **commits atómicos**: cada commit contiene un solo cambio lógico. Los mensajes siguen el formato [Conventional Commits](https://www.conventionalcommits.org/):

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feat:` | Nueva funcionalidad | `feat: add extract module` |
| `fix:` | Corrección de errores | `fix: handle missing database file` |
| `test:` | Pruebas | `test: add unit tests for transform` |
| `docs:` | Documentación | `docs: add installation instructions` |
| `chore:` | Configuración y mantenimiento | `chore: add .gitignore` |
| `ci:` | Pipeline de CI/CD | `ci: add GitHub Actions workflow` |

### Comandos de Git utilizados

| Comando | Propósito |
|---|---|
| `git clone <url>` | Descargar el repositorio remoto con todo su historial. |
| `git checkout -b feature/pipeline-inicial` | Crear una rama de característica y cambiarse a ella. |
| `git status` | Ver qué archivos cambiaron y cuáles están en el *staging area*. |
| `git add <archivo>` / `git add .` | Pasar cambios del *working directory* al *staging area*. |
| `git commit -m "<mensaje>"` | Guardar los cambios preparados en el repositorio local. |
| `git commit --amend` | Corregir el último commit (solo si todavía no se ha hecho push). |
| `git log --oneline` | Ver el historial de commits de forma resumida. |
| `git push -u origin feature/pipeline-inicial` | Subir la rama al remoto y dejar configurado el seguimiento (*upstream*). |

El flujo básico:

```
Working Directory ──git add──▶ Staging Area ──git commit──▶ Repo local ──git push──▶ Repo remoto (GitHub)
```

---

## 5. Pipeline de CI/CD

*En construcción (Tarea 4).*

## 6. Versionamiento de datos y esquemas

*En construcción (Tarea 5).*

## 7. Informe y análisis de resultados

*En construcción (Tarea 6).*