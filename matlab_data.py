import scipy.io
import pandas as pd
import numpy as np

# Load .mat file
mat_data = scipy.io.loadmat('netJointMomentKnee.mat')

# Extract the variables
x = mat_data['x_percentOfGaitCycle'].flatten()  # Flatten to make it 1D
y = mat_data['y_netJointMomentKnee'].flatten()

# Create a DataFrame
df = pd.DataFrame({
    'PercentOfGaitCycle': x,
    'NetJointMomentKnee': y
})

# Evenly sample 71 values from NetJointMomentKnee by index
indices = np.linspace(0, len(y) - 1, 71, dtype=int)
sampled_y = y[indices]

# Evenly sample corresponding PercentOfGaitCycle values
sampled_x = x[indices]

# Create a new DataFrame with sampled values
df_sampled = pd.DataFrame({
    'PercentOfGaitCycle': sampled_x,
    'SampledNetJointMomentKnee': sampled_y
})

# Write the DataFrame with sampled values to an Excel file
df_sampled.to_excel('sampled_output.xlsx', index=False)

print("Sampled DataFrame successfully written to sampled_output.xlsx")