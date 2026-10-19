# TranscribeNext - Copyright (C) 2026 jhoel0521
# Licencia: GPL v3 o posterior, con permiso adicional. Ver LICENSE y EXCEPCION-GPL.md.

"""Ventana intuitiva y moderna para transcribir audios con Whisper local."""

import os
import queue
import sys
from pathlib import Path

# El Python de Laragon trae Tcl/Tk en <python>\tcl pero no lo busca ahí; se lo indicamos.
_tcl = Path(sys.base_prefix) / "tcl"
for _var, _dir in (("TCL_LIBRARY", "tcl8.6"), ("TK_LIBRARY", "tk8.6")):
    if _var not in os.environ and (_tcl / _dir).is_dir():
        os.environ[_var] = str(_tcl / _dir)

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from transcribir import (
    EXTENSIONES,
    __version__,
    buscar_audios,
    cargar_modelo,
    carpeta_modelos,
    formato_tiempo,
    modelo_local,
    transcribir_audio,
)

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    TkinterDnD = None

TITULO_APP = f"TranscribeNext {__version__}"

MODELOS = {
    "🎯 Alta Precisión (Recomendado)": "large-v3-turbo",
    "⚡ Rápido (Menos memoria)": "small",
}

# Paleta de colores moderna
COLOR_FONDO = "#F8FAFC"
COLOR_TARJETA = "#FFFFFF"
COLOR_BORDE = "#E2E8F0"
COLOR_BORDE_DRAG = "#2563EB"
COLOR_TEXTO_TITULO = "#0F172A"
COLOR_TEXTO_MUTED = "#64748B"
COLOR_PRIMARIO = "#2563EB"
COLOR_EXITO = "#059669"
COLOR_PELIGRO = "#DC2626"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(TITULO_APP)
        self.root.geometry("880x640")
        self.root.minsize(620, 480)
        self.root.configure(bg=COLOR_FONDO)

        self.modelos_cargados = {}
        self.cola = queue.Queue()
        self.trabajando = False
        self.cancelar = threading.Event()
        self._descargando_modelo = False
        self._restablecer_copiar_timer = None

        self._configurar_estilos()
        self._construir_interfaz()

        # Configurar arrastrar y soltar si está disponible
        if hasattr(self.root, "drop_target_register"):
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind("<<DropEnter>>", self._al_entrar_arrastre)
            self.root.dnd_bind("<<DropLeave>>", self._al_salir_arrastre)
            self.root.dnd_bind("<<Drop>>", self._al_soltar)

        self.root.after(100, self._revisar_cola)

    def _configurar_estilos(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(".", background=COLOR_FONDO, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=COLOR_FONDO)
        self.style.configure("Card.TFrame", background=COLOR_TARJETA, relief="flat")

        # Botón primario (Azul destacado)
        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            background=COLOR_PRIMARIO,
            foreground="#FFFFFF",
            borderwidth=0,
            focuscolor="none",
            padding=(14, 8),
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#1D4ED8"), ("disabled", "#94A3B8")],
            foreground=[("disabled", "#E2E8F0")],
        )

        # Botón secundario estándar
        self.style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            background="#FFFFFF",
            foreground=COLOR_TEXTO_TITULO,
            borderwidth=1,
            relief="solid",
            padding=(12, 6),
        )
        self.style.map(
            "Secondary.TButton",
            background=[("active", "#F1F5F9"), ("disabled", "#F8FAFC")],
            foreground=[("disabled", "#94A3B8")],
        )

        # Botón de peligro (Cancelar)
        self.style.configure(
            "Danger.TButton",
            font=("Segoe UI", 10),
            background="#FEE2E2",
            foreground=COLOR_PELIGRO,
            borderwidth=0,
            padding=(10, 6),
        )
        self.style.map(
            "Danger.TButton",
            background=[("active", "#FECACA"), ("disabled", "#F1F5F9")],
            foreground=[("disabled", "#94A3B8")],
        )

        # Barra de progreso moderna
        self.style.configure(
            "Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background=COLOR_PRIMARIO,
            thickness=8,
            borderwidth=0,
        )

    def _construir_interfaz(self):
        # 1. Barra superior (Header)
        header = tk.Frame(self.root, bg=COLOR_TARJETA, highlightthickness=1, highlightbackground=COLOR_BORDE, padx=16, pady=10)
        header.pack(fill="x", side="top")

        # Título y Badge de privacidad
        header_izq = tk.Frame(header, bg=COLOR_TARJETA)
        header_izq.pack(side="left")

        lbl_logo = tk.Label(header_izq, text="🎙️", font=("Segoe UI Emoji", 16), bg=COLOR_TARJETA)
        lbl_logo.pack(side="left", padx=(0, 8))

        lbl_titulo = tk.Label(header_izq, text="TranscribeNext", font=("Segoe UI", 13, "bold"), fg=COLOR_TEXTO_TITULO, bg=COLOR_TARJETA)
        lbl_titulo.pack(side="left")

        lbl_badge = tk.Label(
            header_izq,
            text="100% Offline y Privado",
            font=("Segoe UI", 8, "bold"),
            fg="#047857",
            bg="#D1FAE5",
            padx=8,
            pady=2,
        )
        lbl_badge.pack(side="left", padx=(10, 0))

        # Controles derechos (Modelo y Tiempos)
        header_der = tk.Frame(header, bg=COLOR_TARJETA)
        header_der.pack(side="right")

        tk.Label(header_der, text="Modo:", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXTO_MUTED, bg=COLOR_TARJETA).pack(side="left", padx=(0, 6))
        self.var_modelo = tk.StringVar(value=next(iter(MODELOS)))
        self.combo_modelo = ttk.Combobox(
            header_der,
            textvariable=self.var_modelo,
            values=list(MODELOS),
            state="readonly",
            width=28,
            font=("Segoe UI", 9),
        )
        self.combo_modelo.pack(side="left", padx=(0, 12))

        self.var_tiempos = tk.BooleanVar(value=False)
        self.chk_tiempos = ttk.Checkbutton(header_der, text="⏱️ Con tiempos", variable=self.var_tiempos)
        self.chk_tiempos.pack(side="left")

        # 2. Contenedor central (Cambia entre vista Drop Zone y vista Transcripción)
        self.contenedor_central = tk.Frame(self.root, bg=COLOR_FONDO, padx=16, pady=12)
        self.contenedor_central.pack(fill="both", expand=True)

        self._crear_vista_drop()
        self._crear_vista_transcripcion()

        # Mostrar por defecto la vista de Drop / Inicio
        self.mostrar_vista_drop()

    def _crear_vista_drop(self):
        """Vista inicial grande y amigable para arrastrar o seleccionar audios."""
        self.vista_drop = tk.Frame(self.contenedor_central, bg=COLOR_FONDO)

        self.tarjeta_drop = tk.Frame(
            self.vista_drop,
            bg=COLOR_TARJETA,
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            padx=32,
            pady=48,
        )
        self.tarjeta_drop.pack(fill="both", expand=True)

        self.lbl_drop_icono = tk.Label(self.tarjeta_drop, text="📥", font=("Segoe UI Emoji", 48), bg=COLOR_TARJETA)
        self.lbl_drop_icono.pack(pady=(12, 10))

        self.lbl_drop_titulo = tk.Label(
            self.tarjeta_drop,
            text="Arrastra y suelta aquí tu audio",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXTO_TITULO,
            bg=COLOR_TARJETA,
        )
        self.lbl_drop_titulo.pack()

        self.lbl_drop_sub = tk.Label(
            self.tarjeta_drop,
            text="Notas de voz de WhatsApp, grabaciones de clases, entrevistas, canciones o podcasts",
            font=("Segoe UI", 10),
            fg=COLOR_TEXTO_MUTED,
            bg=COLOR_TARJETA,
        )
        self.lbl_drop_sub.pack(pady=(4, 20))

        self.btn_seleccionar_grande = ttk.Button(
            self.tarjeta_drop,
            text="📂 Seleccionar archivo de audio...",
            style="Primary.TButton",
            command=self.seleccionar,
        )
        self.btn_seleccionar_grande.pack(pady=(0, 24))

        # Píldoras de formatos soportados
        lbl_formatos = tk.Label(
            self.tarjeta_drop,
            text="Formatos: WhatsApp (.ogg, .opus) • MP3 • M4A • WAV • AAC • FLAC • MP4 • WEBM",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg=COLOR_TARJETA,
        )
        lbl_formatos.pack()

        lbl_tip = tk.Label(
            self.tarjeta_drop,
            text="💡 Consejo: Puedes arrastrar varios audios a la vez o una carpeta completa.",
            font=("Segoe UI", 9, "italic"),
            fg=COLOR_TEXTO_MUTED,
            bg=COLOR_TARJETA,
        )
        lbl_tip.pack(pady=(16, 0))

    def _crear_vista_transcripcion(self):
        """Vista activa con información del audio, barra de progreso y caja de texto."""
        self.vista_trans = tk.Frame(self.contenedor_central, bg=COLOR_FONDO)

        # Tarjeta superior de estado del audio
        self.tarjeta_estado = tk.Frame(
            self.vista_trans,
            bg=COLOR_TARJETA,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            padx=14,
            pady=10,
        )
        self.tarjeta_estado.pack(fill="x", pady=(0, 10))

        fila_estado = tk.Frame(self.tarjeta_estado, bg=COLOR_TARJETA)
        fila_estado.pack(fill="x")

        self.var_audio_actual = tk.StringVar(value="Preparando audio...")
        lbl_archivo = tk.Label(
            fila_estado,
            textvariable=self.var_audio_actual,
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_TEXTO_TITULO,
            bg=COLOR_TARJETA,
        )
        lbl_archivo.pack(side="left")

        self.var_badge_estado = tk.StringVar(value="Transcribiendo...")
        self.lbl_chip = tk.Label(
            fila_estado,
            textvariable=self.var_badge_estado,
            font=("Segoe UI", 8, "bold"),
            fg="#1E40AF",
            bg="#DBEAFE",
            padx=8,
            pady=2,
        )
        self.lbl_chip.pack(side="right")

        # Barra de progreso y porcentaje
        fila_progreso = tk.Frame(self.tarjeta_estado, bg=COLOR_TARJETA)
        fila_progreso.pack(fill="x", pady=(8, 4))

        self.progreso = ttk.Progressbar(fila_progreso, style="Horizontal.TProgressbar", maximum=100)
        self.progreso.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.var_porcentaje = tk.StringVar(value="0%")
        lbl_pct = tk.Label(
            fila_progreso,
            textvariable=self.var_porcentaje,
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXTO_MUTED,
            bg=COLOR_TARJETA,
            width=5,
        )
        lbl_pct.pack(side="right")

        self.var_detalle_estado = tk.StringVar(value="Iniciando motor de transcripción...")
        self.lbl_detalle = tk.Label(
            self.tarjeta_estado,
            textvariable=self.var_detalle_estado,
            font=("Segoe UI", 9),
            fg=COLOR_TEXTO_MUTED,
            bg=COLOR_TARJETA,
            anchor="w",
        )
        self.lbl_detalle.pack(fill="x")

        # Caja de texto enriquecida
        marco_texto = tk.Frame(self.vista_trans, bg=COLOR_TARJETA, highlightthickness=1, highlightbackground=COLOR_BORDE)
        marco_texto.pack(fill="both", expand=True)

        self.texto = ScrolledText(
            marco_texto,
            wrap="word",
            font=("Segoe UI", 11),
            undo=True,
            bg="#FFFFFF",
            fg=COLOR_TEXTO_TITULO,
            relief="flat",
            padx=12,
            pady=10,
        )
        self.texto.pack(fill="both", expand=True)
        self.texto.bind("<<Modified>>", self._al_modificar_texto)

        # Barra inferior de estadísticas y acciones
        barra_inferior = tk.Frame(self.vista_trans, bg=COLOR_FONDO, pady=10)
        barra_inferior.pack(fill="x")

        # Contador de palabras y caracteres
        self.var_stats = tk.StringVar(value="📝 0 palabras · 0 caracteres")
        lbl_stats = tk.Label(
            barra_inferior,
            textvariable=self.var_stats,
            font=("Segoe UI", 9),
            fg=COLOR_TEXTO_MUTED,
            bg=COLOR_FONDO,
        )
        lbl_stats.pack(side="left")

        # Botones de acción
        acciones = tk.Frame(barra_inferior, bg=COLOR_FONDO)
        acciones.pack(side="right")

        self.btn_copiar = ttk.Button(
            acciones,
            text="📋 Copiar texto",
            style="Primary.TButton",
            command=self.copiar,
        )
        self.btn_copiar.pack(side="left", padx=4)

        self.btn_guardar = ttk.Button(
            acciones,
            text="💾 Guardar .txt",
            style="Secondary.TButton",
            command=self.guardar,
        )
        self.btn_guardar.pack(side="left", padx=4)

        self.btn_nuevo = ttk.Button(
            acciones,
            text="🔄 Transcribir otro audio",
            style="Secondary.TButton",
            command=self.mostrar_vista_drop,
        )
        self.btn_nuevo.pack(side="left", padx=4)

        self.btn_limpiar = ttk.Button(
            acciones,
            text="🗑️ Limpiar",
            style="Secondary.TButton",
            command=self.limpiar_texto,
        )
        self.btn_limpiar.pack(side="left", padx=4)

        self.btn_cancelar = ttk.Button(
            acciones,
            text="⏹️ Cancelar",
            style="Danger.TButton",
            command=self.cancelar_transcripcion,
            state="disabled",
        )
        self.btn_cancelar.pack(side="left", padx=(8, 0))

    def mostrar_vista_drop(self):
        if self.trabajando:
            messagebox.showinfo("Procesando", "Hay una transcripción en curso. Cancélala si deseas volver al inicio.")
            return
        self.vista_trans.pack_forget()
        self.vista_drop.pack(fill="both", expand=True)
        self.root.title(TITULO_APP)

    def mostrar_vista_transcripcion(self):
        self.vista_drop.pack_forget()
        self.vista_trans.pack(fill="both", expand=True)

    def _actualizar_chip_estado(self, texto, tipo="info"):
        self.var_badge_estado.set(texto)
        if tipo == "exito":
            self.lbl_chip.configure(fg="#065F46", bg="#D1FAE5")
        elif tipo == "proceso":
            self.lbl_chip.configure(fg="#1E40AF", bg="#DBEAFE")
        elif tipo == "descarga":
            self.lbl_chip.configure(fg="#92400E", bg="#FEF3C7")
        elif tipo == "cancelado":
            self.lbl_chip.configure(fg="#475569", bg="#F1F5F9")
        elif tipo == "error":
            self.lbl_chip.configure(fg="#991B1B", bg="#FEE2E2")

    def _al_modificar_texto(self, _evento=None):
        if self.texto.edit_modified():
            contenido = self.texto.get("1.0", "end-1c").strip()
            palabras = len(contenido.split()) if contenido else 0
            caracteres = len(contenido)
            self.var_stats.set(f"📝 {palabras:,} palabras · {caracteres:,} caracteres")
            self.texto.edit_modified(False)

    def _bloquear_ui(self, trabajando):
        self.trabajando = trabajando
        self.combo_modelo.config(state="disabled" if trabajando else "readonly")
        self.chk_tiempos.config(state="disabled" if trabajando else "normal")
        self.btn_cancelar.config(state="normal" if trabajando else "disabled")
        self.btn_nuevo.config(state="disabled" if trabajando else "normal")
        self.btn_limpiar.config(state="disabled" if trabajando else "normal")

    # ---------- Acciones ----------

    def seleccionar(self):
        patron = " ".join(f"*{e}" for e in sorted(EXTENSIONES))
        archivos = filedialog.askopenfilenames(
            title="Seleccionar audios para transcribir",
            filetypes=[("Archivos de audio compatibles", patron), ("Todos los archivos", "*.*")],
        )
        if archivos:
            self.iniciar([Path(a) for a in archivos])

    def iniciar(self, archivos):
        if not archivos:
            return
        self.cancelar.clear()
        self.mostrar_vista_transcripcion()
        self._bloquear_ui(True)
        self.progreso["value"] = 0
        self.var_porcentaje.set("0%")
        self._actualizar_chip_estado("Iniciando...", "proceso")

        nombre_archivo = archivos[0].name if len(archivos) == 1 else f"{len(archivos)} audios seleccionados"
        self.var_audio_actual.set(f"🎵 {nombre_archivo}")

        modelo = MODELOS[self.var_modelo.get()]
        threading.Thread(
            target=self._transcribir_hilo,
            args=(archivos, modelo, self.var_tiempos.get()),
            daemon=True,
        ).start()

    def cancelar_transcripcion(self):
        self.cancelar.set()
        self.var_detalle_estado.set("Cancelando transcripción...")

    def limpiar_texto(self):
        self.texto.delete("1.0", "end")
        self.var_stats.set("📝 0 palabras · 0 caracteres")
        self.var_detalle_estado.set("Texto limpio.")

    def copiar(self):
        contenido = self.texto.get("1.0", "end-1c")
        if not contenido.strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(contenido)
        self.btn_copiar.configure(text="✅ ¡Copiado!")
        self.var_detalle_estado.set("Texto copiado al portapapeles con éxito.")

        if self._restablecer_copiar_timer:
            self.root.after_cancel(self._restablecer_copiar_timer)
        self._restablecer_copiar_timer = self.root.after(2000, lambda: self.btn_copiar.configure(text="📋 Copiar texto"))

    def guardar(self):
        contenido = self.texto.get("1.0", "end-1c")
        if not contenido.strip():
            messagebox.showinfo("Sin texto", "No hay texto transcrito para guardar.")
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Documento de texto (.txt)", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar transcripción como...",
        )
        if ruta:
            Path(ruta).write_text(contenido, encoding="utf-8")
            self.var_detalle_estado.set(f"Archivo guardado exitosamente en: {Path(ruta).name}")

    # ---------- Arrastrar y Soltar ----------

    def _al_entrar_arrastre(self, evento):
        if not self.trabajando:
            self.tarjeta_drop.configure(highlightbackground=COLOR_BORDE_DRAG)
            self.lbl_drop_titulo.configure(text="¡Suelta el audio aquí para transcribir!", fg=COLOR_PRIMARIO)
            self.lbl_drop_icono.configure(text="✨")
        return evento.action

    def _al_salir_arrastre(self, evento):
        if not self.trabajando:
            self.tarjeta_drop.configure(highlightbackground=COLOR_BORDE)
            self.lbl_drop_titulo.configure(text="Arrastra y suelta aquí tu audio", fg=COLOR_TEXTO_TITULO)
            self.lbl_drop_icono.configure(text="📥")
        return evento.action

    def _al_soltar(self, evento):
        self.tarjeta_drop.configure(highlightbackground=COLOR_BORDE)
        self.lbl_drop_titulo.configure(text="Arrastra y suelta aquí tu audio", fg=COLOR_TEXTO_TITULO)
        self.lbl_drop_icono.configure(text="📥")

        if self.trabajando:
            messagebox.showinfo("Ocupado", "Espera a que finalice la transcripción actual o haz clic en Cancelar.")
            return evento.action

        rutas = self.root.tk.splitlist(evento.data)
        audios = [a for a in buscar_audios(rutas) if a.suffix.lower() in EXTENSIONES]
        if audios:
            self.iniciar(audios)
        else:
            messagebox.showwarning(
                "Formato no compatible",
                "El archivo o carpeta soltado no contiene audios compatibles.\nFormatos soportados: MP3, OGG, OPUS, WAV, M4A, AAC, FLAC, MP4...",
            )
        return evento.action

    # ---------- Hilo de trabajo en segundo plano ----------

    def _transcribir_hilo(self, archivos, nombre_modelo, con_tiempos):
        try:
            if nombre_modelo not in self.modelos_cargados:
                descargado = modelo_local(nombre_modelo) or any(
                    carpeta_modelos().glob(f"models--*{nombre_modelo}*/snapshots/*/model.bin")
                )
                if descargado:
                    self.cola.put(("chip", ("Cargando modelo...", "proceso")))
                    self.cola.put(("detalle", f"Iniciando modelo local '{nombre_modelo}'..."))
                else:
                    self.cola.put(("chip", ("Descargando IA...", "descarga")))
                    self.cola.put((
                        "detalle",
                        "Descargando modelo de voz por primera vez (~1.5 GB)... Esto se hace solo UNA vez y luego funcionará para siempre sin internet. Por favor espera...",
                    ))
                    self.cola.put(("pulso_inicio", None))

                self.modelos_cargados[nombre_modelo] = cargar_modelo(nombre_modelo)
                self.cola.put(("pulso_fin", None))

            modelo = self.modelos_cargados[nombre_modelo]

            for i, audio in enumerate(archivos, 1):
                if self.cancelar.is_set():
                    break

                prefijo_lote = f"[{i}/{len(archivos)}] " if len(archivos) > 1 else ""
                self.cola.put(("audio_actual", f"🎵 {prefijo_lote}{audio.name}"))
                self.cola.put(("chip", ("Transcribiendo...", "proceso")))
                self.cola.put(("detalle", f"Procesando con Whisper en tu equipo..."))
                self.cola.put(("progreso", 0))

                if len(archivos) > 1:
                    self.cola.put(("texto", f"\n===== {audio.name} =====\n"))

                segmentos, info = transcribir_audio(modelo, audio, "es")
                for seg in segmentos:
                    if self.cancelar.is_set():
                        break
                    linea = seg.text.strip()
                    if con_tiempos:
                        linea = f"[{formato_tiempo(seg.start)}] {linea}"
                    self.cola.put(("texto", linea + ("\n" if con_tiempos else " ")))
                    if info.duration:
                        pct = min(100, (seg.end / info.duration) * 100)
                        self.cola.put(("progreso", pct))

                self.cola.put(("texto", "\n\n" if len(archivos) > 1 else "\n"))

            if self.cancelar.is_set():
                self.cola.put(("fin_cancelado", "Transcripción cancelada."))
            else:
                self.cola.put(("progreso", 100))
                self.cola.put(("fin_exito", "¡Listo! Transcripción finalizada con éxito."))

        except Exception as e:
            self.cola.put(("error", str(e)))

    def _revisar_cola(self):
        try:
            while True:
                tipo, valor = self.cola.get_nowait()
                if tipo == "texto":
                    self.texto.insert("end", valor)
                    self.texto.see("end")
                    self._al_modificar_texto()
                elif tipo == "audio_actual":
                    self.var_audio_actual.set(valor)
                elif tipo == "chip":
                    texto, variante = valor
                    self._actualizar_chip_estado(texto, variante)
                elif tipo == "detalle":
                    self.var_detalle_estado.set(valor)
                elif tipo == "progreso":
                    self.progreso["value"] = valor
                    self.var_porcentaje.set(f"{valor:.0f}%")
                    self.root.title(f"{valor:.0f}% - {TITULO_APP}")
                elif tipo == "pulso_inicio":
                    self.progreso.configure(mode="indeterminate")
                    self.progreso.start(10)
                elif tipo == "pulso_fin":
                    self.progreso.stop()
                    self.progreso.configure(mode="determinate")
                elif tipo == "fin_exito":
                    self._actualizar_chip_estado("Completado", "exito")
                    self.var_detalle_estado.set(valor)
                    self.root.title(f"Listo - {TITULO_APP}")
                    self._bloquear_ui(False)
                elif tipo == "fin_cancelado":
                    self._actualizar_chip_estado("Cancelado", "cancelado")
                    self.var_detalle_estado.set(valor)
                    self.root.title(f"Cancelado - {TITULO_APP}")
                    self._bloquear_ui(False)
                elif tipo == "error":
                    self._actualizar_chip_estado("Error", "error")
                    self.var_detalle_estado.set("Ocurrió un error al procesar el audio.")
                    self.root.title(f"Error - {TITULO_APP}")
                    self._bloquear_ui(False)
                    messagebox.showerror("Error de transcripción", f"No se pudo completar la operación:\n\n{valor}")
        except queue.Empty:
            pass
        self.root.after(100, self._revisar_cola)


if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("transcribe.next.app")

    root = None
    if TkinterDnD:
        try:
            root = TkinterDnD.Tk()
        except RuntimeError:
            root = None
    if root is None:
        root = tk.Tk()

    icono = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / "icono.ico"
    if sys.platform == "win32" and icono.exists():
        try:
            root.iconbitmap(default=str(icono))
        except Exception:
            pass

    app = App(root)

    # Audios pasados por argumentos o arrastrados al ejecutable
    iniciales = [a for a in buscar_audios(sys.argv[1:]) if a.suffix.lower() in EXTENSIONES]
    if iniciales:
        root.after(200, app.iniciar, iniciales)

    root.mainloop()
