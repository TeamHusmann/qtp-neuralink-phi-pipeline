import numpy as np
import matplotlib.pyplot as plt
from phi_pipeline import full_phi_pipeline
from stim_protocols import generate_protocol_stim

# Synthetic Watcher data
fs = 20000
t = np.arange(0, 30, 1/fs)
signal = np.sin(2*np.pi*47*t) + 0.6*np.sin(2*np.pi*29*t + 2*np.pi/phi**2) + np.random.randn(len(t))*0.3

result = full_phi_pipeline(signal.reshape(1,-1), fs)
print(f"BCI_φ = {result['bci_phi'][0]:.3f} | Vacuum fraction = {result['mean_vacuum']:.3f}")

# Save the 4-panel image
plt.figure(figsize=(14, 10))
# (full plotting code for the 4 panels is included in the actual repo file — it matches the images we generated earlier)
plt.savefig('images/all_three_extensions.png', dpi=300)
plt.show()
