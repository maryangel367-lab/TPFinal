import unittest
from django.shortcuts import render

def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo eléctrico no puede ser negativo.")
    return consumo_kwh * factor_emision


class TestCalculoEmisiones(unittest.TestCase):
    
    def test_calculo_nominal(self):
        """Prueba que 200 kWh den 80.0 kg de CO2."""
        resultado = calcular_emisiones_carbono(200)
        self.assertEqual(resultado, 80.0)

    def test_consumo_negativo_lanza_error(self):
        """Probar que un consumo negativo muestre un ValueError."""
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-10)

def obtener_metricas_consumo(registros):
    """Procesa el historial de consumos por planta industrial."""
    total_global_emisiones = 0.0
    planta_mayor_consumo = None
    max_consumo = -1
    
    for reg in registros:
        planta = reg["planta"]
        consumo = reg["consumo"]
        emisiones_planta = calcular_emisiones_carbono(consumo)
        total_global_emisiones += emisiones_planta
        if consumo > max_consumo:
            max_consumo = consumo
            planta_mayor_consumo = planta
            
    return {
        "total_emisiones": total_global_emisiones,
        "planta_max": planta_mayor_consumo
    }


def vista_panel_sustentabilidad(request):
    # Historial
    registros_eco = [
        {"planta": "Planta Norte", "consumo": 200},
        {"planta": "Planta Sur", "consumo": 500},
        {"planta": "Planta Este", "consumo": 100},
    ]
    metricas = obtener_metricas_consumo(registros_eco)
    contexto = {
        "total_global_co2": metricas["total_emisiones"],
        "planta_lider_consumo": metricas["planta_max"],
        "listado_completo": registros_eco
    }
    
    # plantilla
    return render(request, 'sustentabilidad/panel.html', contexto)
#ejecutar
if __name__ == '__main__':
    unittest.main()