from agents.mi_agente import EconometriaAgent

def ejecutar_proyecto():
    print("==================================================")
    print("   PROYECTO ECONOMETRÍA - INFORMALIDAD (ENEMDU)   ")
    print("==================================================\n")

    # 1. Instanciar al agente
    agente = EconometriaAgent(nombre="Agente-Camilo")

    # 2. Cargar el dataset de la ENEMDU
    ruta_datos = "DATA/raw/enemdu_informalidad.csv"
    agente.cargar_datos(ruta_datos)

    # 3. Generar la tabla descriptiva
    agente.generar_estadisticas_descriptivas(ruta_salida="outputs/tables/tabla_descriptiva.csv")

    # 4. Estimar modelo econométrico (Ajusta los nombres de tus variables si varían)
    # Ejemplo: si en tu CSV tienes la variable dependiente 'informalidad' y las independientes 'edad' e 'ingreso'
    # formula_econometrica = "informalidad ~ edad + ingreso"
    # agente.estimar_modelo_logit(formula=formula_econometrica)

    print("\n==================================================")
    print("🎉 ¡Todas las tareas fueron ejecutadas por el agente!")
    print("==================================================")

if __name__ == "__main__":
    ejecutar_proyecto()