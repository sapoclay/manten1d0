import tkinter as tk
from tkinter import ttk

class ToolTip:
    """
    Clase para generar un tooltip en los botones creados.

    Uso:
        tooltip = ToolTip(widget, texto)

    Parámetros:
        widget (tkinter.Widget): El widget al que se asociará el tooltip.
        text (str): El texto que se mostrará en el tooltip.

    Métodos:
        show_tooltip(event=None):
            Muestra el tooltip cuando el cursor entra en el widget.
        hide_tooltip(event=None):
            Oculta el tooltip cuando el cursor sale del widget o se hace clic en él.
    """

    def __init__(self, widget, text):
        """
        Inicializa un tooltip para el widget especificado con el texto dado.

        Args:
            widget (tkinter.Widget): El widget al que se asociará el tooltip.
            text (str): El texto que se mostrará en el tooltip.
        """
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        # Vincula evento de clic del ratón para ocultar el tooltip al hacer clic en el botón
        self.widget.bind("<Button-1>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """
        Muestra el tooltip cuando el cursor entra en el widget.

        Args:
            event: El evento que desencadena la función (opcional).
        """
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, bg="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=5)

    def hide_tooltip(self, event=None):
        """
        Oculta el tooltip cuando el cursor sale del widget o se hace clic en él.

        Args:
            event: El evento que desencadena la función (opcional).
        """ 
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
