import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

def makeplot(data, gtype):
    filepath = f'HotfireData/{data}'
    df = pd.read_csv(filepath)
    x = 'Time'
    y = 'Value'
    if data == 'combined_cf.csv' or data == 'fuel_coldflow.csv':
        y = 'Pressure'

    # Get unique sensors
    sensors = df['Sensor'].unique()
    
    # Create a figure with subplots for each sensor
    fig, axes = plt.subplots(len(sensors), 1, figsize=(10, 4 * len(sensors)))
    
    # Handle single sensor case
    if len(sensors) == 1:
        axes = [axes]
    
    # Plot each sensor separately
    for idx, sensor in enumerate(sensors):
        sensor_data = df[df['Sensor'] == sensor]
        
        match gtype:
            case 'scatter':
                sns.scatterplot(x=x, y=y, data=sensor_data, ax=axes[idx])
            case 'line':
                sns.lineplot(x=x, y=y, data=sensor_data, ax=axes[idx])
            case 'bar':
                sns.barplot(x=x, y=y, data=sensor_data, ax=axes[idx])
            case 'hist':
                sns.histplot(x=x, y=y, data=sensor_data, ax=axes[idx])
            case _:
                print("Invalid gtype")
        
        axes[idx].set_title(f'{sensor}')
    
    plt.tight_layout()
    plt.draw()
    plt.show()

if __name__ == '__main__':
    while True:
        csv = input("Enter csv file\n")

        if csv == 'quit':
            break

        gtype = input("Enter gtype, scatter, line, bar, hist\n")
        makeplot(csv, gtype)
