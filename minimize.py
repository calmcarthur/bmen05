import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Load data from the Excel file
data = pd.read_excel('data.xlsx')

# Extract the relevant columns from the DataFrame
angle = data['angle'].values  # Extract angle values
angular_acceleration = data['angular acceleration'].values  # Extract angular acceleration values
NJM = data['njm'].values  # Extract NJM values

# PCSA values from the table (in cm^2)
PCSA_values = {
    'ili': 0.00054,  # Iliopsoas
    'rec': 0.00109, # Rectus
    'glu': 0.0026, # Glutei
    'ham': 0.0015  # Hamstring
}

# Define the objective functions for each minimization criteria
def objective_a(x):
    return sum(x)

def objective_b(x):
    return sum(f**2 for f in x)

def objective_c(x):
    return sum(f**3 for f in x)

def objective_d(x):
    return sum((f / PCSA_values[key])**2 for f, key in zip(x, PCSA_values))

def constraint(x, angle, angular_acceleration, NJM):
    Fili, Frec, Fglu, Fham = x
    return (0.05 * Fili) + (0.034 * Frec) - (0.062 * Fglu) - (0.072 * Fham) - \
           (NJM + (19.84 * np.sin(np.deg2rad(angle))) + 
            (0.6539 * angular_acceleration))

# Set initial guesses for Fili, Frec, Fglu, Fham
initial_guess = [1.0, 1.0, 1.0, 1.0]

# Optimization results storage
results = []

# Loop over each time step
for i in range(len(angle)):
    # Define constraints for the current time step
    cons = ({'type': 'eq', 'fun': constraint, 'args': (angle[i], angular_acceleration[i], NJM[i])})
    
    # Minimize using different objectives
    res_a = minimize(objective_a, initial_guess, constraints=cons)
    res_b = minimize(objective_b, initial_guess, constraints=cons)
    res_c = minimize(objective_c, initial_guess, constraints=cons)
    res_d = minimize(objective_d, initial_guess, constraints=cons)
    
    # Store results for each minimization criterion
    results.append({
        'min_a': res_a.x,
        'min_b': res_b.x,
        'min_c': res_c.x,
        'min_d': res_d.x
    })

# Add results to the DataFrame
for idx, result in enumerate(results):
    data.loc[idx, 'min_a_ili'], data.loc[idx, 'min_a_rec'], data.loc[idx, 'min_a_glu'], data.loc[idx, 'min_a_ham'] = result['min_a']
    data.loc[idx, 'min_b_ili'], data.loc[idx, 'min_b_rec'], data.loc[idx, 'min_b_glu'], data.loc[idx, 'min_b_ham'] = result['min_b']
    data.loc[idx, 'min_c_ili'], data.loc[idx, 'min_c_rec'], data.loc[idx, 'min_c_glu'], data.loc[idx, 'min_c_ham'] = result['min_c']
    data.loc[idx, 'min_d_ili'], data.loc[idx, 'min_d_rec'], data.loc[idx, 'min_d_glu'], data.loc[idx, 'min_d_ham'] = result['min_d']

# Save the updated DataFrame to a new Excel file or overwrite the existing one
data.to_excel('data_updated.xlsx', index=False)