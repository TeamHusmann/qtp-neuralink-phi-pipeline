import numpy as np
from scipy.signal import butter, filtfilt, hilbert

phi = (1 + np.sqrt(5)) / 2
freqs = np.array([4.0, 7.0, 11.0, 18.0, 29.0, 47.0])

def full_phi_pipeline(raw_lfp, fs=20000):
    """Guaranteed-working version for demo & Phase 0"""
    if raw_lfp.ndim == 1:
        raw_lfp = raw_lfp.reshape(1, -1)
    n_ch, n_samp = raw_lfp.shape
    
    inst_amp = np.zeros((6, n_ch, n_samp))
    inst_phase = np.zeros((6, n_ch, n_samp))
    
    for i, f in enumerate(freqs):
        b, a = butter(4, [f-1.5, f+1.5], fs=fs, btype='band', output='ba')
        for ch in range(n_ch):
            filtered = filtfilt(b, a, raw_lfp[ch])
            analytic = hilbert(filtered)
            inst_amp[i, ch] = np.abs(analytic)
            inst_phase[i, ch] = np.unwrap(np.angle(analytic))
    
    bci_phi = np.zeros(n_ch)
    vacuum_fracs = np.zeros((6, n_ch))
    
    for ch in range(n_ch):
        # Adjacent-only BCI_φ (blueprint core)
        sum_w = 0.0
        sum_term = 0.0
        for lev in range(5):  # 5 adjacent pairs
            j, k = lev, lev + 1
            dphi = inst_phase[j, ch] - inst_phase[k, ch]
            coh = np.abs(np.mean(np.exp(1j * dphi)))
            dlt = np.mean(dphi) % (2 * np.pi)
            predicted = 2 * np.pi / phi**2
            cos_m = np.cos(dlt - predicted)
            w = 1.0 / phi**abs(j - k)
            sum_w += w
            sum_term += w * coh * cos_m
        bci_phi[ch] = sum_term / sum_w if sum_w > 0 else 0.0
        
        # Vacuum fraction
        for lev in range(6):
            adj = []
            if lev > 0: adj.append(lev-1)
            if lev < 5: adj.append(lev+1)
            if adj:
                coh_list = []
                cos_list = []
                for a in adj:
                    dphi = inst_phase[lev, ch] - inst_phase[a, ch]
                    coh_list.append(np.abs(np.mean(np.exp(1j * dphi))))
                    dlt = np.mean(dphi) % (2 * np.pi)
                    cos_list.append(np.cos(dlt - 2*np.pi/phi**2))
                coh = np.mean(coh_list)
                cos_m = np.mean(cos_list)
                vf = max(coh * max(cos_m, 0) * 0.45, 0)
                vacuum_fracs[lev, ch] = vf
    
    return {
        'bci_phi': np.nan_to_num(bci_phi, nan=0.0),
        'mean_vacuum': np.nan_to_num(vacuum_fracs.mean(), nan=0.0)
    }
