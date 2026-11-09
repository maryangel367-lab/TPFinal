import json

class StockInvalidoError(Exception):
    """Excepción para evitar stocks negativos"""
    def __init__(self, mensaje="El stock no puede ser un valor negativo."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class DispositivoEcologico:
    def __init__(self, nombre: str, precio: float, stock_inicial: int):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock_inicial  
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise StockInvalidoError(f"Error en '{self.nombre}': Intento de asignar stock negativo ({valor}).")
        self._stock = valor

    def generar_ficha_tecnica(self) -> str:
        return f"Dispositivo: {self.nombre} | Precio: ${self.precio} | Stock: {self.stock}"

class PanelSolar(DispositivoEcologico):
    def __init__(self, nombre: str, precio: float, stock_inicial: int, eficiencia: float, potencia: int):
        super().__init__(nombre, precio, stock_inicial)
        self.eficiencia = eficiencia
        self.potencia = potencia

    def generar_ficha_tecnica(self) -> str:
        return (f"--- FICHA COMERCIAL: PANEL SOLAR ---\n"
                f"Modelo: {self.nombre}\n"
                f"Potencia: {self.potencia}W | Eficiencia: {self.eficiencia}%\n"
                f"Precio: ${self.precio} | Disponibles: {self.stock} unidades\n"
                f"------------------------------------")


#B
class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos: list, ruta_archivo: str):
        """Serializa y almacena las instancias en un archivo JSON."""
        datos_serializados = []
        
        for dispositivo in lista_dispositivos:

            info_producto = {
                "nombre": dispositivo.nombre,
                "precio": dispositivo.precio,
                "stock": dispositivo.stock
            }
            
            if isinstance(dispositivo, PanelSolar):
                info_producto["eficiencia"] = dispositivo.eficiencia
                info_producto["potencia"] = dispositivo.potencia
                
            datos_serializados.append(info_producto)
        
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos_serializados, archivo, indent=4, ensure_ascii=False)
        print(f"\n[Éxito] Catálogo exportado correctamente a '{ruta_archivo}'.")

#Prueba
if __name__ == "__main__":
    print("=== INICIANDO PRUEBAS DE INVENTARIO ECOTECH ===\n")
    
    catalogo_valido = []

    try:
        panel_premium = PanelSolar("EcoPanel Ultra 400", 250.0, 15, eficiencia=21.5, potencia=400)
        panel_estandar = PanelSolar("EcoPanel Basic 300", 180.0, 8, eficiencia=18.2, potencia=300)
        
        catalogo_valido.append(panel_premium)
        catalogo_valido.append(panel_estandar)
        
        print(panel_premium.generar_ficha_tecnica())
        
    except StockInvalidoError as error:
        print(f"[Error inesperado]: {error}")

    print("\n--- Probando Validación de Negocio (Stock Negativo) ---")
    try:
        print(f"Modificando stock de {panel_estandar.nombre} a -5...")
        panel_estandar.stock = -5  # Esto disparará el Setter y lanzará la excepción
        
    except StockInvalidoError as error:
        print(f"[CAPTURA CONTROLADA]: {error}")
        print("El sistema bloqueó la operación. El stock original permanece intacto.")

    # validos
    GestorInventario.guardar_catalogo_json(catalogo_valido, "catalogo_ecotech.json")
