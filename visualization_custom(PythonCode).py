import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable

# Set seed for reproducibility
np.random.seed(12345)

# Generate sample data
df = pd.DataFrame([np.random.normal(32000, 20000, 3650), 
                   np.random.normal(43000, 10000, 3650), 
                   np.random.normal(43500, 14000, 3650), 
                   np.random.normal(48000, 7000, 3650)], 
                  index=[1992, 1993, 1994, 1995])

# Calculate mean and standard deviation
mean_values = df.mean(axis=1)
std_dev = df.std(axis=1)

# Define y-value of interest
y_interest = 39541.52

# Create a colormap ranging from blue to white to red
cmap = plt.get_cmap('coolwarm')

# Adjust the normalization to make the transitions between blue and red sharper
norm = mcolors.Normalize(vmin=-0.5, vmax=1.5)  # More aggressive normalization

# Determine the color for each bar based on the proximity to y_interest
colors = []
for mean, std in zip(mean_values, std_dev):
    lower_bound = mean - 1.96 * std
    upper_bound = mean + 1.96 * std
    
    if upper_bound < y_interest:
        color_value = 0  # Fully blue
    elif lower_bound > y_interest:
        color_value = 1  # Fully red
    else:
        # If the y_interest is within the confidence interval, calculate the proportion
        proportion = (y_interest - lower_bound) / (upper_bound - lower_bound)
        color_value = proportion  # Proportion for the colormap

    colors.append(cmap(norm(color_value)))

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))  # Create figure and axis explicitly
bars = ax.bar(df.index, mean_values, yerr=1.96 * std_dev, color=colors, edgecolor='black')

# Add horizontal line for the y-interest value
ax.axhline(y=y_interest, color='black', linestyle='--', label=f'Y-Value of Interest ({y_interest})')

# Add color bar for the gradient
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Explicitly specify the axis for the colorbar
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', label='Color Scale', pad=0.2, aspect=50)

# Set labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Mean Value')
ax.set_title('Bar Chart with More Pronounced Gradient Colors Based on Y-Axis Value')
ax.legend()

# Show the plot
plt.show()
