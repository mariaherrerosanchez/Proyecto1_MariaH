# taximetro_MariaH
import time
import os

# Aquí nos añade la fecha de las carreras #
from datetime import datetime

def limpiar_pantalla():
    os.system("cls")

# Esta funcion nos sirve para guardar en un fichero el historial de las carreras #
def guardar_historial(tiempo_parado, tiempo_movimiento, tarifa_total):
    
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open("historial.txt", "a", encoding="utf-8") as archivo:
        
        archivo.write(
    f"{fecha} | "
    f"Parado: {tiempo_parado:.1f}s | "
    f"Movimiento: {tiempo_movimiento:.1f}s | "
    f"Total: €{tarifa_total:.2f}\n"
    )

# Esta función muestra el historial guardado
def mostrar_historial():

    try:
        with open("historial.txt", "r", encoding="utf-8") as archivo:

            contenido = archivo.read()

            print("\n📄 HISTORIAL DE TRAYECTOS:\n")
            print(contenido)

    except FileNotFoundError:
        print("❌ No existe historial todavía.")


###Aqui es donde podemos añadir el precio del combustible###

def calcula_tarifa(segundos_parado, segundos_movimiento, precio_combustible):
    """
    Calcular la tarifa total en euros.
    -Parado: 0.02€/seg
    -Movimiento: 0.05€/seg
    """
    tarifa_parado = 0.02 * precio_combustible
    tarifa_movimiento = 0.05 * precio_combustible

    tarifa = (segundos_parado * tarifa_parado + segundos_movimiento * tarifa_movimiento    )
    print(f"Este es el precio total: {tarifa}")
    return tarifa

def tarifa_en_vivo(tiempo_parado, tiempo_movimiento, precio_combustible):
    tarifa_parado = 0.02 * precio_combustible
    tarifa_movimiento = 0.05 * precio_combustible

    return (tiempo_parado * tarifa_parado +
            tiempo_movimiento * tarifa_movimiento)
    

def taximetro():

    limpiar_pantalla()

    """
    Funcion para usar y mostrar las opciones de nuestro taximetro.
    """
    print("""
====================================
         🚕 TAXÍMETRO MHS 🚕
====================================

Comandos disponibles:

▶ inicio            → iniciar carrera
▶ parado            → taxi detenido
▶ moviendonos       → taxi en movimiento
▶ findetrayecto     → finalizar viaje
▶ resumen_dia       → mostrar ganancias
▶ historial         → mostrar trayectos guardados
▶ salir             → cerrar programa

====================================
""")
    
    
    precio_combustible = float(input("Introduce el precio del combustible: "))
    print(f"⛽ Combustible actual: €{precio_combustible}")
    print(f"Precio combustible actualizado: €{precio_combustible}")
    viaje_activo = False
    inicio_carrera = 0
    tiempo_parado = 0
    Fin_carrera = 0
    tiempo_movimiento = 0
    estado = None # 'parado' o 'moviendonos'
    estado_inicio_carrera = 0
    ingresos_dia = []
    comandos_validos = [
    "inicio",
    "parado",
    "moviendonos",
    "findetrayecto",
    "resumen_dia",
    "historial",
    "salir"]
    

    while True:
        command = input ("> ").strip().lower()

        if command == "inicio":
            if viaje_activo:
                print("Error:la carrera ya ha comenzado")
                continue
            viaje_activo = True
            inicio_carrera = time.time()
            tiempo_parado = 0
            tiempo_movimiento = 0
            estado = 'parado'  # Iniciamos en estado 'parado'
            estado_inicio_carrera = time.time()
            print("La carrera ha comenzado. Estado inicial: 'parado' .")
        elif command == "resumen_dia":
            total = sum(ingresos_dia)
            print(f"Total ganado hoy: €{total:.2f}")
        
        elif command == "historial":
            mostrar_historial()
        
        elif command in ("parado", "moviendonos"):
            if not viaje_activo:
                print ("Error: No se ha iniciado la carrera. Por favor inicie carrera primero")
                continue
            # Calcula el tiempo del estado anterior
            duracion = time.time() - estado_inicio_carrera
            if estado == 'parado':
                tiempo_parado += duracion
            else:
                tiempo_movimiento += duracion
            
            # Cambia el estado #
            estado = 'parado' if command == "parado" else 'moviendonos'
            estado_inicio_carrera = time.time()
            print(f"El estado ha cambiado a '{estado}'.")

            tarifa_actual = tarifa_en_vivo(tiempo_parado, tiempo_movimiento, precio_combustible)
            print(f"💰 Tarifa actual: €{tarifa_actual:.2f}")

        elif command == "findetrayecto":
            
            if not viaje_activo:
                print("Error: No hay un viaje activo para finalizar")
                continue
            # Agrega tiempo del ultimo estado
            duracion = time.time() - estado_inicio_carrera
            if estado == 'parado':
                tiempo_parado += duracion
            else:
                tiempo_movimiento += duracion

                tarifa_actual = tarifa_en_vivo(tiempo_parado, tiempo_movimiento, precio_combustible)
            
            # Como calculamos la tarifa total y muestra el resumen del viaje #
            
            tarifa_total =  calcula_tarifa(tiempo_parado, tiempo_movimiento, precio_combustible)
            ingresos_dia.append(tarifa_total)

            guardar_historial(tiempo_parado, tiempo_movimiento, tarifa_total)


            print("""
            ========================
              🚕 TAXÍMETRO
            ========================

            --- RESUMEN DEL VIAJE ---
            """)

            print(f"🟡 Tiempo parado: {tiempo_parado:.1f} segundos")
            print(f"🟢 Tiempo en movimiento: {tiempo_movimiento:.1f} segundos")
            print(f"💰 Factura total: €{tarifa_total:.2f}")

            print("""
            ========================
            """)

            # Reseteamos las variables para el próximo viaje #
            viaje_activo = False
            estado = None
        elif command == "salir":
            print("Saliendo del programa.¡Hasta mañana!")
            break
        
        else:
            print("❌ Comando desconocido.")
            print("👉 Comandos válidos:")
            print(", ".join(comandos_validos))
    
            
            

if __name__ == "__main__":
    taximetro()









