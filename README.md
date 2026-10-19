<div align="center">

  <img src="logo.png" alt="TranscribeNext Logo" width="110" height="110" style="border-radius: 20px;" />

  # TranscribeNext

  **Transcriptor inteligente de audios a texto con IA local. 100% privado, ilimitado y sin suscripciones.**

  <p>
    <a href="https://github.com/jhoel0521/transcriptor-audios/releases"><img src="https://img.shields.io/badge/ESTADO-ESTABLE%20v1.0-2ea44f?style=for-the-badge" alt="Estado" /></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/PYTHON-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /></a>
    <a href="https://github.com/SYSTRAN/faster-whisper"><img src="https://img.shields.io/badge/MOTOR-FASTER--WHISPER-orange?style=for-the-badge" alt="Faster Whisper" /></a>
    <img src="https://img.shields.io/badge/PRIVACIDAD-100%25%20LOCAL-6f42c1?style=for-the-badge" alt="100% Local" />
    <img src="https://img.shields.io/badge/RED-OFFLINE%20LISTO-0366d6?style=for-the-badge" alt="Offline" />
    <a href="LICENSE"><img src="https://img.shields.io/badge/LICENCIA-GPL--3.0-informational?style=for-the-badge" alt="Licencia" /></a>
  </p>

  <p>
    <a href="#-vista-rápida">Vista rápida</a> •
    <a href="#-características">Características</a> •
    <a href="#-instalación-rápida">Instalación rápida</a> •
    <a href="#-cómo-se-usa-paso-a-paso">Cómo se usa</a> •
    <a href="#-uso-desde-la-terminal">Modo Terminal (CLI)</a> •
    <a href="#-preguntas-frecuentes">Preguntas frecuentes</a>
  </p>

</div>

---

**TranscribeNext** convierte tus audios y notas de voz a texto en cuestión de segundos utilizando los modelos de inteligencia artificial de [Whisper](https://github.com/openai/whisper) ejecutados **directamente en tu propia computadora**. 

> [!NOTE]
> 🔒 **Privacidad total garantizada:** Tus audios, grabaciones y conversaciones **nunca salen de tu equipo** ni se envían a ningún servidor externo. Tras la primera ejecución, el programa funciona **100% sin conexión a internet**.

---

## 🎬 Vista rápida

Solo tienes que arrastrar tu archivo y obtendrás el texto transcrito de inmediato:

```text
  ┌─────────────────────────────────────────────────────────────┐
  │  1. Arrastra tu audio  ──►  2. Procesamiento local (IA)     │
  │     (WhatsApp, MP3...)         (Whisper en tu propio CPU)   │
  │                                           │                 │
  │                                           ▼                 │
  │                             3. ¡Texto listo para copiar!    │
  └─────────────────────────────────────────────────────────────┘
```

### 🎵 Formatos de audio soportados
`WhatsApp (.ogg, .opus)` • `.mp3` • `.m4a` • `.wav` • `.aac` • `.flac` • `.webm` • `.mp4`

---

## ✨ Características

- 🔒 **Privacidad absoluta**: Tus grabaciones personales, médicas, legales o de trabajo permanecen en tu computadora.
- ⚡ **Rápido y optimizado**: Motor [faster-whisper](https://github.com/SYSTRAN/faster-whisper) con aceleración eficiente en procesadores estándar.
- 🎯 **Dos modelos según tu necesidad**:
  - **Preciso (`large-v3-turbo`)**: Máxima exactitud y puntuación gramatical impecable.
  - **Rápido (`small`)**: Velocidad superior, ideal para equipos más modestos o transcripciones rápidas.
- ⏱️ **Marcas de tiempo opcionales**: Activa la casilla *Con tiempos* para obtener el minuto exacto `[00:15]` de cada intervención.
- 📁 **Soporte para múltiples audios y carpetas**: Procesa audios sueltos o una carpeta completa en lote.
- 📋 **Exportación en un clic**: Copia todo al portapapeles o guárdalo como archivo `.txt`.
- 🧳 **100% Portable**: No requiere instalador ni permisos de administrador; puedes llevarlo en una memoria USB.

---

## 🚀 Instalación rápida

Elige la opción que mejor se adapte a ti:

### 🌟 Opción 1: Descargar versión lista para usar (Recomendada)
*No necesitas saber de programación ni instalar Python.*

1. Ve a la sección de **[Últimas Versiones (Releases)](../../releases/latest)**.
2. Descarga el paquete correspondiente a tu sistema operativo:

| Sistema Operativo | Archivo de descarga | Cómo iniciarlo |
|---|---|---|
| **Windows 10 / 11** (64 bits) | `Transcriptor-Windows.zip` | Descomprime el `.zip` y haz doble clic en `Transcriptor.exe` |
| **Linux** (Ubuntu, Debian, Mint, Fedora) | `Transcriptor-Linux.zip` | Descomprime y ejecuta el archivo `Transcriptor` |
| **macOS** | *(Próximamente ejecutable)* | Usar la Opción 2 (desde código) |

> [!TIP]
> **¿Aparece el aviso "Windows protegió su PC"?**  
> Al tratarse de un programa de código abierto sin firma digital comercial, Windows SmartScreen puede mostrar una advertencia azul. Es completamente seguro: haz clic en **"Más información"** y luego en **"Ejecutar de todas formas"**.

> [!IMPORTANT]
> **Primera vez que transcribes:**  
> En la primera transcripción, la aplicación descargará el modelo de inteligencia artificial (~1.6 GB) de forma automática. Tardará unos minutos según la velocidad de tu internet. **A partir de ese momento, funcionará siempre sin conexión a internet.**

---

### 💻 Opción 2: Ejecutar desde el código fuente
*Para desarrolladores o usuarios que deseen personalizar el código.*

#### Prerrequisitos
- **Python 3.10** o superior instalado.
- *(En Linux Debian/Ubuntu)*: `sudo apt install python3-venv python3-tk`

#### Paso a paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/jhoel0521/transcriptor-audios.git
cd transcriptor-audios

# 2. Crear el entorno virtual
python -m venv .venv
```

**En Windows:**
```powershell
# Activar entorno e instalar dependencias
.venv\Scripts\python -m pip install -r requirements.txt

# Iniciar la aplicación
.venv\Scripts\python app.pyw
```

**En Linux o macOS:**
```bash
# Activar entorno e instalar dependencias
.venv/bin/python -m pip install -r requirements.txt

# Iniciar la aplicación
.venv/bin/python app.pyw
```

---

## 📖 Cómo se usa (Paso a paso)

1. **Abre el programa**: Ejecuta `Transcriptor.exe` o `app.pyw`.
2. **Carga tus audios**:
   - Haz clic en **"Seleccionar audio..."** o simplemente **arrastra y suelta** los archivos dentro de la ventana.
3. **Elige tus preferencias**:
   - **Modelo**: Déjalo en *"Preciso"* para la mejor calidad o cambia a *"Rápido"* si tienes prisa.
   - **Con tiempos**: Marca esta casilla si deseas ver los minutos y segundos de cada frase.
4. **Obtén tu resultado**:
   - Observa la transcripción en tiempo real.
   - Cuando termine y muestre el estado **"Listo"**, presiona **"Copiar todo"** o **"Guardar .txt..."**.

---

## 💻 Uso desde la Terminal

Si prefieres la consola o quieres automatizar tareas por lotes, utiliza `transcribir.py`:

```bash
# Transcribir un archivo individual
python transcribir.py "mi_audio.mp3"

# Transcribir y guardar el resultado en una carpeta específica
python transcribir.py "audio.ogg" --salida "mis_textos"

# Transcribir todos los audios de una carpeta
python transcribir.py "C:\AudiosGrabados"

# Transcribir con marcas de tiempo e indicar idioma español
python transcribir.py "entrevista.wav" --tiempos --idioma es

# Mover los audios ya procesados a otra carpeta
python transcribir.py "pendientes" --mover "procesados"
```

---

## 🛠️ Compilar el programa portable

Si modificaste el código y quieres generar tu propio ejecutable:

### En Windows / macOS
```bash
pip install pyinstaller
python compilar.py
```
El resultado estará listo en `dist/Transcriptor/`.

Para crear el paquete `.zip` distribuible:
```bash
python compilar.py --publicar
```

### En Linux con Docker (Multiplataforma)
Puedes compilar la versión de Linux desde cualquier sistema operativo teniendo Docker instalado:
```bash
docker build -f Dockerfile.linux -o dist .
```

---

## ❓ Preguntas frecuentes

<details>
<summary><b>¿Funciona con las notas de voz de WhatsApp?</b></summary>
<p>
¡Sí! Es uno de sus principales usos. Solo arrastra el archivo de audio de WhatsApp (generalmente formato <code>.ogg</code> u <code>.opus</code>) y la aplicación lo transcribirá perfectamente.
</p>
</details>

<details>
<summary><b>¿Cuánto tarda en transcribir?</b></summary>
<p>
Depende de la duración del audio y la potencia de tu equipo. En una computadora moderna estándar, un audio de 2 minutos suele tardar entre 30 y 60 segundos.
</p>
</details>

<details>
<summary><b>¿Necesito conexión a internet permanente?</b></summary>
<p>
No. Solo requieres conexión la primera vez que se descarga el modelo de voz. Luego de esa descarga inicial, el programa funcionará en modo avión o sin red de forma permanente.
</p>
</details>

<details>
<summary><b>¿Qué diferencia hay entre el modelo "Preciso" y "Rápido"?</b></summary>
<p>
El modelo <b>Preciso</b> (<code>large-v3-turbo</code>) ofrece la mayor fidelidad ortográfica, nombres propios y acentos. El modelo <b>Rápido</b> (<code>small</code>) procesa el audio en una fracción del tiempo usando menos memoria RAM, con una precisión muy buena para conversaciones cotidianas.
</p>
</details>

<details>
<summary><b>¿Mis datos o audios son almacenados o compartidos?</b></summary>
<p>
No. A diferencia de las APIs comerciales en la nube, todo el proceso de transcripción ocurre localmente en la memoria de tu computadora. Nadie más tiene acceso a tus archivos.
</p>
</details>

---

## 📂 Estructura del repositorio

| Archivo / Carpeta | Propósito |
|---|---|
| `app.pyw` | Interfaz gráfica de usuario (GUI con Tkinter) |
| `transcribir.py` | Motor de transcripción con Whisper (utilizable por GUI y CLI) |
| `compilar.py` | Script automatizado para empaquetar con PyInstaller |
| `Dockerfile.linux` | Contenedor para compilar la versión de Linux herméticamente |
| `requirements.txt` | Dependencias del proyecto en Python |
| `licencias/` | Licencias de terceros incluidas para distribución legal |

---

## 🤝 Colaboración y Comunidad

¿Encontraste un problema o tienes sugerencias de mejora? ¡Las contribuciones son bienvenidas!
- Revisa las pautas en [CONTRIBUTING.md](CONTRIBUTING.md).
- Abre un reporte o sugerencia en [Issues](../../issues).

---

## 📄 Licencia

Este proyecto está bajo la licencia **[GPL v3 o posterior](LICENSE)**, con una [excepción adicional](EXCEPCION-GPL.md) para componentes vinculados como OpenSSL e Intel OpenMP. Puedes usarlo, estudiarlo y modificarlo libremente.

Los detalles de bibliotecas de terceros y sus respectivas licencias se encuentran en [TERCEROS.md](TERCEROS.md).
