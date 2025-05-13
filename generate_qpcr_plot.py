import matplotlib
matplotlib.use('Agg') # Use a non-interactive backend, suitable for scripts
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_qpcr_curve(output_directory="static"):
    """Generates and saves a conceptual qPCR amplification curve."""
    cycles = np.arange(1, 41) # 40 PCR cycles
    
    samples_params = [
        {'label': 'Sample 1 (High Conc.)', 'L': 1.0, 'k': 0.5, 'x0': 15, 'color': 'blue'},
        {'label': 'Sample 2 (Med Conc.)', 'L': 1.0, 'k': 0.5, 'x0': 22, 'color': 'green'},
        {'label': 'Sample 3 (Low Conc.)', 'L': 1.0, 'k': 0.5, 'x0': 28, 'color': 'red'},
        {'label': 'NTC (No Template Control)', 'L': 0.05, 'k':0.3, 'x0': 35, 'color': 'grey'}
    ]

    plt.figure(figsize=(10, 6))

    for params in samples_params:
        fluorescence = params['L'] / (1 + np.exp(-params['k'] * (cycles - params['x0'])))
        noise = np.random.normal(0, 0.015, len(cycles)) * (params['L'] if params['L'] > 0.1 else 0.1)
        fluorescence = np.clip(fluorescence + noise, 0, params['L'] * 1.1 if params['L'] > 0 else 0.1)
        plt.plot(cycles, fluorescence, label=params['label'], color=params['color'])

    plt.title('Conceptual qPCR Amplification Plot')
    plt.xlabel('Cycle Number')
    plt.ylabel('Fluorescence Intensity (Arbitrary Units)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    
    threshold = 0.25
    plt.axhline(y=threshold, color='purple', linestyle=':', label=f'Threshold ({threshold})')
    
    handles, labels = plt.gca().get_legend_handles_labels()
    from matplotlib.lines import Line2D
    if f'Threshold ({threshold})' not in labels: # Ensure threshold is added if not picked up
        handles.append(Line2D([0], [0], color='purple', linestyle=':'))
        labels.append(f'Threshold ({threshold})')
    plt.legend(handles, labels)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    output_path = os.path.join(output_directory, 'q_pcr_curve.png')
    plt.savefig(output_path)
    print(f"qPCR plot saved as {output_path}")

if __name__ == '__main__':
    generate_qpcr_curve()