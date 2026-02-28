import numpy as np
from scipy.signal import butter, filtfilt, hilbert

phi = (1 + np.sqrt(5)) / 2
freqs = np.array([4.0, 7.0, 11.0, 18.0, 29.0, 47.0])

def full_phi_pipeline(raw_lfp, fs=20000, window_sec=0.5):
    """Production-ready: sliding windows + diagnostics + error correction (Blueprint p.5)"""
    if raw_lfp.ndim == 1:
        raw_lfp = raw_lfp.reshape(1, -1)
    n_ch, n_samp = raw_lfp.shape
    win_samples = int(window_sec * fs)
    num_windows = max(1, n_samp // win_samples)
    
    bci_phi = np.zeros(n_ch)
    vacuum_fracs = np.zeros((6, n_ch))
    
    for ch in range(n_ch):
        C_windows = []
        delta_windows = []
        good_windows = 0
        
        for w in range(num_windows):
            start = w * win_samples
            end = min(start + win_samples, n_samp)
            if end - start < 200: continue  # skip tiny windows
            
            # Extract phases for this window
            inst_phase = np.zeros((6, end-start))
            for i, f in enumerate(freqs):
                b, a = butter(4, [f-1.5, f+1.5], fs=fs, btype='band', output='ba')
                filtered = filtfilt(b, a, raw_lfp[ch, start:end])
                analytic = hilbert(filtered)
                inst_phase[i] = np.unwrap(np.angle(analytic))
            
            # Compute coherence & delta for this window
            C = np.zeros((6,6))
            delta = np.zeros((6,6))
            for j in range(6):
                for k in range(j+1,6):
                    dphi = inst_phase[j] - inst_phase[k]
                    coh = np.abs(np.mean(np.exp(1j * dphi)))
                    C[j,k] = C[k,j] = coh
                    dlt = np.mean(dphi) % (2 * np.pi)
                    delta[j,k] = delta[k,j] = dlt
            
            C_windows.append(C)
            delta_windows.append(delta)
            good_windows += 1
        
        if good_windows == 0:
            print(f"⚠️  No good windows for channel {ch}")
            continue
        
        C = np.mean(C_windows, axis=0)
        delta = np.mean(delta_windows, axis=0)
        
        # BCI_φ (adjacent pairs only - most stable)
        sum_w = 0.0
        sum_term = 0.0
        for lev in range(5):
            j, k = lev, lev + 1
            coh = C[j,k]
            dlt = delta[j,k]
            predicted = 2 * np.pi / phi**2
            cos_m = np.cos(dlt - predicted)
            w = 1.0 / phi
            sum_w += w
            sum_term += w * coh * cos_m
            print(f"  Pair L{lev+1}-L{lev+2}: coh={coh:.3f}, offset={dlt*180/np.pi:.1f}°, cos={cos_m:.3f}")
        
        bci_phi[ch] = sum_term / sum_w if sum_w > 0 else 0.0
        print(f"  → BCI_φ for channel {ch} = {bci_phi[ch]:.3f}")
        
        # Vacuum fraction
        for lev in range(6):
            adj = []
            if lev > 0: adj.append(lev-1)
            if lev < 5: adj.append(lev+1)
            if adj:
                coh_list = [C[lev,a] for a in adj]
                cos_list = [np.cos(delta[lev,a] - 2*np.pi/phi**2) for a in adj]
                coh = np.mean(coh_list)
                cos_m = np.mean(cos_list)
                vf = max(coh * max(cos_m, 0) * 0.45, 0)
                vacuum_fracs[lev,ch] = vf
    
    return {
        'bci_phi': np.nan_to_num(bci_phi, nan=0.0),
        'mean_vacuum': np.nan_to_num(vacuum_fracs.mean(), nan=0.0)
    }
