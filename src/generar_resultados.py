import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import roc_curve, auc

def generar_graficos_y_tablas():
    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('outputs/tables', exist_ok=True)
    
    path_data = 'DATA/raw/enemdu_informalidad.csv' if os.path.exists('DATA/raw/enemdu_informalidad.csv') else 'data/raw/enemdu_informalidad.csv'
    df = pd.read_csv(path_data)
    
    # 1. Exportar Tabla Descriptiva
    desc = df[['informal', 'anios_estudio', 'edad', 'sexo', 'area', 'casado']].describe().T
    desc.round(2).to_csv('outputs/tables/tabla_descriptiva.csv')
    
    # 2. Estimación de Modelos para Gráficos
    y = df['informal']
    X = sm.add_constant(df[['anios_estudio', 'edad', 'sexo', 'area', 'casado']])
    
    logit_mod = sm.Logit(y, X).fit(disp=0)
    probit_mod = sm.Probit(y, X).fit(disp=0)
    
    p_logit = logit_mod.predict(X)
    p_probit = probit_mod.predict(X)
    
    # 3. Generar Curva ROC
    fpr_l, tpr_l, _ = roc_curve(y, p_logit)
    fpr_p, tpr_p, _ = roc_curve(y, p_probit)
    
    plt.figure(figsize=(7, 5))
    plt.plot(fpr_l, tpr_l, label=f'Logit (AUC = {auc(fpr_l, tpr_l):.3f})', color='#1f77b4', lw=2)
    plt.plot(fpr_p, tpr_p, label=f'Probit (AUC = {auc(fpr_p, tpr_p):.3f})', color='#2ca02c', linestyle='--', lw=2)
    plt.plot([0, 1], [0, 1], color='gray', linestyle=':')
    plt.xlabel('Tasa de Falsos Positivos')
    plt.ylabel('Tasa de Verdaderos Positivos')
    plt.title('Curva ROC - Rendimiento Predictivo Logit vs Probit')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/figures/curva_roc.png', dpi=300)
    plt.close()
    
    # 4. Generar Gráfico de Efectos Marginales Probit
    me_probit = probit_mod.get_margeff(at='overall').summary_frame()
    vars_names = ['Años Estudio', 'Edad', 'Sexo (Mujer)', 'Área (Urbana)', 'Casado']
    me_probit['Variable'] = vars_names
    
    plt.figure(figsize=(8, 4.5))
    sns.barplot(data=me_probit, x='dy/dx', y='Variable', color='#2b5c8f')
    plt.axvline(0, color='red', linestyle='--')
    plt.title('Efectos Marginales Promedio (Modelo Probit)')
    plt.xlabel('Cambio en la probabilidad de informalidad (dy/dx)')
    plt.ylabel('Variable Explicativa')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/figures/efectos_marginales.png', dpi=300)
    plt.close()
    
    print("✅ Gráficos guardados en 'outputs/figures/'")
    print("✅ Tabla descriptiva guardada en 'outputs/tables/'")

if __name__ == '__main__':
    generar_graficos_y_tablas()