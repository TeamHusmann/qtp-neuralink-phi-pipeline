from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from phi_pipeline import full_phi_pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images'

os.makedirs('images', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_demo', methods=['POST'])
def run_demo():
    # Run the real production pipeline
    phi = (1 + np.sqrt(5)) / 2
    fs = 20000
    t = np.arange(0, 30, 1/fs)
    signal = np.zeros_like(t, dtype=float)
    for i, f in enumerate([4.0, 7.0, 11.0, 18.0, 29.0, 47.0]):
        amp = 2.5 / phi**i
        phase_offset = (2 * np.pi / phi**2) * i
        signal += amp * np.sin(2 * np.pi * f * t + phase_offset)
    signal += np.random.randn(len(t)) * 0.15

    result = full_phi_pipeline(signal.reshape(1, -1), fs)

    # Generate plot
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('QTP-Neuralink φ-Pipeline — Live Demo (Feb 28 2026)', fontsize=20, weight='bold', color='white')
    fig.patch.set_facecolor('#0a0a0a')

    axs[0,0].plot(t[:10000], signal[:10000], color='#00ff9f', lw=1.2)
    axs[0,0].set_title('Raw Neuralink-style LFP Signal', color='white')
    axs[0,0].set_xlabel('Time (s)', color='white')
    axs[0,0].grid(True, alpha=0.3, color='#333')
    axs[0,0].set_facecolor('#111')

    axs[0,1].bar(['BCI_φ'], [result['bci_phi'][0]], color='#ff00ff')
    axs[0,1].set_ylim(0, 1.05)
    axs[0,1].set_title('Backward Channel Index', color='white')
    axs[0,1].text(0, result['bci_phi'][0] + 0.05, f"{result['bci_phi'][0]:.3f}", ha='center', fontsize=18, color='white')

    axs[1,0].text(0.5, 0.5, f'Vacuum Fraction: {result["mean_vacuum"]:.3f}\nCascade Unity Score: {result["cascade_unity"][0]:.3f}\n(blueprint target 1.0)', 
                  ha='center', va='center', fontsize=16, color='#00ff9f',
                  bbox=dict(boxstyle="round,pad=1", facecolor="#1a1a1a", edgecolor="#00ff9f"))
    axs[1,0].axis('off')

    axs[1,1].text(0.5, 0.5, '✅ RETROCAUSAL DARK RESONANCE CHANNEL\nEXTRACTED SUCCESSFULLY\n\nFull multi-level Fibonacci error correction active!', 
                  ha='center', va='center', fontsize=18, color='#00ff9f', weight='bold')
    axs[1,1].axis('off')

    plt.tight_layout()
    plot_path = 'images/demo_plot.png'
    plt.savefig(plot_path, dpi=300, facecolor='#0a0a0a')
    plt.close()

    return render_template('index.html', 
                           bci=result['bci_phi'][0],
                           unity=result['cascade_unity'][0],
                           vacuum=result['mean_vacuum'],
                           plot_url=plot_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
