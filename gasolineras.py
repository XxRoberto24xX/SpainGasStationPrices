import requests
import json

def obtener_precios_diesel():
    # URL de la API del Ministerio de Transición Ecológica
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"

    # Hacer la petición a la API
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        # Convertir la respuesta JSON en un diccionario
        datos = respuesta.json()
        
        # Lista donde almacenaremos las gasolineras que cumplen con las condiciones
        gasolineras_repsol_salamanca = []

        # Filtrar por gasolineras en Salamanca de la compañía Repsol
        for gasolinera in datos['ListaEESSPrecio']:
            if gasolinera['Provincia'].lower() == 'salamanca' and gasolinera['Rótulo'].lower() == 'repsol':
                # Obtener el precio del diésel
                precio_diesel = gasolinera['Precio Gasoleo A']
                
                # Obtener las coordenadas de la gasolinera y reemplazar las comas por puntos
                latitud = gasolinera['Latitud'].replace(',', '.')
                longitud = gasolinera['Longitud (WGS84)'].replace(',', '.')

                # Generar el enlace de Google Maps
                enlace_google_maps = f"https://www.google.com/maps?q={latitud},{longitud}"

                # Añadir la gasolinera con el precio de diésel y el enlace de Google Maps
                gasolineras_repsol_salamanca.append({
                    'nombre': gasolinera['Dirección'],
                    'precio_diesel': precio_diesel,
                    'enlace_maps': enlace_google_maps
                })

        # Ordenar las gasolineras por el precio del diésel
        gasolineras_repsol_salamanca_ordenadas = sorted(gasolineras_repsol_salamanca, key=lambda x: x['precio_diesel'])

        # Imprimir los resultados con el enlace a Google Maps
        print("Gasolineras Repsol en Salamanca ordenadas por precio de diésel:")
        for gasolinera in gasolineras_repsol_salamanca_ordenadas:
            print(f"Dirección: {gasolinera['nombre']}, Precio: {gasolinera['precio_diesel']} €/L, Enlace: {gasolinera['enlace_maps']}")
    
    else:
        print(f"Error al consultar la API. Código de estado: {respuesta.status_code}")

# Llamar a la función para obtener los precios
obtener_precios_diesel()

input("Presiona enter para acabar...")
