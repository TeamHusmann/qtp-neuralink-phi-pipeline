import numpy as np
from scipy.signal import butter, filtfilt, hilbert

phi = (1 + np.sqrt(5)) / 2
freqs = np.array([4.0, 7.0, 11.0, 18.0, 29.0, 47.0])

def full_phi_pipeline(raw_lfp, fs=20000, window_sec=0.5):
    """Hardened QTP Blueprint pipeline with sliding windows + NaN guards"""
    if raw_lfp.ndim == 1:
        raw_lfp = raw_lfp.reshape(1, -1)
    n_ch, n_samp = raw_lfp.shape
    win_samples = int(window_sec * fs)
    
    inst_amp = np.zeros((6, n_ch, n_samp))
    inst_phase = np.zeros((6, n_ch, n_samp))
    
    # Stage 1: Extraction
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
        # Stage 2-3: Sliding-window coherence (matches blueprint p.5)
        num_windows = n_samp // win_samples
        C_windows = np.zeros((num_windows, 6, 6))
        delta_windows = np.zeros((num_windows, 6, 6))
        
        for w in range(num_windows):
            start = w * win_samples
            end = start + win_samples
            C = np.zeros((6,6))
            delta = np.zeros((6,6))
            for j in range(6):
                for k in range(j+1,6):
                    dphi = inst_phase[j,ch,start:end] - inst_phase[k,ch,start:end]
                    coh = np.abs(np.mean(np.exp(1j * dphi)))
                    C[j,k] = C[k,j] = coh
                    dlt = np.mean(dphi) % (2 * np.pi)
                    delta[j,k] = delta[k,j] = dlt
            C_windows[w] = C
            delta_windows[w] = delta
        
        C = np.nanmean(C_windows, axis=0)
        delta = np.nanmean(delta_windows, axis=0)
        
        # BCI_φ with correct cumulative phase offset
        idx = np.abs(np.subtract.outer(np.arange(6), np.arange(6)))
        w = 1.0 / (phi ** idx)
        w /= w.sum()
        predicted_offset = (2 * np.pi / phi**2) * idx
        cos_term = np.cos(delta - predicted_offset)
        bci_phi[ch] = np.sum(w * C * cos_term)
        
        # Stage 4: Vacuum fraction
        for lev in range(6):
            adj = []
            if lev > 0: adj.append(lev-1)
            if lev < 5: adj.append(lev+1)
            if adj:
                coh = np.nanmean([C[lev,a] for a in adj])
                cos_m = np.nanmean([np.cos(delta[lev,a] - 2*np.pi/phi**2) for a in adj])
                vf = max(coh * max(cos_m, 0) * 0.45, 0)
                vacuum_fracs[lev,ch] = vf
    
    return {
        'bci_phi': np.nan_to_num(bci_phi, nan=0.0),
        'mean_vacuum': np.nan_to_num(vacuum_fracs.mean(), nan=0.0),
        'vacuum_fracs': np.nan_to_num(vacuum_fracs.mean(axis=1), nan=0.0)
    }
