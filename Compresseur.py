import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

gamma = 1.4

# Charger le fichier CSV
file_path = 'C:/Users/fahim/Downloads/241204.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Filtrer les données entre les indices 18744 et 21999
data_filtered = data.iloc[18744:22000].copy()

# Conversion des températures et pressions
data_filtered['T1_K'] = data_filtered['AI A-1/T1 (°C)'] + 273.15
data_filtered['T2_K'] = data_filtered['AI A-2/T2 (°C)'] + 273.15
data_filtered['T3_K'] = data_filtered['AI B-6/AI B-6 (T3) (°C)'] + 273.15
data_filtered['T4_K'] = data_filtered['AI A-4/T4 (°C)'] + 273.15
data_filtered['T5_K'] = data_filtered['AI A-5/T5 (°C)'] + 273.15

data_filtered['P1_bar'] = data_filtered['AI B-1/AI B-1 (Pamb) (mbar)'] / 1000
data_filtered['P2_bar'] = data_filtered['AI B-2/AI B-2 (P2) (mbar)'] / 1000
data_filtered['P4_bar'] = data_filtered['AI B-3/AI B-3 (P4) (mbar)'] / 1000
data_filtered['P5_bar'] = data_filtered['P1_bar']  # Hypothèse : pression initiale au point 4 (cycle ouvert)

# Conversion du débit massique de kg/h en kg/s
data_filtered['mdot_kg_per_s'] = data_filtered['AI B-4/AI B-4 (gas) (kg/h)'] / 3600

# Moyennes des températures et pressions dans la plage spécifiée
T1 = data_filtered['T1_K'].mean()
T2 = data_filtered['T2_K'].mean()
T3 = data_filtered['T3_K'].mean()
T4 = data_filtered['T4_K'].mean()
T5 = data_filtered['T5_K'].mean()

P1 = data_filtered['P1_bar'].mean()
P2 = data_filtered['P2_bar'].mean()
P4 = data_filtered['P4_bar'].mean()
P3 = P4 * (T3 / T4) ** (gamma / (gamma - 1))
P5 = P1

# Moyenne du débit massique
mdot = data_filtered['mdot_kg_per_s'].mean()

# Constantes
R = 8.34# Constante des gaz parfaits

# Vérification des températures mesurées
if T2 <= T1:
    raise ValueError("T2 doit être supérieur à T1 pour un compresseur valide.")
if T3 <= T4:
    raise ValueError("T3 doit être supérieur à T4 pour une turbine valide.")

# Calcul du rapport de compression (π_c)
pi_c = P2 / P1

# Calcul de T2s (compression isentropique)
T2s = T1 * (1 / pi_c) ** ((1 - gamma) / gamma)

# Calcul du rendement isentropique du compresseur
eta_c = (T2s - T1) / (T2 - T1)

# Calcul du rapport de détente (π_t1)
pi_t1 = P4 / P3

# Calcul de T4s (détente isentropique)
T4s = T3 * ( pi_t1) ** ((1 - gamma) / gamma)

# Calcul du rendement isentropique de la turbine 1
eta_t1 = -(T3 - T4) / (T3 - T4s)

# Calcul du rapport de détente (π_t2)
pi_t2 = P1 / P4

# Calcul de T5s (détente isentropique)
T5s = T4 * (pi_t2) ** ((gamma - 1) / gamma)

# Calcul du rendement isentropique de la turbine 2
eta_t2 = -1 / ((T5 - T4) / (T4 - T5s))


mdot_fuel = data_filtered['AI B-4/AI B-4 (gas) (kg/h)'].mean()/3600
mdot_air = data_filtered['AI B-5/AI B-5 (air) (kg/s)'].mean()
cp=1000
P_turbine = mdot_air * cp * ((T3 - T4) * eta_t1 + (T4 - T5) * eta_t2)

# Puissance absorbée par le compresseur (Pc)
P_compresseur = mdot_fuel * cp * (T2 - T1) / eta_c

# Puissance thermique fournie par le combustible (Pfournie)
PCI = 46369e3  # Pouvoir calorifique inférieur (J/kg)
P_fournie =  mdot_fuel* PCI

# Puissance utile (Putile)
Pu=P_turbine-P_compresseur

# Rendement global


# Résultats
print(f"Rapport de compression (pi_c) : {pi_c:.2f}")
print(f"Rendement isentropique du compresseur (eta_c) : {eta_c:.2f}")
print(f"Rapport de détente (pi_t1) : {pi_t1:.2f}")
print(f"Rapport de détente (pi_t2) : {pi_t2:.2f}")
print(f"Rendement isentropique de la turbine 1 (eta_t1) : {eta_t1:.2f}")
print(f"Rendement isentropique de la turbine 2 (eta_t2) : {eta_t2:.2f}")
print("Rendement globale de la turbine : ",Pu/P_fournie)

