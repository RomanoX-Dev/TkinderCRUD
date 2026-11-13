from Dao.inventarioDAO import ProductoDAO

class ProductoControlador:
    def __init__(self):
        self.dao = ProductoDAO()

    def registrar_producto(self, nombre, descripcion, precio, stock):
    
        if not nombre or not precio or not stock:
            return False, "El nombre, precio y stock son obligatorios."
        
        try:
            precio_valido = float(precio)
            stock_valido = int(stock)
        except ValueError:
            return False, "El precio debe ser decimal y el stock un número entero."

        exito = self.dao.insertar_producto(nombre, descripcion, precio_valido, stock_valido)
        
        if exito:
            return True, "Producto registrado con éxito."
        else:
            return False, "Ocurrió un error al guardar en la base de datos."

    def listar_productos(self):
        return self.dao.obtener_productos()

    def modificar_producto(self, id_producto, nombre, descripcion, precio, stock):
        if not id_producto or not nombre or not precio or not stock:
            return False, "Faltan datos obligatorios."
        try:
            exito = self.dao.actualizar_producto(int(id_producto), nombre, descripcion, float(precio), int(stock))
            return (True, "Producto actualizado con éxito.") if exito else (False, "Error al actualizar.")
        except ValueError:
            return False, "El precio y stock deben ser numéricos."

    def borrar_producto(self, id_producto):
        if not id_producto:
            return False, "No se ha seleccionado ningún producto."
        exito = self.dao.eliminar_producto(int(id_producto))
        return (True, "Producto eliminado.") if exito else (False, "Error al eliminar.")