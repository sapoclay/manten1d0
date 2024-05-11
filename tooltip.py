import tkinter as tk
from tkinter import ttk

# Clase para generar el tooltip en los botones creados 
# Ejemplo: ToolTip(nombre_del_boton, "Texto del tooltip")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        # Vincula evento de clic del ratón para ocultar el tooltip al hacer clic en el botón
        self.widget.bind("<Button-1>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, bg="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=5)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
