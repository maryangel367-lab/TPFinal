#PUNTO A
def limpiar_registro_sensor(registro_raw):
    
    id_limpio = registro_raw["sensor_id"].strip()

    temp_sin_c = registro_raw["temperatura"].replace("C", "")
    temp_numerica = float(temp_sin_c)
    
 
    ubicacion_limpia = registro_raw.get("ubicacion", "Desconocida")
    

    diccionario_limpio = {
        "sensor_id": id_limpio,
        "temperatura": temp_numerica,
        "ubicacion": ubicacion_limpia
    }

    return diccionario_limpio
#PUNTO B
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    lista_sensores_alerta = []
    
    suma_temperaturas = 0.0
    
    for sensor in lista_sensores_limpios:
        suma_temperaturas += sensor["temperatura"]
        
        if sensor["temperatura"] > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])
            
    promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    
    return (lista_sensores_alerta, promedio_temperatura)
if __name__ == "__main__":
    datos_crudos = [
        {"sensor_id": "  SENSOR-001  ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": " SENSOR-002 ", "temperatura": "36.2C", "ubicacion": "Planta Sur"},
        {"sensor_id": "SENSOR-003", "temperatura": "18.0C"}, # Este no tiene ubicación
        {"sensor_id": "  SENSOR-004  ", "temperatura": "42.1C", "ubicacion": "Planta Este"}
    ]
    
    lista_limpia = []
    for registro in datos_crudos:
        registro_sanitizado = limpiar_registro_sensor(registro)
        lista_limpia.append(registro_sanitizado)
        
    umbral = 30.0
    alertas, promedio = generar_resumen_sensores(lista_limpia, umbral)
    
    print("--- REPORTE CONSOLIDADO DE ECOTECH SOLUTIONS ---")
    print(f"Sensores en alerta (superan los {umbral}°C): {alertas}")
    print(f"Promedio térmico global de la planta: {promedio:.2f}°C")