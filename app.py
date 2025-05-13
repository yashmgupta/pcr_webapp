from flask import Flask, render_template, jsonify, send_from_directory
import os
import json

# Import the functions from your scripts
from generate_qpcr_plot import generate_qpcr_curve
from simulate_pcr import simulate_pcr_amplification, save_simulation_data

app = Flask(__name__)

# Define the static folder path correctly
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.config['STATIC_FOLDER'] = STATIC_FOLDER


def ensure_data_generated():
    """Checks if data/plot exist, generates them if not."""
    plot_path = os.path.join(STATIC_FOLDER, 'q_pcr_curve.png')
    data_path = os.path.join(STATIC_FOLDER, 'pcr_simulation_data.json')

    if not os.path.exists(STATIC_FOLDER):
        os.makedirs(STATIC_FOLDER)

    if not os.path.exists(plot_path):
        print(f"Plot not found at {plot_path}. Generating...")
        generate_qpcr_curve(output_directory=STATIC_FOLDER)
    
    if not os.path.exists(data_path):
        print(f"Simulation data not found at {data_path}. Generating...")
        simulation_results = simulate_pcr_amplification(initial_molecules=50, cycles=25, efficiency=0.95)
        save_simulation_data(simulation_results, output_directory=STATIC_FOLDER)

@app.before_request
def before_first_request_func():
    # Ensures data is generated once before the first request if needed,
    if not hasattr(app, 'data_ensured'):
        ensure_data_generated()
        app.data_ensured = True


@app.route('/')
def home():
    return render_template('pcr_app.html')

@app.route('/get_simulation_data')
def get_simulation_data_endpoint():
    data_path = os.path.join(STATIC_FOLDER, 'pcr_simulation_data.json')
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Simulation data file not found. Please try restarting the app or check logs."}), 404
    except Exception as e:
        return jsonify({"error": f"Error reading simulation data: {str(e)}"}), 500

# Flask automatically serves files from the 'static' folder if referenced with url_for.
# This explicit route is usually not needed if STATIC_FOLDER is configured and url_for is used.
# @app.route('/static/<path:filename>')
# def serve_static(filename):
#    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)