import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Charger le fichier CSV
file_path = 'C:/Users/fahim/Downloads/241204.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Constantes
T0 = 298.15  # Température de référence (K)
P0 = 1000.0  # Pression de référence (mbar)
cp = 1684   # Chaleur spécifique à pression constante pour propane (J/(mole.K)
R = 8.34     # Constante des gaz parfaits (J/(kg·K))
M = 44.097e-3  # Masse molaire de l'air (kg/mol)
gamma = 1.13  # Rapport des capacités calorifiques pour l'air

# Sélectionner les indices de 18744 à 21999 dans le fichier (index Python est 0 basé)
data_subset = data.iloc[18750:22000]

# Conversion des températures et pressions
data_subset.loc[:, 'T1_K'] = data_subset['AI A-1/T1 (°C)'] + 273.15
data_subset.loc[:, 'T2_K'] = data_subset['AI A-2/T2 (°C)'] + 273.15
data_subset.loc[:, 'T3_K'] = data_subset['AI B-6/AI B-6 (T3) (°C)'] + 273.15
data_subset.loc[:, 'T4_K'] = data_subset['AI A-4/T4 (°C)'] + 273.15
data_subset.loc[:, 'T5_K'] = data_subset['AI A-5/T5 (°C)'] + 273.15  # Température T5 depuis le fichier

data_subset.loc[:, 'P1_bar'] = data_subset['AI B-1/AI B-1 (Pamb) (mbar)'] / 1000
data_subset.loc[:, 'P2_bar'] = data_subset['AI B-2/AI B-2 (P2) (mbar)'] / 1000
data_subset.loc[:, 'P4_bar'] = data_subset['AI B-3/AI B-3 (P4) (mbar)'] / 1000
data_subset.loc[:, 'P3_bar'] = data_subset['P2_bar'] * (132660.8 / 133410.8)
  # Hypothèse : cycle ouvert, retour à la pression initiale

# Calcul de P5
# Hypothèse : P5 est proche de P4 dans un cycle ouvert
data_subset.loc[:, 'P5_bar'] = data_subset['P1_bar']

# Calcul de l'enthalpie massique
data_subset.loc[:, 'h1'] = cp * data_subset['T1_K']-cp*T0
data_subset.loc[:, 'h2'] = cp * data_subset['T2_K']-cp*T0
data_subset.loc[:, 'h3'] = cp * data_subset['T3_K']-cp*T0
data_subset.loc[:, 'h4'] = cp * data_subset['T4_K']-cp*T0
data_subset.loc[:, 'h5'] = cp * data_subset['T5_K']-cp*T0

# Calcul des entropies spécifiques



data_subset.loc[:, 's1'] = cp * np.log(data_subset['T1_K'] / T0) - (R / M) * np.log(data_subset['P1_bar'] * 1e3 / P0)
data_subset.loc[:, 's2'] = cp * np.log(data_subset['T2_K'] / T0) - (R / M) * np.log(data_subset['P2_bar'] * 1e3 / P0)
data_subset.loc[:, 's3'] = cp * np.log(data_subset['T3_K'] / T0) - (R / M) * np.log(data_subset['P3_bar'] * 1e3 / P0)
data_subset.loc[:, 's4'] = cp * np.log(data_subset['T4_K'] / T0) - (R / M) * np.log(data_subset['P4_bar'] * 1e3 / P0)
data_subset.loc[:, 's5'] = cp * np.log(data_subset['T5_K'] / T0) - (R / M) * np.log(data_subset['P5_bar'] * 1e3 / P0)



# Points du cycle (moyennes des données mesurées sur le sous-ensemble)


s_points = [
    data_subset['s1'].mean(),
    data_subset['s2'].mean(),
    data_subset['s3'].mean(),
    data_subset['s4'].mean(),
    data_subset['s5'].mean(),
    data_subset['s1'].mean()  # Retour à s1
]
T_points = [
    data_subset['T1_K'].mean(),
    data_subset['T2_K'].mean(),
    data_subset['T3_K'].mean(),
    data_subset['T4_K'].mean(),
    data_subset['T5_K'].mean(),
    data_subset['T1_K'].mean(),  # Retour à T1
]

# Calcul de la masse volumique à chaque point
data_subset['rho1'] = data_subset['P1_bar'].mean() * 1e5 / (R * T_points[0])  # en kg/m^3
data_subset['rho2'] = data_subset['P2_bar'].mean() * 1e5 / (R * T_points[1])
data_subset['rho3'] = data_subset['P3_bar'].mean() * 1e5 / (R * T_points[2])
data_subset['rho4'] = data_subset['P4_bar'].mean() * 1e5 / (R * T_points[3])
data_subset['rho5'] = data_subset['P5_bar'].mean() * 1e5 / (R * T_points[4])

# Affichage des valeurs calculées pour chaque point
points = {
    "Point": ["1", "2", "3", "4", "5"],
    "Température (K)": T_points[:-1],
    "Pression (bar)": [data_subset['P1_bar'].mean(), data_subset['P2_bar'].mean(), data_subset['P3_bar'].mean(),
                       data_subset['P4_bar'].mean(), data_subset['P5_bar'].mean()],
    "Entropie (J/(kg·K))": s_points[:-1]
}
results = pd.DataFrame(points)
print("Valeurs calculées pour chaque point du cycle :")
print(results)

# Tracé du diagramme T-s avec annotations des points
plt.figure(figsize=(10, 6))
plt.plot(s_points, T_points, marker='o', label='Cycle Brayton (5 points)')

# Annoter les points avec leur numéro
for i, (s, T) in enumerate(zip(s_points, T_points)):
    plt.annotate(f"{i + 1}", (s, T), textcoords="offset points", xytext=(5, 5), ha='center', fontsize=10)


Dm_air=(data_subset['AI B-5/AI B-5 (air) (kg/s)'].mean())
h1=data_subset.loc[:, 'h1'].mean()
h2=data_subset.loc[:, 'h2'].mean()
h3=data_subset.loc[:, 'h3'].mean()
h5=data_subset.loc[:, 'h5'].mean()
P_utile=Dm_air*((h3-h5)-(h2-h1))



# Configurer les axes et la légende
plt.title("Cycle thermodynamique Brayton - Diagramme T-s (5 points)")
plt.xlabel("Entropie spécifique $s$ (J/(kg·K))")
plt.ylabel("Température $T$ (K)")
plt.legend()
plt.grid(True)
plt.show()
print('masse vol 1' ,data_subset['rho1'].mean() )
print('masse vol 2' ,data_subset['rho2'].mean() )
print('masse vol 3' ,data_subset['rho3'].mean() )
print('masse vol 4' ,data_subset['rho4'].mean() )
print('masse vol 5' ,data_subset['rho5'].mean() )
print('h1' ,data_subset.loc[:, 'h1'].mean() )
print('h2' ,data_subset.loc[:, 'h2'].mean() )
print('h3' ,data_subset.loc[:, 'h3'].mean() )
print('h4' ,data_subset.loc[:, 'h4'].mean() )
print('h5' ,data_subset.loc[:, 'h5'].mean() )







