import mariadb
import sys

class ProductoDAO:
    def __init__(self):
        try:
            self.conexion = mariadb.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3306,
                database="inventario"
            )
            print(f"Conectado a la base de datos exitosamente!")
            self.cursor = self.conexion.cursor()
        except mariadb.Error as error:
            print(f"Error al conectar con la base de datos: {error}")
            sys.exit(1)

    def insertar_producto(self, nombre, descripcion, precio, stock):
        try:
            query = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (nombre, descripcion, precio, stock))
            self.conexion.commit()
            return True
        except mariadb.Error as error_registro:
            print(f"Error en el registro: {error_registro}")
            return False
        
    def obtener_productos(self):
        try:
            query = "SELECT id, nombre, descripcion, precio, stock FROM productos"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mariadb.Error as error:
            print(f"Error al consultar: {error}")
            return []
    def actualizar_producto(self, id_producto, nombre, descripcion, precio, stock):
        try:
            query = "UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=? WHERE id=?"
            self.cursor.execute(query, (nombre, descripcion, precio, stock, id_producto))
            self.conexion.commit()
            return True
        except mariadb.Error as error:
            print(f"Error al actualizar: {error}")
            return False
            
    def eliminar_producto(self, id_producto):
        try:
            query = "DELETE FROM productos WHERE id=?"
            self.cursor.execute(query, (id_producto,))
            self.conexion.commit()
            return True
        except mariadb.Error as error:
            print(f"Error al eliminar: {error}")
            return False
        
    def cerrar_conexion(self):
        self.conexion.close()