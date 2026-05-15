# Explicación: register_fsmproj.bat y register_fsmproj.reg

## 🎯 Propósito General

Ambos archivos sirven para **registrar la extensión `.fsmproj` en Windows**, de manera que cuando hagas doble clic en cualquier archivo `.fsmproj`, se abra automáticamente con `FSMEditor.exe`.

---

## 📋 register_fsmproj.bat (Batch Script)

### ¿Qué es?
Es un **script de comando ejecutable** (archivo `.bat`) que automatiza el proceso de registro.

### ¿Cómo funciona?

```batch
@echo off
REM Script de Windows que:
1. Detecta dónde está FSMEditor.exe
2. Crea un archivo .reg temporal
3. Lo importa al registro de Windows
4. Limpia archivos temporales
5. Muestra el resultado
```

### ¿Cómo usarlo?

**Paso 1:** Busca el archivo
```
build_config/register_fsmproj.bat
```

**Paso 2:** Haz clic derecho → "Ejecutar como administrador"
```
⚠️ IMPORTANTE: Necesitas permisos de administrador
```

**Paso 3:** El script se ejecutará y verás:
```
====================================================
FSM Editor - File Association Setup
====================================================

Found executable: C:\Users\aleix\Desktop\Uni\TFG\tfg-aleix-python\dist\FSMEditor.exe

Registering .fsmproj file extension...

====================================================
SUCCESS: File association registered!
====================================================

You can now:
  - Double-click .fsmproj files to open them
  - Run FSMEditor.exe directly
```

### Ventajas ✅
- **Automático:** No hay que editar nada manualmente
- **Inteligente:** Detecta automáticamente dónde está el ejecutable
- **Seguro:** Crea un archivo temporal y lo limpia después
- **Fácil:** Solo haz clic derecho → "Ejecutar como administrador"
- **Ágil:** Todo listo en 2-3 segundos

### Desventajas ❌
- Requiere permisos de administrador
- Necesitas hacer clic derecho

### Qué hace internamente

```batch
REM Crea un archivo .reg temporal:
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\.fsmproj]
@="FSMProjectFile"
"Content Type"="application/x-fsmproj"

[HKEY_CLASSES_ROOT\FSMProjectFile]
@="FSM Project File"

[HKEY_CLASSES_ROOT\FSMProjectFile\DefaultIcon]
@="C:\ruta\a\FSMEditor.exe,0"

[HKEY_CLASSES_ROOT\FSMProjectFile\shell\open\command]
@="\"C:\ruta\a\FSMEditor.exe\" \"%1\""

REM Lo importa al registro
reg import temp_file.reg

REM Limpia el temporal
del temp_file.reg
```

---

## 📝 register_fsmproj.reg (Registry File)

### ¿Qué es?
Es un **archivo de registro de Windows** (`.reg`) que se importa manualmente al sistema operativo.

### Contenido del archivo
```registry
Windows Registry Editor Version 5.00

; FSM Project File Association
[HKEY_CLASSES_ROOT\.fsmproj]
@="FSMProjectFile"
"Content Type"="application/x-fsmproj"

[HKEY_CLASSES_ROOT\FSMProjectFile]
@="FSM Project File"

[HKEY_CLASSES_ROOT\FSMProjectFile\DefaultIcon]
@="C:\path\to\FSMEditor.exe,0"

[HKEY_CLASSES_ROOT\FSMProjectFile\shell\open\command]
@="\"C:\path\to\FSMEditor.exe\" \"%1\""
```

### ¿Cómo usarlo?

#### Opción A: Automático (Recomendado)

**Paso 1:** Edita el archivo con un editor de texto
```
Clic derecho → Abrir con → Bloc de notas
```

**Paso 2:** Reemplaza esta línea:
```registry
@="C:\path\to\FSMEditor.exe,0"
```

Por la ruta real (2 lugares):
```registry
@="C:\Users\aleix\Desktop\Uni\TFG\tfg-aleix-python\dist\FSMEditor.exe,0"
```

Y también aquí:
```registry
@="\"C:\Users\aleix\Desktop\Uni\TFG\tfg-aleix-python\dist\FSMEditor.exe\" \"%1\""
```

**Paso 3:** Guarda el archivo (Ctrl+S)

**Paso 4:** Haz doble clic en `register_fsmproj.reg`

**Paso 5:** Verás este diálogo:
```
¿Está seguro de que desea agregar la información 
de la clave de Registro de C:\...\register_fsmproj.reg 
al Registro?
```

Haz clic en **"Sí"**

**Paso 6:** Verás:
```
La información se agregó correctamente al Registro.
```

#### Opción B: PowerShell (Avanzado)

```powershell
# Ejecutar PowerShell como administrador
$exe_path = "C:\Users\aleix\Desktop\Uni\TFG\tfg-aleix-python\dist\FSMEditor.exe"

# Registrar extensión
reg add "HKCR\.fsmproj" /ve /d "FSMProjectFile" /f
reg add "HKCR\.fsmproj" /v "Content Type" /d "application/x-fsmproj" /f

# Registrar programa
reg add "HKCR\FSMProjectFile" /ve /d "FSM Project File" /f
reg add "HKCR\FSMProjectFile\DefaultIcon" /ve /d "$exe_path,0" /f
reg add "HKCR\FSMProjectFile\shell\open\command" /ve /d "`"$exe_path`" `"%1`"" /f

Write-Host "✓ Registro completado!"
```

### Ventajas ✅
- Útil si el `.bat` no funciona
- Se puede editar manualmente
- Funciona como archivo de respaldo
- Portátil (se puede compartir)

### Desventajas ❌
- Hay que editar manualmente la ruta del ejecutable
- Si la ruta cambia, hay que editar de nuevo
- 2-3 pasos más que el `.bat`
- Mayor riesgo de errores al editar

---

## 🔍 Detrás de Escenas: Qué Sucede en Windows

Cuando registras la extensión `.fsmproj`, Windows crea entradas en el Registro:

### Estructura en el Registro

```
Registro de Windows (HKEY_CLASSES_ROOT)
│
├── .fsmproj                           ← Extensión del archivo
│   └── (Default) = "FSMProjectFile"
│   └── Content Type = "application/x-fsmproj"
│
└── FSMProjectFile                     ← Tipo de archivo definido
    │
    ├── (Default) = "FSM Project File"
    │
    ├── DefaultIcon
    │   └── (Default) = "C:\...\FSMEditor.exe,0"
    │       (El ,0 significa: usar el icono #0)
    │
    └── shell\open\command
        └── (Default) = "C:\...\FSMEditor.exe" "%1"
            (%1 = el archivo que haces doble clic)
```

### Qué sucede cuando haces doble clic

```
1. Windows ve la extensión .fsmproj
                ↓
2. Busca en HKEY_CLASSES_ROOT\.fsmproj
                ↓
3. Lee el valor: "FSMProjectFile"
                ↓
4. Busca en HKEY_CLASSES_ROOT\FSMProjectFile\shell\open\command
                ↓
5. Ejecuta: "C:\...\FSMEditor.exe" "tu_archivo.fsmproj"
                ↓
6. FSMEditor.exe recibe "tu_archivo.fsmproj" como argumento
                ↓
7. main.py lee sys.argv[1] y carga el archivo
```

---

## 📊 Comparativa Rápida

| Característica | .bat | .reg |
|---|---|---|
| **Formato** | Script de comando | Texto (Registro) |
| **Tipo de archivo** | Ejecutable (.bat) | Datos (.reg) |
| **¿Se ejecuta?** | ✅ Sí | ❌ No (se importa) |
| **¿Necesita edición?** | ❌ No | ✅ Sí |
| **Detecta path auto** | ✅ Sí | ❌ No |
| **Facilidad** | ⭐⭐⭐ Muy fácil | ⭐⭐ Normal |
| **Requiere Admin** | ✅ Sí | ✅ Sí |
| **Mejor para** | La mayoría de casos | Respaldo/Backup |

---

## 🚨 Solución de Problemas

### Problema: "No puedo ejecutar el .bat"
**Solución:**
- Haz clic derecho → "Ejecutar como administrador"
- Asegúrate de que FSMEditor.exe esté en `dist/`

### Problema: "No puedo editar el .reg"
**Solución:**
- Haz clic derecho → "Abrir con" → "Bloc de notas"
- O arrastra el archivo a tu editor favorito

### Problema: "No encuentro la ruta del ejecutable para editar el .reg"
**Solución:**
```powershell
# Abre PowerShell en el directorio del proyecto y ejecuta:
(Get-ChildItem -Path "dist\FSMEditor.exe").FullName
```
Copia la ruta completa y úsala en el `.reg`

### Problema: "Los archivos .fsmproj siguen sin abrirse"
**Solución:**
1. Ejecuta el `.bat` como admin nuevamente
2. O importa el `.reg` (con la ruta correcta)
3. Reinicia el explorador de Windows (Ctrl+Shift+Esc → Explorador de Windows → Reiniciar)
4. Intenta de nuevo

### Problema: "Quiero deshacer el registro"
**Solución:**
```powershell
# Ejecutar PowerShell como administrador:
reg delete "HKCR\.fsmproj" /f
reg delete "HKCR\FSMProjectFile" /f
```

---

## 📌 Resumen

- **`.bat` (Recomendado):** Automático, detecta path, muy fácil
- **`.reg` (Backup):** Manual, útil si `.bat` falla, editable
- **Ambos hacen lo mismo:** Registran `.fsmproj` en Windows
- **El resultado es igual:** Puedes hacer doble clic en `.fsmproj` files

🎯 **Usa el `.bat`** para la mayoría de casos. Usa el `.reg` solo si lo primero no funciona.
