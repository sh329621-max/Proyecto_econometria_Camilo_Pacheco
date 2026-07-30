import os
import numpy as np
import pandas as pd

def generar_datos_enemdu(n_observaciones=1500, seed=42):
    np.random.seed(seed)
    
    # Variables sociodemográficas oficiales (INEC - ENEMDU Ecuador)
    edad = np.random.randint(18, 65, size=n_observaciones)
    anios_estudio = np.random.randint(0, 19, size=n_observaciones)
    sexo = np.random.choice([0, 1], size=n_observaciones, p=[0.52, 0.48])  # 1: Mujer, 0: Hombre
    area = np.random.choice([0, 1], size=n_observaciones, p=[0.38, 0.62])  # 1: Urbana, 0: Rural
    casado = np.random.choice([0, 1], size=n_observaciones, p=[0.45, 0.55]) # 1: Casado/Unión libre
    
    # Probabilidad de estar en la informalidad según teoría económica
    z = 1.2 - 0.15 * anios_estudio - 0.02 * edad + 0.35 * sexo - 0.50 * area - 0.10 * casado
    probabilidad = 1 / (1 + np.exp(-z))
    informal = (np.random.rand(n_observaciones) < probabilidad).astype(int)
    factor_expansion = np.random.uniform(50, 500, size=n_observaciones).round(2)
    
    df = pd.DataFrame({
        'id_persona': range(1, n_observaciones + 1),
        'informal': informal,
        'anios_estudio': anios_estudio,
        'edad': edad,
        'sexo': sexo,
        'area': area,
        'casado': casado,
        'fexp': factor_expansion
    })
    
    # Detectar la carpeta de datos existente
    folder = 'DATA/raw' if os.path.exists('DATA') else 'data/raw'
    os.makedirs(folder, exist_ok=True)
    
    path = os.path.join(folder, 'enemdu_informalidad.csv')
    df.to_csv(path, index=False)
    print(f"✅ Base de datos generada exitosamente en '{path}'")

if __name__ == '__main__':
    generar_datos_enemdu()