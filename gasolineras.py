import requests
import json

def obtener_precios_diesel():
    # Accedemos al servicio REST y recogemos la respuesta que este nos devuelva
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    respuesta = requests.get(url)

    # Comenzamos la ejecución del programa si la restpuesta que se nos devuelve es correcta
    if respuesta.status_code == 200:
        # Convertir la respuesta JSON en un diccionario
        datos = respuesta.json()
        
        # Lista donde almacenaremos las gasolineras que cumplen con las condiciones
        lista_gasolineras = []

        # Preguntaremos por la provincia y localidad de la gasolinera además del tipo de combustible y tipo de gasolinera a busacar
        provincia = input("Introduce el nombre de la provincia donde desea buscar: ")
        localidad = input("Introduce el nombre de la localidad donde desea buscar: ")
        tipoGasolinera = input("Introduce el nombre de la cadena de gasolineras específica a busacar: ")

        print("¿Que tipo de combustible desea busacar?:")
        print("A) Diesel")
        print("B) Diesel Premium")
        print("C) Diesel Agrícola")
        print("D) Gasolina 95 E5")
        print("E) Gasolina 95 E10")
        print("F) Gasolina 95 E5 Premium")
        print("G) Gasolina 98 E5")
        print("H) Gasolina 98 E10")
        opcion = input("Selecciona una opción: ")

        match opcion:
            case "A":
                combustible = "Precio Gasoleo A"
            case "B":
                combustible = "Precio Gasoleo Premium"
            case "C":
                combustible = "Precio Gasoleo B"
            case "D":
                combustible = "Precio Gasolina 95 E5"
            case "E":
                combustible = "Precio Gasolina 95 E10"
            case "F":
                combustible = "Precio Gasolina 95 E5 Premium"
            case "G":
                combustible = "Precio Gasolina 98 E5"
            case "H":
                combustible = "Precio Gasolina 98 E10"
            case _:
                combustible = "todos"

        # Filtrar por gasolineras en Salamanca de la compañía Repsol
        for gasolinera in datos['ListaEESSPrecio']:
            if gasolinera["Provincia"].lower() == provincia.lower or provincia == "":
                if gasolinera["Localidad"].lower() == localidad.lower or localidad == "":
                    if gasolinera["Rótulo"].lower() == tipoGasolinera.lower or tipoGasolinera == "":
                        #Sacamos la latitud y longitud de la gasolinera para sacar el enlace de googel maps
                        latitud = gasolinera['Latitud'].replace(',', '.')
                        longitud = gasolinera['Longitud (WGS84)'].replace(',', '.')
                        enlace_google_maps = f"https://www.google.com/maps?q={latitud},{longitud}"

                        #Añadimos la gasolinera a la lista
                        lista_gasolineras.append({
                            'nombre': gasolinera['Dirección'],
                            'precio': gasolinera[combustible],
                            'enlace_maps': enlace_google_maps
                        })
                    elif tipoGasolinera.lower == "repsol" and gasolinera["Rótulo"].lower() == "campsa":
                        #Sacamos la latitud y longitud de la gasolinera para sacar el enlace de googel maps
                        latitud = gasolinera['Latitud'].replace(',', '.')
                        longitud = gasolinera['Longitud (WGS84)'].replace(',', '.')
                        enlace_google_maps = f"https://www.google.com/maps?q={latitud},{longitud}"

                        #Añadimos la gasolinera a la lista
                        lista_gasolineras.append({
                            'nombre': gasolinera['Dirección'],
                            'precio': gasolinera[combustible],
                            'enlace_maps': enlace_google_maps
                        })


        # Ordenar las gasolineras por el precio del diésel
        gasolineras_ordenadas = sorted(lista_gasolineras, key=lambda x: x['precio'])

        # Imprimir los resultados con el enlace a Google Maps
        print("Gasolineras Repsol en Salamanca ordenadas por precio de diésel:")
        for gasolinera in gasolineras_ordenadas:
            print(f"Dirección: {gasolinera['nombre']}, Precio: {gasolinera['precio']} €/L, Enlace: {gasolinera['enlace_maps']}")
    
    else:
        print(f"Error al consultar la API. Código de estado: {respuesta.status_code}")

# Llamar a la función para obtener los precios
obtener_precios_diesel()

# Permite que el programa no acabe de mostra los datos hasta que el usuario quiera
input("Presiona enter para acabar...")
