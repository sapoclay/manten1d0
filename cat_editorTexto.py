import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
 
class EditorTextos:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto")
        self.root.geometry("800x600")

        self.create_menu()
        self.create_text_area()
        self.create_status_bar()
        self.create_context_menu()
        self.update_word_and_char_count()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.exit_program)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Buscar", command=self.search_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Deshacer", command=self.undo)
        edit_menu.add_command(label="Rehacer", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Copiar (Ctrl+C)", command=self.copy_text)
        edit_menu.add_command(label="Pegar (Ctrl+V)", command=self.paste_text)
        menu_bar.add_cascade(label="Opciones", menu=edit_menu)

    def create_text_area(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.line_numbers = tk.Label(frame, width=4, bg="lightgrey", anchor='nw')
        self.line_numbers.pack(side="left", fill="y")

        self.text_area = tk.Text(frame, wrap="word", undo=True)
        self.text_area.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.text_area.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self.text_area.bind("<Key>", self.update_line_numbers)
        self.text_area.bind("<KeyRelease>", self.update_word_and_char_count)
        self.text_area.bind("<Button-3>", self.show_context_menu)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_word_and_char_count()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copiar", command=self.copy_text)
        self.context_menu.add_command(label="Pegar", command=self.paste_text)
        self.context_menu.add_command(label="Deshacer", command=self.undo)
        self.context_menu.add_command(label="Rehacer", command=self.redo)
        self.context_menu.add_command(label="Buscar", command=self.search_text)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def update_line_numbers(self, event=None):
        lines = self.text_area.get("1.0", "end-1c").split('\n')
        line_numbers_text = "\n".join(str(i + 1) for i in range(len(lines)))
        self.line_numbers.config(text=line_numbers_text)

    def update_word_and_char_count(self, event=None):
        text = self.text_area.get("1.0", "end-1c")
        words = len(text.split())
        characters = len(text)
        self.status_bar.config(text=f"Palabras: {words}  Caracteres: {characters}")

    def new_file(self):
        self.text_area.delete(1.0, "end")
        self.update_line_numbers()
        self.update_word_and_char_count()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, "end")
                self.text_area.insert("end", content)
            self.update_line_numbers()
            self.update_word_and_char_count()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, "end"))

    def exit_program(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.destroy()

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def undo(self):
        self.text_area.edit_undo()

    def redo(self):
        self.text_area.edit_redo()

    def search_text(self):
        search_query = simpledialog.askstring("Buscar", "Escribe el texto a buscar:")
        if search_query:
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(search_query, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_query)}c"
                self.text_area.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            self.text_area.tag_config("highlight", background="yellow", foreground="black")

def main():
    root = tk.Tk()
    editor = EditorTextos(root)
    root.mainloop()

if __name__ == "__main__":
    main()