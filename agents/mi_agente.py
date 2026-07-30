import os
import json
import pandas as pd
import statsmodels.formula.api as smf

class EconometriaAgent:
    """
    Agente inteligente encargado de automatizar el procesamiento de datos,
    generación de estadísticas descriptivas y estimación de modelos econométricos.
    """
    def __init__(self, nombre="EconometraBot"):
        self.nombre = nombre
        self.data = None

    def cargar_datos(self, ruta_csv):
        """Carga el dataset CSV en memoria."""
        print(f"🤖 [{self.nombre}]: Cargando datos desde {ruta_csv}...")
        if os.path.exists(ruta_csv):
            self.data = pd.read_csv(ruta_csv)
            print(f"  └─ ✅ Datos cargados exitosamente. ({len(self.data)} filas, {len(self.data.columns)} columnas)")
            return self.data
        else:
            print(f"  └─ ❌ Error: No se encontró el archivo en '{ruta_csv}'")
            return None

    def generar_estadisticas_descriptivas(self, ruta_salida="outputs/tables/tabla_descriptiva.csv"):
        """Genera el resumen estadístico de las variables y lo guarda en CSV."""
        if self.data is None:
            print(f"🤖 [{self.nombre}]: ⚠️ Primero debes cargar los datos.")
            return None

        print(f"🤖 [{self.nombre}]: Calculando estadísticas descriptivas...")
        descriptivas = self.data.describe().T
        
        # Crear la carpeta de salida si no existe
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        descriptivas.to_csv(ruta_salida)
        
        print(f"  └─ ✅ Tabla descriptiva guardada en: {ruta_salida}")
        return descriptivas

    def estimar_modelo_logit(self, formula, ruta_salida="outputs/results/model_summary.json"):
        """
        Estima un modelo Logit/Probabilístico según la fórmula indicada 
        y guarda los coeficientes y métricas en formato JSON.
        """
        if self.data is None:
            print(f"🤖 [{self.nombre}]: ⚠️ Primero debes cargar los datos.")
            return None

        print(f"🤖 [{self.nombre}]: Estimando modelo con fórmula: '{formula}'...")
        try:
            # Estimación del modelo Logit
            modelo = smf.logit(formula=formula, data=self.data).fit(disp=False)
            
            resumen = {
                "formula": formula,
                "nobs": int(modelo.nobs),
                "prsquared": round(float(modelo.prsquared), 4),
                "aic": round(float(modelo.aic), 2),
                "bic": round(float(modelo.bic), 2),
                "coeficientes": {k: round(v, 4) for k, v in modelo.params.to_dict().items()},
                "p_values": {k: round(v, 4) for k, v in modelo.pvalues.to_dict().items()}
            }

            os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
            with open(ruta_salida, "w", encoding="utf-8") as f:
                json.dump(resumen, f, indent=4, ensure_ascii=False)

            print(f"  └─ ✅ Resultados del modelo guardados en: {ruta_salida}")
            return modelo

        except Exception as e:
            print(f"  └─ ⚠️ Ocurrió un error al estimar el modelo: {e}")
            return None