# Determinantes del Empleo Informal en Ecuador: Un Análisis Probabilístico (Logit y Probit)

**Autor:** Camilo Pacheco  
**Materia:** Econometría Aplicada  
**Año:** 2026  

---

🌐 **Dashboard Web en Vivo:** [Ver Dashboard Interactivo] (https://proyecto-econometria-camilo-pacheco-drab.vercel.app/)

## 📌 1. Descripción del Problema
El empleo informal constituye uno de los principales retos estructurales del mercado laboral ecuatoriano. Este proyecto analiza cómo influyen factores socioeconómicos clave (educación, edad, sexo, área de residencia y estado civil) en la probabilidad de que un trabajador pertenezca al sector informal.

---

## 📊 2. Datos y Variables
La base de datos utiliza la estructura oficial de la Encuesta Nacional de Empleo, Desempleo y Subempleo (**ENEMDU - INEC**).

* **Variable Dependiente:** `informal` (1 = Sector Informal, 0 = Sector Formal).
* **Variables Explicativas:**
  * `anios_estudio`: Años de escolaridad acumulados.
  * `edad`: Edad del individuo (18-65 años).
  * `sexo`: Variable dummie (1 = Mujer, 0 = Hombre).
  * `area`: Variable dummie (1 = Urbana, 0 = Rural).
  * `casado`: Variable dummie (1 = Casado/Unión Libre, 0 = Otro).

---

## ⚙️ 3. Metodología Econométrica
Se estiman y comparan dos modelos de respuesta binaria:
1. **Modelo Logit:** Utiliza la función de distribución logística.
2. **Modelo Probit:** Utiliza la función de distribución normal estándar.

Se evalúa la bondad de ajuste mediante **AIC, BIC, Pseudo $R^2$** y capacidad predictiva con la **Curva ROC / AUC**.

---

## 📈 4. Principales Resultados
* **Criterio AIC:** Logit (1551.92) vs Probit (1553.09). El modelo Logit presenta un ajuste ligeramente superior.
* **Capacidad Discriminatoria:** Ambos modelos presentan un área bajo la curva ROC de $\approx 0.716$, demostrando un buen poder de clasificación.
* **Efectos Marginales Clave:** Cada año adicional de educación reduce significativamente la probabilidad de caer en la informalidad. Residir en zona urbana disminuye de forma sustancial el riesgo de empleo informal.

---

## 📁 5. Estructura del Repositorio
```text
PROYECTO_ECONOMETRIA_CAMILO_PACHECO/
├── data/
│   ├── raw/
│   └── diccionario_variables.md
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── results/
├── prompts/
│   └── registro_uso_ia.md
├── src/
│   ├── obtener_datos.py
│   ├── estimar_modelo.py
│   └── generar_resultados.py
├── README.md
└── requirements.txt
# 1. Clonar el repositorio
git clone <URL_DE_TU_REPOSOTORIO>

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar la base de datos
python src/obtener_datos.py

# 4. Estimar los modelos econométricos
python src/estimar_modelo.py

# 5. Exportar gráficos y tablas
python src/generar_resultados.py
3. Guarda con **`Ctrl` + `S`**.

---

### 2. Crear el Diccionario de Variables (`DATA/diccionario_variables.md`)

1. Despliega la carpeta **`DATA`** (o `data`) en el panel izquierdo.
2. Haz clic derecho sobre la carpeta **`DATA`** $\rightarrow$ **`New File`** y nómbralo: **`diccionario_variables.md`**.
3. Pega este texto adentro:

```markdown
# Diccionario de Variables - ENEMDU Informalidad

| Variable | Nombre Completo | Tipo | Descripción | Valores / Unidades |
| :--- | :--- | :--- | :--- | :--- |
| `informal` | Condición de Informalidad | Binaria | Identifica si el trabajador labora en el sector informal | 1 = Informal, 0 = Formal |
| `anios_estudio` | Años de Escolaridad | Numérica | Años de estudio completados | 0 a 18 años |
| `edad` | Edad | Numérica | Edad en años cumplidos | 18 a 65 años |
| `sexo` | Sexo | Binaria | Sexo de la persona | 1 = Mujer, 0 = Hombre |
| `area` | Zona Geográfica | Binaria | Dominio geográfico de residencia | 1 = Urbana, 0 = Rural |
| `casado` | Estado Civil | Binaria | Estado conyugal | 1 = Casado/Unión libre, 0 = Otro |
| `fexp` | Factor de Expansión | Numérica | Ponderador poblacional representativo | Valor continuo |