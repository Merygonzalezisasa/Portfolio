# SETUP — Finance Analytics España

Qué se instaló en esta máquina (Windows 11 Pro), con qué comando, y qué errores
aparecieron en el camino. Regla de oro de la Fase 0.5: cada error resuelto se anota,
porque va a volver a pasar en otra máquina dentro de tres semanas.

## Inventario inicial (2026-07-17)

Ya estaban instalados:
- **Power BI Desktop** v2.155 (Microsoft Store)
- **VS Code**

Faltaban: Python, Git, PostgreSQL.

## Lo que se instaló y cómo

### Python 3.12.10 (por usuario, sin admin)

El plan A era winget (`winget install Python.Python.3.12`), pero **se colgó dos veces
sin producir salida** en la terminal no interactiva. Plan B — instalador oficial directo:

```powershell
# Descargar de python.org y correr en silencio (instala en %LOCALAPPDATA%\Programs\Python\Python312)
Invoke-WebRequest "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe" -OutFile python-3.12.10-amd64.exe
Start-Process .\python-3.12.10-amd64.exe -ArgumentList "/quiet","InstallAllUsers=0","PrependPath=1","Include_launcher=1" -Wait
```

Verificado: `python --version` → `Python 3.12.10`.

### Entorno virtual + dependencias

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Git (instalador oficial de git-for-windows, GitHub Releases)

```powershell
# La URL exacta se obtiene de https://api.github.com/repos/git-for-windows/git/releases/latest
Start-Process .\Git-<version>-64-bit.exe -ArgumentList "/VERYSILENT","/NORESTART","/CURRENTUSER" -Wait
git config --global user.name  "Rosmary González Isasa"
git config --global user.email "isasamery@gmail.com"
```

*(estado: en curso — se actualiza al terminar)*

### PostgreSQL 16 (nativo, decisión de FICHA.md §7) + pgAdmin 4

*(pendiente — se documenta al instalar)*

## Errores encontrados y su solución

| Síntoma | Causa | Solución |
|---|---|---|
| `python` en la terminal "responde" pero pide instalar desde la Store | Es el **alias stub** de Microsoft Store, no un Python real | Desactivar el alias o instalar Python de verdad; verificar con `Get-Command python` que apunte a `...\Programs\Python\...` |
| `curl.exe` a APIs HTTPS falla con exit code 35 | Windows PowerShell 5.1 negocia TLS viejo | `[Net.ServicePointManager]::SecurityProtocol = Tls12` antes de llamar; en Python `requests` no hace falta |
| `winget install` se cuelga sin salida en terminal no interactiva | winget espera algo que no puede mostrar (elevación/acuerdos) | Descargar el instalador oficial y correrlo con flags silenciosos (`/quiet`, `/VERYSILENT`) |
