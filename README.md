# Whisper GNOME

Frontend de escritorio para GNOME 44+ que envuelve el binario CLI de WhisperX con una cola de trabajos.

## Requisitos

En Ubuntu 24.04+ instala las dependencias base:

```
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 ffmpeg
```

El backend WhisperX se espera disponible como binario `whisperx` en el `PATH` (puedes instalarlo aparte). La aplicación arrancará aunque no esté presente.

## Entorno de desarrollo

Clona el repositorio y prepara el entorno Python 3.11+:

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Compila el esquema de GSettings al trabajar en local:

```
glib-compile-schemas data/
```

Si el esquema no se instala en el sistema, exporta la ruta antes de ejecutar:

```
export GSETTINGS_SCHEMA_DIR=$(pwd)/data
```

## Ejecución

Lanza la aplicación directamente con el comando instalado:

```
whisper-gnome
```

O desde el árbol de código sin instalar:

```
python -m whisper_gnome
```

## Estado

La lógica de ejecución de WhisperX está reemplazada por un stub que marca los trabajos como finalizados. La arquitectura está lista para integrar ffmpeg y WhisperX en el futuro.
