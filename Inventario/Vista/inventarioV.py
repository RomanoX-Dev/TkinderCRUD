from tkinter import *
from tkinter import ttk, messagebox
from Controladores.inventarioCON import ProductoControlador

class VistaInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario de Productos")
        self.root.geometry("600x550") # Ventana más grande para que quepa la tabla
        
        self.controlador = ProductoControlador()
        self.id_seleccionado = None # Para saber qué producto editar o borrar

        # Título
        Label(self.root, text="Gestión de Inventario", font="calibri 16 bold", fg="blue").pack(pady=10)

        # Frame para los inputs
        frame_inputs = Frame(self.root)
        frame_inputs.pack(pady=5)

        Label(frame_inputs, text="Nombre").grid(row=0, column=0, pady=5, padx=5)
        self.e_nombre = Entry(frame_inputs)
        self.e_nombre.grid(row=0, column=1, pady=5, padx=5)

        Label(frame_inputs, text="Descripción").grid(row=1, column=0, pady=5, padx=5)
        self.e_descripcion = Entry(frame_inputs)
        self.e_descripcion.grid(row=1, column=1, pady=5, padx=5)

        Label(frame_inputs, text="Precio ($)").grid(row=2, column=0, pady=5, padx=5)
        self.e_precio = Entry(frame_inputs)
        self.e_precio.grid(row=2, column=1, pady=5, padx=5)

        Label(frame_inputs, text="Cantidad (Stock)").grid(row=3, column=0, pady=5, padx=5)
        self.e_stock = Entry(frame_inputs)
        self.e_stock.grid(row=3, column=1, pady=5, padx=5)

        # Frame para botones
        frame_botones = Frame(self.root)
        frame_botones.pack(pady=10)

        Button(frame_botones, text="Registrar", command=self.registrar, bg="green", fg="white").grid(row=0, column=0, padx=5)
        Button(frame_botones, text="Actualizar", command=self.actualizar, bg="orange").grid(row=0, column=1, padx=5)
        Button(frame_botones, text="Eliminar", command=self.eliminar, bg="red", fg="white").grid(row=0, column=2, padx=5)
        Button(frame_botones, text="Limpiar Campos", command=self.limpiar_campos).grid(row=0, column=3, padx=5)

        # NUEVO: Tabla para consultar datos (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Descripción", "Precio", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        
        self.tree.column("ID", width=30)
        self.tree.column("Nombre", width=120)
        self.tree.column("Descripción", width=150)
        self.tree.column("Precio", width=80)
        self.tree.column("Stock", width=80)
        
        self.tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Evento: Al hacer clic en una fila, rellenar los Entry
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_fila)

        # Cargar los datos al iniciar la ventana
        self.cargar_tabla()

    def limpiar_campos(self):
        self.e_nombre.delete(0, END)
        self.e_descripcion.delete(0, END)
        self.e_precio.delete(0, END)
        self.e_stock.delete(0, END)
        self.id_seleccionado = None

    def cargar_tabla(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for fila in self.tree.get_children():
            self.tree.delete(fila)
        
        productos = self.controlador.listar_productos()
        for p in productos:
            self.tree.insert("", END, values=p)

    def seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            valores = self.tree.item(seleccion)['values']
            self.limpiar_campos()
            
            self.id_seleccionado = valores[0]
            self.e_nombre.insert(0, valores[1])
            self.e_descripcion.insert(0, valores[2])
            self.e_precio.insert(0, valores[3])
            self.e_stock.insert(0, valores[4])

    def registrar(self):
        exito, msj = self.controlador.registrar_producto(
            self.e_nombre.get(), self.e_descripcion.get(), self.e_precio.get(), self.e_stock.get()
        )
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.limpiar_campos()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", msj)

    def actualizar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla para actualizar.")
            return

        exito, msj = self.controlador.modificar_producto(
            self.id_seleccionado, self.e_nombre.get(), self.e_descripcion.get(), self.e_precio.get(), self.e_stock.get()
        )
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.limpiar_campos()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", msj)

    def eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla para eliminar.")
            return
            
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este producto?")
        if respuesta:
            exito, msj = self.controlador.borrar_producto(self.id_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_campos()
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", msj)