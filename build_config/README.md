# Build Configuration - Scripts de Construcción

Esta carpeta contiene todos los scripts necesarios para compilar el FSM Editor a un ejecutable Windows e instalar la asociación de archivos.

## 📂 Contenido

### 1. **setup.py** - Script Principal de Setup
Script Python que automatiza todo el proceso de construcción.

**Qué hace:**
- ✅ Verifica que PyInstaller esté instalado
- ✅ Compila todo el proyecto a un ejecutable único (`FSMEditor.exe`)
- ✅ Registra automáticamente la extensión `.fsmproj` en Windows
- ✅ Muestra mensajes de progreso y éxito

**Cómo usarlo:**
```bash
python setup.py
```

**Requisitos previos:**
```bash
pip install -r ../requirements.txt
```

---

### 2. **register_fsmproj.bat** - Batch de Registro Automático
Script de comando Windows (.bat) que registra archivos `.fsmproj`.

**Qué hace:**
- ✅ Detecta automáticamente dónde está el ejecutable `FSMEditor.exe`
- ✅ Crea un archivo de registro temporal (.reg)
- ✅ Lo aplica automáticamente al sistema Windows
- ✅ Limpia archivos temporales

**Cómo usarlo:**
1. Haz clic derecho en `register_fsmproj.bat`
2. Selecciona "Ejecutar como administrador"
3. El script se ejecutará y mostrará el resultado

**Ventajas:**
- 🟢 Automático - no hay que editar nada
- 🟢 Detecta el path del ejecutable automáticamente
- 🟢 Más fácil que editar el registro manualmente

**Requisitos:**
- Administrador del sistema

---

### 3. **register_fsmproj.reg** - Archivo de Registro Manual
Archivo de formato `.reg` (Registro de Windows) que se puede importar manualmente.

**Qué hace:**
- 📝 Define cómo se abren archivos `.fsmproj` con FSM Editor
- 📝 Crea asociaciones en el registro de Windows
- 📝 Se puede editar con cualquier editor de texto

**Cómo usarlo (Opción A - Automático):**
1. Edita el archivo con Bloc de Notas
2. Reemplaza `C:\path\to\FSMEditor.exe` con la ruta real
3. Ejemplo: `C:\Users\aleix\Desktop\Uni\TFG\tfg-aleix-python\dist\FSMEditor.exe`
4. Guarda el archivo
5. Haz doble clic en `register_fsmproj.reg`
6. Haz clic en "Sí" cuando se pida confirmación

**Cómo usarlo (Opción B - PowerShell):**
```powershell
$exe_path = "C:\ruta\actual\dist\FSMEditor.exe"
reg add "HKCR\.fsmproj" /ve /d "FSMProjectFile" /f
reg add "HKCR\.fsmproj" /v "Content Type" /d "application/x-fsmproj" /f
reg add "HKCR\FSMProjectFile" /ve /d "FSM Project File" /f
reg add "HKCR\FSMProjectFile\DefaultIcon" /ve /d "$exe_path,0" /f
reg add "HKCR\FSMProjectFile\shell\open\command" /ve /d "`"$exe_path`" `"%1`"" /f
```

**Ventajas:**
- 🔧 Útil si el script .bat no funciona
- 🔧 Se puede editar manualmente
- 🔧 Funciona como backup

**Requisitos:**
- Administrador del sistema
- Editar el path manualmente

---

### 4. **BUILD_AND_INSTALL.md** - Guía Completa
Documentación detallada de todos los métodos de construcción e instalación.

## 🚀 Flujo de Trabajo Recomendado

### Opción 1: Automática (Recomendado)
```bash
# Desde el directorio raíz del proyecto
python build_config/setup.py
```

Resultado:
- ✅ `dist/FSMEditor.exe` listo para usar
- ✅ Archivo asociación automáticamente instalada
- ✅ Puedes hacer doble clic en `.fsmproj` files

### Opción 2: Manual
```bash
# Paso 1: Compilar con PyInstaller
PyInstaller --name=FSMEditor --onefile --windowed ^
    --add-data data:data --add-data model:model ^
    --add-data editor:editor --add-data commands:commands ^
    --add-data persistence:persistence --add-data export:export ^
    main.py

# Paso 2: Registrar (elige uno):

# A) Con batch automático
build_config\register_fsmproj.bat

# B) Con el archivo .reg editado manualmente
# (edita build_config/register_fsmproj.reg)
# y haz doble clic
```

## 📊 Comparativa de Métodos

| Método | Facilidad | Automático | Requisitos |
|--------|-----------|-----------|------------|
| **setup.py** | ⭐⭐⭐ Muy fácil | ✅ Sí | Python, pip |
| **register_fsmproj.bat** | ⭐⭐⭐ Muy fácil | ✅ Sí | Admin |
| **register_fsmproj.reg** | ⭐⭐ Normal | ❌ No | Admin, edición manual |
| **PowerShell** | ⭐ Difícil | ⚠️ Parcial | Admin, conocimiento PS |

## 🔍 Contenido de los Archivos de Registro

### Qué se registra en Windows

Cuando ejecutas cualquiera de los métodos de registro, Windows recibe:

```
Extensión:        .fsmproj
Tipo de archivo:  FSMProjectFile
Descripción:      FSM Project File
Ícono:            [ícono del ejecutable]
Comando de apertura: "C:\ruta\a\FSMEditor.exe" "%1"
```

### Dónde se almacena

En el registro de Windows (Regedit):
```
HKEY_CLASSES_ROOT
├── .fsmproj              (extensión)
│   └── FSMProjectFile    (tipo asociado)
│
└── FSMProjectFile        (definición del tipo)
    ├── DefaultIcon
    └── shell\open\command
```

## ⚠️ Solución de Problemas

### "No se encuentra PyInstaller"
```bash
pip install pyinstaller
```

### "Acceso denegado" o error de permisos
- Ejecuta los scripts como **Administrador**
- Haz clic derecho → "Ejecutar como administrador"

### No puedo editar register_fsmproj.reg
- Haz clic derecho → "Abrir con..." → "Bloc de notas"
- Reemplaza la ruta `C:\path\to\FSMEditor.exe`
- Guarda

### Los archivos .fsmproj no abren al doble clic
- Ejecuta nuevamente `build_config/register_fsmproj.bat` como admin
- O importa manualmente el `.reg` (edita la ruta primero)

### No encuentro el ejecutable después de build
- Mira en `../dist/FSMEditor.exe` (relativo a esta carpeta)
- O busca `FSMEditor.exe` en el directorio del proyecto

## 🎯 Próximos Pasos

Después de compilar:

1. **Prueba el ejecutable:**
   ```bash
   dist/FSMEditor.exe
   ```

2. **Abre un archivo .fsmproj:**
   - Haz doble clic en un archivo `.fsmproj`
   - O ejecuta: `FSMEditor.exe "archivo.fsmproj"`

3. **Crea un acceso directo (opcional):**
   - Clic derecho en `dist/FSMEditor.exe`
   - "Enviar a" → "Escritorio (crear acceso directo)"

4. **Distribuye (opcional):**
   - Copia `dist/FSMEditor.exe` a otros PC
   - No necesitan Python instalado

---