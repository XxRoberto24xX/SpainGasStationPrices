from curl_cffi import requests
import json
import os
from datetime import datetime
import time

# 
# VARIABLE GLOBALES
# 
datos = {}  # Lista donde almacenaremos todas las gasolineras que nos devuelva el API
DIRECTORIO_CACHE = os.path.join(os.path.expanduser("~"), ".gasprice")
ARCHIVO_CACHE = os.path.join(DIRECTORIO_CACHE, "datos_gasolineras.json")


#
# VERIFICACION DE LA VALIDEZ TEMPORAL DE LOS DATOS
#
def isDatosActulalizados(fecha_hora_str):
    # Parsear la fecha y hora del cache
    try:
        fecha_str, hora_str = fecha_hora_str.split(" ")
        dia, mes, anio = map(int, fecha_str.split("/"))
        hora, minuto, segundo = map(int, hora_str.split(":"))
        
        fecha_hora_cache = datetime(anio, mes, dia, hora, minuto, segundo)
        ahora = datetime.now()
        
        # Verificar si es el mismo día
        if fecha_hora_cache.date() != ahora.date():
            return False
            
        # Calcular diferencia de tiempo
        diferencia = ahora - fecha_hora_cache
        diferencia_minutos = diferencia.total_seconds() / 60
        
        # Si han pasado menos de 30 minutos y estamos en el mismo intervalo de actualización
        if diferencia_minutos < 30:
            # Verificar si ambos momentos están en el mismo intervalo de 30 minutos
            # (ambos antes o después de la media hora)
            cache_interval = fecha_hora_cache.minute // 30
            ahora_interval = ahora.minute // 30
            
            if cache_interval == ahora_interval:
                return True
        
        return False
    except:
        return False


#
# 
# CONEXIÓN CON EL SERVIDOR Y OBTENCIÓN DE LA INFORMACIÓN 
# 
# 
def primera_conexion():
    # Crear el directorio de cache si no existe
    if not os.path.exists(DIRECTORIO_CACHE):
        os.makedirs(DIRECTORIO_CACHE)

    # Verificar si ya existe un archivo con datos del día actual
    if os.path.exists(ARCHIVO_CACHE):
        with open(ARCHIVO_CACHE, "r", encoding="utf-8") as archivo:
            global datos
            datos = json.load(archivo)
            fecha_hora_cache = datos["Fecha"]
            if isDatosActulalizados(fecha_hora_cache):
                print("Datos recuperados de Cache")
                introduccion_de_datos()
                return
            else:
                print("Obteniendo datos del api")

    # Accedemos al servicio REST y recogemos la respuesta que este nos devuelva
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "sedeaplicaciones.minetur.gob.es",
        "Sec-Ch-Ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
        
    max_reintentos = 3
    for intento in range(max_reintentos):
        try:
            respuesta = requests.get(
                url,
                headers=headers,
                impersonate="chrome110"  # Imita perfectamente a Chrome
            )

            # Comenzamos la ejecución del programa si la respuesta que se nos devuelve es correcta
            if respuesta.status_code == 200:
                # Convertir la respuesta JSON en un diccionario
                datos = respuesta.json()

                # Guardar los datos en un archivo JSON con la fecha actual
                with open(ARCHIVO_CACHE, "w", encoding="utf-8") as archivo:
                    json.dump(datos, archivo, ensure_ascii=False, indent=4)

                introduccion_de_datos()
            else:
                print(f"Error al consultar la API. Código de estado: {respuesta.status_code}")
                input("Pulsa cualquier tecla para finalizar...")
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                print(f"Intento {intento + 1} fallido: {e}")
                if intento < max_reintentos - 1:
                    time.sleep(5)  # Espera 5 segundos antes de reintentar
                else:
                    print("Demasiados intentos fallidos. Verifica tu conexión o la disponibilidad de la API.")
                    input("Pulsa cualquier tecla para finalizar...")
                    exit()
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
    print("N) No, cerrar la aplicación")

    opcion = input("Selecciona una opción: ")

    match opcion:
        case "S":
            os.system('cls' if os.name == 'nt' else 'clear')
            introduccion_de_datos()
        case "N":
            exit()
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
