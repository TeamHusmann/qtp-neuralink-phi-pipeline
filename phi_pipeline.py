import numpy as np
from scipy.signal import butter, filtfilt, hilbert

phi = (1 + np.sqrt(5)) / 2
freqs = np.array([4.0, 7.0, 11.0, 18.0, 29.0, 47.0])

def full_phi_pipeline(raw_lfp, fs=20000):
    """Simplified & robust version — full-signal window (perfect for demo & Phase 0)"""
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
        C = np.zeros((6,6))
        delta = np.zeros((6,6))
        for j in range(6):
            for k in range(j+1,6):
                dphi = inst_phase[j,ch] - inst_phase[k,ch]
                coh = np.abs(np.mean(np.exp(1j * dphi)))
                C[j,k] = C[k,j] = coh
                dlt = np.mean(dphi) % (2 * np.pi)
                delta[j,k] = delta[k,j] = dlt
        
        idx = np.abs(np.subtract.outer(np.arange(6), np.arange(6)))
        w = 1.0 / (phi ** idx)
        w /= w.sum()
        predicted_offset = (2 * np.pi / phi**2) * idx
        cos_term = np.cos(delta - predicted_offset)
        bci_phi[ch] = np.sum(w * C * cos_term)
        
        for lev in range(6):
            adj = []
            if lev > 0: adj.append(lev-1)
            if lev < 5: adj.append(lev+1)
            if adj:
                coh = np.mean([C[lev,a] for a in adj])
                cos_m = np.mean([np.cos(delta[lev,a] - 2*np.pi/phi**2) for a in adj])
                vf = max(coh * max(cos_m, 0) * 0.45, 0)
                vacuum_fracs[lev,ch] = vf
    
    return {
        'bci_phi': np.nan_to_num(bci_phi, nan=0.0),
        'mean_vacuum': np.nan_to_num(vacuum_fracs.mean(), nan=0.0)
    }
