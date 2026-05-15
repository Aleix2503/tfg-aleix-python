# FSM Editor Framework

Un framework visual para crear y editar Máquinas de Estados Finitos (FSM) interactivamente usando Python y PySide6.

## 📁 Estructura del Proyecto

```
tfg-aleix-python/
├── README.md                 # Este archivo
├── main.py                   # Punto de entrada de la aplicación
├── requirements.txt          # Dependencias del proyecto
│
├── build_config/             # Scripts para compilar ejecutable
│   ├── setup.py              # Script de setup (crea ejecutable e instala archivo)
│   ├── register_fsmproj.bat  # Batch para registrar asociación de archivos
│   ├── register_fsmproj.reg  # Archivo de registro de Windows (manual)
│   └── BUILD_AND_INSTALL.md  # Guía completa de construcción
│
├── editor/                   # GUI components
│   ├── window.py             # Ventana principal
│   ├── graph_view.py         # Vista gráfica del FSM (editor visual)
│   ├── node_item.py          # Representación visual de estados
│   ├── edge_item.py          # Representación visual de transiciones
│   ├── inspector.py          # Panel de propiedades (inspector)
│   └── __init__.py
│
├── model/                    # Modelo de datos (lógica del FSM)
│   ├── fsm.py                # Clase principal FSM
│   ├── state.py              # Definición de estados
│   ├── transition.py         # Definición de transiciones
│   ├── action.py             # Acciones de los estados
│   ├── condition.py          # Condiciones de las transiciones
│   └── __init__.py
│
├── commands/                 # Sistema Undo/Redo (Command Pattern)
│   ├── command_manager.py    # Gestor de comandos
│   ├── commands.py           # Implementaciones de comandos
│   └── __init__.py
│
├── persistence/              # Serialización/Deserialización
│   ├── project_serializer.py # Guardado a archivo .fsmproj
│   ├── project_loader.py     # Cargado desde archivo .fsmproj
│   └── __init__.py
│
├── data/                     # Registros de datos
│   ├── action_registry.py    # Acciones disponibles (predefinidas)
│   ├── condition_registry.py # Condiciones disponibles
│   └── __init__.py
│
└── export/                   # Exportación de datos
    ├── json_exporter.py      # Exportación a JSON
    └── __init__.py
```

## 🚀 Inicio Rápido

### Requisitos
- Python 3.7+
- PySide6

### Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

### Abrir un proyecto guardado

```bash
python main.py "ruta/del/proyecto.fsmproj"
```

## 🔧 Compilar a Ejecutable (Windows)

### Opción 1: Automática (Recomendado)

```bash
python build_config/setup.py
```

Esto:
- ✅ Instala PyInstaller si es necesario
- ✅ Compila todo a `dist/FSMEditor.exe`
- ✅ Registra automáticamente la asociación de archivos `.fsmproj`
- ✅ Puedes hacer doble clic en archivos `.fsmproj` para abrirlos

### Opción 2: Manual

Ver [BUILD_AND_INSTALL.md](build_config/BUILD_AND_INSTALL.md) para instrucciones detalladas.

## 📝 Componentes Principales

### Editor (`editor/`)
- **window.py**: Ventana principal con menús (File, Edit)
- **graph_view.py**: Canvas interactivo para crear/editar FSM
- **node_item.py**: Representación visual de estados (nodos)
- **edge_item.py**: Representación visual de transiciones (aristas)
- **inspector.py**: Panel lateral para editar propiedades

### Modelo (`model/`)
Estructura de datos que representa el FSM:
- **fsm.py**: Contenedor principal con estados y transiciones
- **state.py**: Estados (normal, entry point, global state, any_state)
- **transition.py**: Transiciones entre estados
- **action.py**: Acciones (Enter, Tick, Exit)
- **condition.py**: Condiciones para transiciones

### Comandos (`commands/`)
Sistema de Undo/Redo basado en el patrón Command:
- **command_manager.py**: Gestiona pilas de undo/redo
- **commands.py**: Implementa comandos específicos (CreateState, DeleteState, etc.)

### Persistencia (`persistence/`)
Serialización/Deserialización de proyectos:
- Guarda/carga proyectos en formato `.fsmproj`
- Preserva toda la información del modelo

## 🎮 Características

✅ Crear/eliminar estados  
✅ Crear/eliminar transiciones  
✅ Auto-transiciones (transiciones de un estado a sí mismo)  
✅ Entry points y global states  
✅ ANY_STATE para transiciones globales  
✅ Sistema Undo/Redo (Ctrl+Z, Ctrl+Shift+Z)  
✅ Guardar/cargar proyectos (Ctrl+S, Ctrl+O)  
✅ Exportar a JSON (Ctrl+E)  
✅ Ejecutable compilado para Windows  
✅ Asociación de archivos para doble clic  

## 📋 Información de Archivos de Build

### `build_config/setup.py`
Script Python que:
1. Detecta la instalación de PyInstaller
2. Compila el proyecto a ejecutable usando PyInstaller
3. Registra automáticamente la extensión `.fsmproj` en Windows
4. Coloca el ejecutable en `dist/FSMEditor.exe`

### `build_config/register_fsmproj.bat`
**Script de comando (Batch)** para registrar archivos `.fsmproj`:
- Genera automáticamente el archivo de registro correcto
- Necesita permisos de administrador
- Más fácil que editar el registro manualmente
- Busca automáticamente el ejecutable en `dist/`

### `build_config/register_fsmproj.reg`
**Archivo de Registro de Windows** (Registry):
- Formato texto que se importa al registro de Windows
- Define cómo se abre `.fsmproj` con el FSM Editor
- Hay que editar manualmente el path del ejecutable
- Se aplica haciendo doble clic en el archivo `.reg`

#### ¿Qué hacen estos archivos?

Ambos archivos hacen lo mismo: **registrar la extensión `.fsmproj` en Windows**, para que cuando hagas doble clic en un archivo `.fsmproj`, se abra automáticamente con `FSMEditor.exe`.

| Aspecto | .bat | .reg |
|---------|------|------|
| **Formato** | Comando ejecutable | Registro de Windows |
| **Facilidad** | ⭐⭐⭐ Muy fácil | ⭐⭐ Necesita editar |
| **Automatización** | ✅ Detecta path automático | ❌ Hay que cambiar path |
| **Requiere Admin** | ✅ Sí | ✅ Sí |
| **Mejor opción** | ✅ Recomendado | Backup manual |

## 🔐 Requisitos del Sistema

- **Windows 10/11**
- **Python 3.7+** (si ejecutas desde fuente)
- **PySide6** (instalado automáticamente)
- **PyInstaller** (solo para compilar ejecutable)

## 📚 Documentación Adicional

- [BUILD_AND_INSTALL.md](build_config/BUILD_AND_INSTALL.md) - Guía de compilación e instalación
- Código autodocumentado con docstrings

## 📄 Licencia

Proyecto de TFG (Trabajo de Fin de Grado)

---