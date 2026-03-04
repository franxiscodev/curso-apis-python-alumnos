import asyncio
import httpx
import time

# -------------------------------------------------------------------
# PASO 1: Definimos las funciones asíncronas para cada API
# Cada función es independiente y hace una sola cosa
# -------------------------------------------------------------------

async def obtener_usuario(user_id: int):
    """
    Obtiene información de un usuario desde JSONPlaceholder
    Esta API es rápida, pero simularemos que puede tomar tiempo
    """
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    print(f"  🔍 Solicitando usuario {user_id}...")

    # async with = contexto asíncrono para manejar el cliente HTTP
    async with httpx.AsyncClient() as cliente:
        # await = esperamos la respuesta, pero mientras tanto...
        # ...el programa puede hacer otras cosas
        respuesta = await cliente.get(url)

        # Verificamos que la petición fue exitosa
        respuesta.raise_for_status()

        datos = respuesta.json()
        print(f"  ✅ Usuario {user_id} obtenido: {datos['name']}")
        return datos

async def obtener_pokemon(nombre: str):
    """
    Obtiene información de un Pokémon desde PokéAPI
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"

    print(f"  🔍 Solicitando Pokémon: {nombre}...")

    async with httpx.AsyncClient() as cliente:
        respuesta = await cliente.get(url)
        respuesta.raise_for_status()

        datos = respuesta.json()
        print(f"  ✅ Pokémon {nombre} obtenido (altura: {datos['height']})")
        return datos

# -------------------------------------------------------------------
# PASO 2: Función principal que ejecuta ambas llamadas CONCURRENTEMENTE
# -------------------------------------------------------------------

async def main():
    """
    Función principal que coordina la ejecución de ambas tareas
    """
    print("🚀 INICIO DEL PROGRAMA")
    inicio_total = time.time()

    # -------------------------------------------------------------------
    # EJEMPLO 1: Llamadas SECUENCIALES (una después de otra)
    # Esto es lo que NO debemos hacer en código asíncrono
    # -------------------------------------------------------------------
    print("\n📋 EJEMPLO 1: Llamadas SECUENCIALES (lento) 🐢")
    inicio_secuencial = time.time()

    # Primero esperamos al usuario
    usuario = await obtener_usuario(1)

    # Luego esperamos al pokémon (no empezamos hasta que termine el usuario)
    pokemon = await obtener_pokemon("pikachu")

    fin_secuencial = time.time()
    print(f"  ⏱️  Tiempo secuencial: {fin_secuencial - inicio_secuencial:.2f} segundos")

    # Mostramos resultados combinados
    print(f"  📊 Resultado: {usuario['name']} quiere un {pokemon['name'].capitalize()}")

    # -------------------------------------------------------------------
    # EJEMPLO 2: Llamadas CONCURRENTES con asyncio.gather()
    # Esto es lo CORRECTO en programación asíncrona
    # -------------------------------------------------------------------
    print("\n📋 EJEMPLO 2: Llamadas CONCURRENTES (rápido) ⚡")
    inicio_concurrente = time.time()

    # Creamos las tareas pero NO las await todavía
    # Simplemente preparamos las corrutinas
    tarea_usuario = obtener_usuario(2)
    tarea_pokemon = obtener_pokemon("charizard")

    # asyncio.gather() ejecuta TODAS las tareas CONCURRENTEMENTE
    # y espera a que TODAS terminen
    usuario2, pokemon2 = await asyncio.gather(
        tarea_usuario,
        tarea_pokemon
    )

    fin_concurrente = time.time()
    print(f"  ⏱️  Tiempo concurrente: {fin_concurrente - inicio_concurrente:.2f} segundos")

    # Mostramos resultados combinados
    print(f"  📊 Resultado: {usuario2['name']} quiere un {pokemon2['name'].capitalize()}")

    # -------------------------------------------------------------------
    # EJEMPLO 3: Múltiples llamadas a la MISMA API con gather
    # Esto muestra el verdadero poder de la concurrencia
    # -------------------------------------------------------------------
    print("\n📋 EJEMPLO 3: Múltiples Pokémon CONCURRENTES 🔥💧🌿")
    inicio_multiple = time.time()

    # Lista de Pokémon para buscar
    pokemons = ["bulbasaur", "charmander", "squirtle", "pikachu", "eevee"]

    # Creamos una lista de tareas dinámicamente
    tareas_pokemon = [obtener_pokemon(p) for p in pokemons]

    # Ejecutamos TODAS concurrentemente
    resultados_pokemon = await asyncio.gather(*tareas_pokemon)  # El * desempaqueta la lista

    fin_multiple = time.time()
    print(f"  ⏱️  Tiempo para 5 Pokémon: {fin_multiple - inicio_multiple:.2f} segundos")

    # Mostramos los nombres de los Pokémon obtenidos
    nombres = [p['name'].capitalize() for p in resultados_pokemon]
    print(f"  📊 Pokémon obtenidos: {', '.join(nombres)}")

    # -------------------------------------------------------------------
    # RESUMEN FINAL
    # -------------------------------------------------------------------
    fin_total = time.time()
    print(f"\n🏁 TIEMPO TOTAL DEL PROGRAMA: {fin_total - inicio_total:.2f} segundos")

    print("\n" + "="*60)
    print("📚 EXPLICACIÓN DE LO QUE ACABA DE PASAR:")
    print("="*60)
    print("• Las llamadas a APIs externas son operaciones de I/O (Entrada/Salida)")
    print("• En el EJEMPLO 1, perdimos tiempo esperando secuencialmente")
    print("• En el EJEMPLO 2, ambas APIs se llamaron AL MISMO TIEMPO")
    print("• El tiempo del EJEMPLO 2 fue el de la API MÁS LENTA, no la suma")
    print("• En el EJEMPLO 3, ¡5 Pokémon se obtuvieron casi al mismo tiempo!")
    print("• asyncio.gather() es como un 'lanzador' de tareas concurrentes")

# -------------------------------------------------------------------
# PASO 3: Función auxiliar para medir tiempos (opcional)
# -------------------------------------------------------------------
async def llamada_con_timeout():
    """
    Ejemplo extra: Cómo manejar timeouts con httpx
    """
    print("\n⏰ EJEMPLO EXTRA: Timeout en peticiones")
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:  # Timeout de 2 segundos
            # Esta API es lenta a propósito para probar timeouts
            respuesta = await client.get("https://httpbin.org/delay/3")
            print("  Esto no se imprimirá porque la API tarda 3 segundos")
    except httpx.TimeoutException:
        print("  ⚠️  La petición excedió el tiempo de espera (timeout)")

# -------------------------------------------------------------------
# PASO 4: Ejecutar el programa
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Punto de entrada: ejecutamos la función main()
    # asyncio.run() crea el bucle de eventos y ejecuta nuestra corrutina
    asyncio.run(main())

    # Ejemplo extra de timeout (opcional, descomentar para probar)
    # asyncio.run(llamada_con_timeout())
