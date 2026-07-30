import os
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score, accuracy_score

def estimar_modelos():
    # 1. Cargar datos
    path_data = 'DATA/raw/enemdu_informalidad.csv' if os.path.exists('DATA/raw/enemdu_informalidad.csv') else 'data/raw/enemdu_informalidad.csv'
    
    if not os.path.exists(path_data):
        print("⚠️ No se encontró la base de datos. Ejecutando obtener_datos.py...")
        from obtener_datos import generar_datos_enemdu
        generar_datos_enemdu()

    df = pd.read_csv(path_data)
    
    # 2. Definir variables
    y = df['informal']
    X = df[['anios_estudio', 'edad', 'sexo', 'area', 'casado']]
    X_const = sm.add_constant(X)
    
    # 3. Estimación Logit
    modelo_logit = sm.Logit(y, X_const).fit(disp=0)
    me_logit = modelo_logit.get_margeff(at='overall').summary_frame()
    
    # 4. Estimación Probit
    modelo_probit = sm.Probit(y, X_const).fit(disp=0)
    me_probit = modelo_probit.get_margeff(at='overall').summary_frame()
    
    # 5. Predicciones y Métricas Predictivas
    pred_logit_prob = modelo_logit.predict(X_const)
    pred_probit_prob = modelo_probit.predict(X_const)
    
    pred_logit_bin = (pred_logit_prob >= 0.5).astype(int)
    pred_probit_bin = (pred_probit_prob >= 0.5).astype(int)
    
    auc_logit = roc_auc_score(y, pred_logit_prob)
    auc_probit = roc_auc_score(y, pred_probit_prob)
    
    acc_logit = accuracy_score(y, pred_logit_bin)
    acc_probit = accuracy_score(y, pred_probit_bin)
    
    # Convertir efectos marginales de forma segura
    me_logit_dict = me_logit.round(4).to_dict(orient='index')
    me_probit_dict = me_probit.round(4).to_dict(orient='index')
    
    # 6. Estructurar Resultados para el Dashboard y Minipaper
    resultados = {
        "logit": {
            "aic": round(float(modelo_logit.aic), 2),
            "bic": round(float(modelo_logit.bic), 2),
            "pseudo_r2": round(float(modelo_logit.prsquared), 4),
            "auc": round(float(auc_logit), 4),
            "accuracy": round(float(acc_logit), 4),
            "efectos_marginales": me_logit_dict
        },
        "probit": {
            "aic": round(float(modelo_probit.aic), 2),
            "bic": round(float(modelo_probit.bic), 2),
            "pseudo_r2": round(float(modelo_probit.prsquared), 4),
            "auc": round(float(auc_probit), 4),
            "accuracy": round(float(acc_probit), 4),
            "efectos_marginales": me_probit_dict
        }
    }
    
    # Guardar en outputs/results
    folder_out = 'outputs/results'
    os.makedirs(folder_out, exist_ok=True)
    
    with open(os.path.join(folder_out, 'model_summary.json'), 'w') as f:
        json.dump(resultados, f, indent=4)
        
    print("✅ Modelos Logit y Probit estimados con éxito.")
    print("📊 Resultados guardados en 'outputs/results/model_summary.json'")
    
    # Resumen impreso en pantalla
    print("\n" + "="*50)
    print("          COMPARACIÓN DE MODELOS ECONOMÉTRICOS")
    print("="*50)
    print(f" LOGIT  -> AIC: {resultados['logit']['aic']} | Pseudo R2: {resultados['logit']['pseudo_r2']} | ROC AUC: {resultados['logit']['auc']}")
    print(f" PROBIT -> AIC: {resultados['probit']['aic']} | Pseudo R2: {resultados['probit']['pseudo_r2']} | ROC AUC: {resultados['probit']['auc']}")
    print("="*50)

if __name__ == '__main__':
    estimar_modelos()