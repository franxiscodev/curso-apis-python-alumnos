import asyncio
import httpx
import time
from datetime import datetime

# -------------------------------------------------------------------
# PASO 1: Definimos las funciones para cada API
# Cada una obtiene un tipo específico de datos
# -------------------------------------------------------------------

async def obtener_usuario(user_id: int):
    """
    API #1: Obtiene datos de un usuario (JSONPlaceholder)
    """
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    print(f"  👤 Solicitando datos del usuario {user_id}...")

    async with httpx.AsyncClient() as cliente:
        respuesta = await cliente.get(url)
        respuesta.raise_for_status()

        datos = respuesta.json()
        print(f"  ✅ Usuario encontrado: {datos['name']} (de {datos['address']['city']})")
        return {
            "nombre": datos['name'],
            "email": datos['email'],
            "ciudad_origen": datos['address']['city'],
            "empresa": datos['company']['name']
        }

async def obtener_info_pais(nombre_pais: str):
    """
    API #2: Obtiene información de un país (REST Countries API)
    """
    # REST Countries API - búsqueda por nombre
    url = f"https://restcountries.com/v3.1/name/{nombre_pais}"

    print(f"  🌍 Buscando información de {nombre_pais}...")

    async with httpx.AsyncClient() as cliente:
        respuesta = await cliente.get(url)
        respuesta.raise_for_status()

        # La API devuelve un array, tomamos el primer resultado
        datos = respuesta.json()[0]

        # Extraemos información relevante
        capital = datos.get('capital', ['Desconocida'])[0]
        poblacion = datos.get('population', 0)
        moneda_info = list(datos.get('currencies', {}).values())
        moneda = moneda_info[0]['name'] if moneda_info else 'Desconocida'

        print(f"  ✅ País encontrado: {datos['name']['common']}")
        print(f"     Capital: {capital} | Población: {poblacion:,}")

        return {
            "nombre": datos['name']['common'],
            "capital": capital,
            "poblacion": poblacion,
            "continente": datos.get('region', 'Desconocido'),
            "moneda": moneda,
            "codigo_pais": datos.get('cca2', ''),  # Código de 2 letras (ej: FR, JP)
            "latitud": datos.get('latlng', [0, 0])[0] if datos.get('latlng') else 0,
            "longitud": datos.get('latlng', [0, 1])[1] if datos.get('latlng') else 0
        }

async def obtener_clima(ciudad: str, pais_codigo: str = "", lat: float = 0, lon: float = 0):
    """
    API #3: Obtiene el clima actual (Open-Meteo - gratuita, sin API key)
    Podemos pasar coordenadas directamente o buscar por ciudad
    """
    # Open-Meteo no requiere API key y es muy confiable
    # Si tenemos coordenadas del país, las usamos (aproximación a la capital)

    # Valores por defecto: París (coordenadas aproximadas de Europa)
    latitud = lat if lat != 0 else 48.8566
    longitud = lon if lon != 0 else 2.3522

    # Open-Meteo API para clima actual
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "current_weather": "true",
        "timezone": "auto",
        "hourly": "temperature_2m,relativehumidity_2m"  # Datos adicionales
    }

    print(f"  ☁️  Consultando clima en {ciudad}...")

    async with httpx.AsyncClient() as cliente:
        respuesta = await cliente.get(url, params=params)
        respuesta.raise_for_status()

        datos = respuesta.json()
        clima = datos.get('current_weather', {})

        # Determinar condición del clima basado en código WMO
        codigo_wmo = clima.get('weathercode', 0)
        condicion = interpretar_codigo_clima(codigo_wmo)

        print(f"  ✅ Clima obtenido: {clima.get('temperature', '?')}°C, {condicion}")

        return {
            "temperatura": clima.get('temperature', 'N/A'),
            "viento": clima.get('windspeed', 'N/A'),
            "direccion_viento": clima.get('winddirection', 'N/A'),
            "condicion": condicion,
            "hora_consulta": datetime.now().strftime("%H:%M:%S")
        }

def interpretar_codigo_clima(codigo: int) -> str:
    """
    Interpreta los códigos WMO de Open-Meteo
    """
    codigos = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna densa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada intensa",
        95: "Tormenta",
    }
    return codigos.get(codigo, f"Código {codigo}")

async def obtener_geocodificacion(ciudad: str, pais: str):
    """
    Función auxiliar para obtener coordenadas de una ciudad
    Usamos Open-Meteo Geocoding API (gratuita)
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": ciudad,
        "count": 1,
        "language": "es",
        "format": "json"
    }

    async with httpx.AsyncClient() as cliente:
        try:
            respuesta = await cliente.get(url, params=params)
            datos = respuesta.json()

            if datos.get('results'):
                resultado = datos['results'][0]
                return {
                    "lat": resultado['latitude'],
                    "lon": resultado['longitude'],
                    "nombre": resultado['name'],
                    "pais": resultado.get('country', 'Desconocido')
                }
        except:
            pass

    # Si no encontramos, devolvemos coordenadas por defecto (París)
    return {"lat": 48.8566, "lon": 2.3522, "nombre": ciudad, "pais": pais}

# -------------------------------------------------------------------
# PASO 2: Función principal que coordina TODO
# -------------------------------------------------------------------

async def planificar_viaje(usuario_id: int, destino: str):
    """
    Planifica un viaje consultando 3 APIs de manera concurrente
    """
    print(f"\n{'='*60}")
    print(f"🗺️  PLANIFICANDO VIAJE PARA USUARIO #{usuario_id} A {destino.upper()}")
    print(f"{'='*60}")

    inicio = time.time()

    # -------------------------------------------------------------------
    # PASO 2.1: PREPARAMOS TODAS LAS TAREAS
    # Nota: Obtenemos coordenadas primero (dependencia para el clima)
    # -------------------------------------------------------------------

    # Primero, obtenemos coordenadas del destino (necesario para clima preciso)
    print("\n📍 Obteniendo coordenadas del destino...")
    coordenadas = await obtener_geocodificacion(destino, "")

    if coordenadas:
        print(f"   Coordenadas de {coordenadas['nombre']}: {coordenadas['lat']:.2f}, {coordenadas['lon']:.2f}")

    # -------------------------------------------------------------------
    # PASO 2.2: LANZAMOS LAS 3 CONSULTAS CONCURRENTEMENTE
    # -------------------------------------------------------------------
    print("\n🔄 Consultando APIs de usuario, país y clima CONCURRENTEMENTE...")

    # Creamos las tareas
    tarea_usuario = obtener_usuario(usuario_id)
    tarea_pais = obtener_info_pais(destino)
    tarea_clima = obtener_clima(
        destino,
        lat=coordenadas['lat'] if coordenadas else 0,
        lon=coordenadas['lon'] if coordenadas else 0
    )

    # Ejecutamos TODAS concurrentemente con gather
    usuario, info_pais, clima = await asyncio.gather(
        tarea_usuario,
        tarea_pais,
        tarea_clima
    )

    tiempo_total = time.time() - inicio

    # -------------------------------------------------------------------
    # PASO 2.3: MOSTRAMOS EL RESULTADO COMBINADO
    # -------------------------------------------------------------------
    print(f"\n{'='*60}")
    print("📋 RESUMEN DEL VIAJE PLANIFICADO")
    print(f"{'='*60}")

    print(f"\n👤 VIAJERO: {usuario['nombre']}")
    print(f"   📧 Email: {usuario['email']}")
    print(f"   🏠 Ciudad de origen: {usuario['ciudad_origen']}")
    print(f"   💼 Trabaja en: {usuario['empresa']}")

    print(f"\n🌍 DESTINO: {info_pais['nombre']}")
    print(f"   🏛️  Capital: {info_pais['capital']}")
    print(f"   👥 Población: {info_pais['poblacion']:,} habitantes")
    print(f"   🌎 Continente: {info_pais['continente']}")
    print(f"   💰 Moneda: {info_pais['moneda']}")

    print(f"\n☁️  CLIMA AHORA EN {info_pais['capital']}:")
    print(f"   🌡️  Temperatura: {clima['temperatura']}°C")
    print(f"   💨 Viento: {clima['viento']} km/h")
    print(f"   ☁️  Condición: {clima['condicion']}")
    print(f"   🕐 Consulta: {clima['hora_consulta']}")

    print(f"\n⏱️  TIEMPO TOTAL: {tiempo_total:.2f} segundos")

    # Consejo de viaje personalizado
    print(f"\n💡 RECOMENDACIÓN DE VIAJE:")
    if "lluvia" in clima['condicion'].lower() or "tormenta" in clima['condicion'].lower():
        print(f"   🌂 Lleva paraguas! El clima en {info_pais['capital']} no es el mejor.")
    elif "nieve" in clima['condicion'].lower():
        print(f"   🧥 Abrígate bien! Está nevando en {info_pais['capital']}.")
    else:
        print(f"   😎 Buen clima para visitar {info_pais['capital']}! Disfruta tu viaje.")

    return {
        "usuario": usuario,
        "destino": info_pais,
        "clima": clima,
        "tiempo_total": tiempo_total
    }

# -------------------------------------------------------------------
# PASO 3: EJEMPLO CON MÚLTIPLES DESTINOS (para demostrar poder real)
# -------------------------------------------------------------------

async def planificar_viajes_multiples():
    """
    Planifica viajes para el mismo usuario a MÚLTIPLES destinos
    ¡Aquí es donde la concurrencia realmente brilla!
    """
    print("\n" + "🔥"*60)
    print("🔥 PLANIFICANDO VIAJES A MÚLTIPLES DESTINOS CONCURRENTEMENTE")
    print("🔥"*60)

    usuario_id = 3  # El mismo usuario para todos los viajes
    destinos = ["France", "Japan", "Brazil", "Australia", "Egypt"]

    inicio = time.time()

    # -------------------------------------------------------------------
    # Creamos UNA lista con TODAS las tareas de planificación
    # -------------------------------------------------------------------
    tareas_viajes = []
    for destino in destinos:
        # Importante: NO USAMOS await aquí, solo preparamos las tareas
        tarea = planificar_viaje(usuario_id, destino)
        tareas_viajes.append(tarea)

    # -------------------------------------------------------------------
    # Ejecutamos TODOS los viajes CONCURRENTEMENTE
    # -------------------------------------------------------------------
    print(f"\n🚀 Lanzando {len(tareas_viajes)} planificaciones de viaje CONCURRENTEMENTE...")
    print("   (Esto tomará el tiempo del viaje MÁS LENTO, no la suma de todos)")

    resultados = await asyncio.gather(*tareas_viajes)

    tiempo_total = time.time() - inicio

    # -------------------------------------------------------------------
    # Mostramos resumen comparativo
    # -------------------------------------------------------------------
    print(f"\n{'='*60}")
    print("📊 COMPARATIVA DE VIAJES")
    print(f"{'='*60}")

    for i, resultado in enumerate(resultados):
        destino = resultado['destino']['nombre']
        capital = resultado['destino']['capital']
        temp = resultado['clima']['temperatura']
        cond = resultado['clima']['condicion']
        print(f"{i+1}. {destino:<12} (Capital: {capital:<10}) | {temp:>4}°C | {cond:<15}")

    print(f"\n⏱️  TIEMPO TOTAL PARA {len(destinos)} VIAJES: {tiempo_total:.2f} segundos")
    print(f"   (Si fuera secuencial, tomaría aproximadamente {tiempo_total * len(destinos):.1f} segundos!)")

# -------------------------------------------------------------------
# PASO 4: EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------------

async def main():
    """
    Función principal que ejecuta todo el ejemplo
    """
    print("🚀 INICIO DEL SISTEMA DE PLANIFICACIÓN DE VIAJES")
    print("="*60)

    # -------------------------------------------------------------------
    # EJEMPLO 1: Viaje simple a un destino
    # -------------------------------------------------------------------
    resultado_viaje = await planificar_viaje(usuario_id=1, destino="Spain")

    # -------------------------------------------------------------------
    # EJEMPLO 2: Viaje con coordenadas específicas (ciudad exacta)
    # -------------------------------------------------------------------
    print("\n" + "🌆"*30)
    print("🌆 VIAJE A CIUDAD ESPECÍFICA: Barcelona")
    print("🌆"*30)

    # Para Barcelona, podemos obtener coordenadas más precisas
    inicio_bcn = time.time()

    # Obtenemos coordenadas de Barcelona
    coords_bcn = await obtener_geocodificacion("Barcelona", "Spain")

    # Consultas concurrentes
    tareas_bcn = [
        obtener_usuario(2),
        obtener_info_pais("Spain"),
        obtener_clima("Barcelona", lat=coords_bcn['lat'], lon=coords_bcn['lon'])
    ]

    usuario_bcn, pais_bcn, clima_bcn = await asyncio.gather(*tareas_bcn)

    print(f"\n📍 Viaje a Barcelona:")
    print(f"   👤 Viajero: {usuario_bcn['nombre']}")
    print(f"   🌍 País: {pais_bcn['nombre']}")
    print(f"   ☁️  Clima en Barcelona: {clima_bcn['temperatura']}°C, {clima_bcn['condicion']}")
    print(f"   ⏱️  Tiempo: {time.time() - inicio_bcn:.2f} segundos")

    # -------------------------------------------------------------------
    # EJEMPLO 3: Múltiples destinos (opcional - puede ser mucho output)
    # Descomenta la siguiente línea si quieres ver el ejemplo completo
    # -------------------------------------------------------------------
    await planificar_viajes_multiples()

    print(f"\n{'='*60}")
    print("✅ PROGRAMA FINALIZADO")
    print(f"{'='*60}")

# -------------------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Ejecutamos el programa asíncrono
    asyncio.run(main())
