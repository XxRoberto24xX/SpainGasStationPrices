import requests
import json
import os

# 
# VARIABLE GLOBALES
# 
datos={} # Lista donde almacenaremos todas las gasolineras que nos devuelva el api


#
# 
# CONEXIÓN CON EL SERVIDOR Y OBTENCIÓN DE LA INFORMACIÓN 
# 
# 
def primera_conexion():
# Accedemos al servicio REST y recogemos la respuesta que este nos devuelva
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    respuesta = requests.get(url)

    # Comenzamos la ejecución del programa si la restpuesta que se nos devuelve es correcta
    if respuesta.status_code == 200:
        # Convertir la respuesta JSON en un diccionario
        global datos
        datos = respuesta.json()

        # Pedimos al usuario que acote la busqueda segun sus necesidades
        introduccion_de_datos()
    else:
        print(f"Error al consultar la API. Código de estado: {respuesta.status_code}")
        input("pulsa cualquier letra para acabar.......")

# 
# 
# PEDIDA DE DATOS AL USUARIO PARA PERSONALIZAR LA BUSQUEDA 
# 
#
def introduccion_de_datos():
    # Preguntaremos por la localidad y cadena de gasolinera que quiera el usuario
    provincia = input("Introduce el nombre de la provincia donde desea buscar (dejar en blanco para buscar todas): ")
    localidad = input("Introduce el nombre de la localidad donde desea buscar (dejar en blanco para buscar todas): ")
    tipoGasolinera = input("Introduce el nombre de la cadena de gasolineras específica a busacar (dejar en blanco para buscar todas): ")

    # Pedimos al usuario el tipo de combustible a consultar
    combustible=False

    while combustible==False:
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
                os.system('cls' if os.name == 'nt' else 'clear')
                print("La opción seleccionada no se encuentra entre las disponibles")
    
    #Una vez tenemos todos los datos que queremos podemos pasar a buscar en la base de datos que acabamos de obtener
    obterner_precios(provincia, localidad, tipoGasolinera, combustible)

# 
# 
# BUSQUEDA Y FILTRADO CON LOS DATOS OBTENIDOS
# 
#
def obterner_precios(provincia, localidad, tipoGasolinera, combustible):
    # Inicializamos una lista en la que guardar los resultados
    lista_gasolineras=[]

    # Filtrar por gasolineras en Salamanca de la compañía Repsol  --> como python usa short-circuit evaluation ponemos primero el caso de que el campo de filtrado este vacio
    for gasolinera in datos['ListaEESSPrecio']:
        if provincia == "" or gasolinera["Provincia"].lower() == provincia.lower():
            if localidad == "" or gasolinera["Localidad"].lower() == localidad.lower():
                if tipoGasolinera == "" or gasolinera["Rótulo"].lower() == tipoGasolinera.lower() or (tipoGasolinera.lower() == "repsol" and gasolinera["Rótulo"].lower() == "campsa"):
                    if gasolinera[combustible] != "":
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
    print()
    if len(gasolineras_ordenadas) == 0:
        print("No se encontraron coincidencias con esos datos")
    else:
        print("Resultados Obtenidos:")
        for gasolinera in gasolineras_ordenadas:
            print(f"Dirección: {gasolinera['nombre']}, Precio: {gasolinera['precio']} €/L, Enlace: {gasolinera['enlace_maps']}")

    # Acabamos la busqueda y preguntamos al usuario sobre que quiere hacer
    finalizacion_busqueda()

# 
# 
# FINALIZA LA BUSQUEDA Y PERIMITE AL USUARIO DECIDIR SI CERRAR LA APLICACIÓN    
# 
#
def finalizacion_busqueda():
    print()
    print()
    print("Busque finalizada, ¿desea realizar otra consulta?: ")
    print("S) Si")
    print("N) No, cerra la aplicación")

    opcion = input("Selecciona una opción: ")

    match opcion:
        case "S":
            os.system('cls' if os.name == 'nt' else 'clear')
            introduccion_de_datos()
        case "N":
            exit
        case _:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("La opción seleccionada no se encuentra entre las disponibles")
            finalizacion_busqueda()

# 
# 
# COMENZAMOS LA EJECUCIÓN DEL PROGRAMA 
# 
# 
primera_conexion()
