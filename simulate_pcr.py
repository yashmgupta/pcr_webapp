import json
import os

def simulate_pcr_amplification(initial_molecules=100, cycles=30, efficiency=1.0):
    """
    Simulates basic PCR amplification.
    """
    amplification_data = []
    current_molecules = float(initial_molecules)
    
    for cycle in range(cycles + 1):
        amplification_data.append({"cycle": cycle, "molecules": round(current_molecules)})
        if cycle < cycles:
            current_molecules += current_molecules * efficiency
            
    return amplification_data

def save_simulation_data(data, output_directory="static", filename="pcr_simulation_data.json"):
    """Saves the simulation data to a JSON file."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    output_path = os.path.join(output_directory, filename)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"PCR simulation data saved to {output_path}")


if __name__ == '__main__':
    simulation_results = simulate_pcr_amplification(initial_molecules=50, cycles=25, efficiency=0.95)
    save_simulation_data(simulation_results)