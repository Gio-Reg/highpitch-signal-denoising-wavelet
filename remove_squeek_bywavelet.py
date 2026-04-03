import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pywt 

plt.ion()

# Load the wav file
#sample_rate, data = wavfile.read('original_9s_window.wav')
sample_rate, data = wavfile.read('squeek_audio.wav')


# If the audio is 16-bit, normalize it to a range of -1.0 to 1.0
if data.dtype == np.int16:
    data = data / 32768.0

# Create a time axis
time = np.linspace(0, len(data) / sample_rate, num=len(data))

sig=data

sig_window=sig
time_window=time

#widths = np.arange(1, 16)

octaves = 5
nodes = 12
widths = 2**np.arange(0, octaves, 1/nodes)
#widths = np.arange(1, 16)
widths = np.array([2 ** x for x in range(11)])

print("scales are:", widths)


#cwtmatr, freqs = pywt.cwt(sig_window, widths, 'mexh')
cwtmatr, freqs = pywt.cwt(sig_window, widths, 'morl')
print("frequencies are:", freqs)


# 2. Show the dimensions (Rows, Columns)
# Rows = Number of scales (widths), Columns = Length of your signal
print(f"Matrix Shape: {cwtmatr.shape}")

freqs_mask = (freqs >= 0.01) & (freqs <= 0.3)
# 2. Slice the frequency array and the matrix
# We slice the rows (axis 0) of the matrix
freqs_high = freqs[freqs_mask]
cwtmatr_high = cwtmatr[freqs_mask, :]

freqs_high=freqs
cwtmatr_high=cwtmatr


# 1. Get the absolute values
abs_cwt = np.abs(cwtmatr_high)

# 2. Standardize row-by-row (along the time axis)
# We add a tiny epsilon (1e-8) to avoid division by zero
row_means = np.mean(abs_cwt, axis=1, keepdims=True)
row_stds = np.std(abs_cwt, axis=1, keepdims=True) + 1e-8

standardized_cwt = (abs_cwt - row_means) / row_stds


########
high_freq_coeffs = standardized_cwt[1, :]
high_freq_hz = freqs_high[1]

mid_freq_coeffs = standardized_cwt[5, :]
mid_freq_hz = freqs_high[5]

low_freq_coeffs = standardized_cwt[9, :]
low_freq_hz = freqs_high[9]

answ=input("Do you want to see the plots? : ")
if answ == 1: 

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
    plt.subplots_adjust(hspace=0.4) # Increased space for titles

    # --- Top Plot: The Raw Audio Signal ---
    ax1.plot(time_window, sig_window, color='royalblue', alpha=0.8, lw=1)
    #ax1.set_title(f"Original Signal Window ({start_sec}s - {end_sec}s)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)

    # --- High Freq Plot ---
    ax2.plot(time_window, high_freq_coeffs, color='orangered', lw=1.5)
    ax2.axhline(y=3, color='black', linestyle='--', alpha=0.5, label="3-Sigma")
    #ax2.set_title(f"High Freq Coefficients: {high_freq_hz:.4f} (Normalized)")
    ax2.set_ylabel("Z-Score")
    ax2.legend(loc='upper right')
    ax2.set_ylim(-1, 10)
    ax2.grid(True, alpha=0.3)

    # --- Mid Freq Plot ---
    ax3.plot(time_window, mid_freq_coeffs, color='forestgreen', lw=1.5)
    ax3.axhline(y=3, color='black', linestyle='--', alpha=0.5, label="3-Sigma")
    #ax3.set_title(f"Mid Freq Coefficients: {mid_freq_hz:.4f} (Normalized)")
    ax3.set_ylabel("Z-Score")
    ax3.legend(loc='upper right')
    ax3.set_ylim(-1, 10)
    ax3.grid(True, alpha=0.3)

    # --- Low Freq Plot ---
    ax4.plot(time_window, low_freq_coeffs, color='purple', lw=1.5)
    ax4.axhline(y=3, color='black', linestyle='--', alpha=0.5, label="3-Sigma")
    #ax4.set_title(f"Low Freq Coefficients: {low_freq_hz:.4f} (Normalized)")
    ax4.set_ylabel("Z-Score")
    ax4.set_xlabel("Time (s)")
    ax4.legend(loc='upper right')
    ax4.set_ylim(-1, 10)
    ax4.grid(True, alpha=0.3)

    # Use block=True so the window stays open until you close it
    plt.show(block=True)

########

########
# --- NEW RECONSTRUCTION PART ---
########

print("Processing surgical reconstruction...")

# #-------------origianl handling of the coefficients valid ------
# # 1. Create a copy of the original complex coefficients
# cleaned_cwt = cwtmatr.copy()

# # 2. Create the mask for Z-scores > 3
# mask = standardized_cwt > 3

# # 3. Restrict the mask: Only keep 'True' for the first 7 rows (indices 0-6)
# # We set the mask to False for all rows from index 7 onwards
# mask[4:, :] = False

# # 4. Apply the restricted mask to the coefficients
# cleaned_cwt[mask] = 0.0
# #--------------------------------------------------------

#---- New method (Fixed Broadcasting) ----
cleaned_cwt = cwtmatr.copy()

# 1. Identify the spikes
mask = standardized_cwt > 2.3
mask[4:, :] = False  # Only affect high-freq rows

# 2. Calculate target values (1-Sigma)
target_values = (0. * row_stds) + row_means 

# 3. CRITICAL FIX: Broadcast target_values to match the matrix shape
# This stretches the (11, 1) vector into an (11, 396900) matrix
target_values_full = np.broadcast_to(target_values, cleaned_cwt.shape)

# 4. Apply the cap while preserving Phase
# We use a small epsilon to avoid division by zero
phases = cwtmatr / (np.abs(cwtmatr) + 1e-10)

# Now the shapes match perfectly for boolean indexing
cleaned_cwt[mask] = phases[mask] * target_values_full[mask]

print("Squeaks capped at 0-Sigma. Shapes aligned. Reconstruction ready.")

# 3. Inverse Transform via Scale-Summation
# Formula for Morlet: Signal ~ Sum [ Real(Coefficients) / sqrt(scales) ]
scales = widths[:, np.newaxis]
reconstruction_raw = np.sum(np.real(cleaned_cwt) / (scales**0.5), axis=0)

perfect_recon = reconstruction_raw

# 5. Save the Surgically Cleaned Reconstruction
clean_recon_int = (perfect_recon * 32767).clip(-32768, 32767).astype(np.int16)
#wavfile.write('surgical_clean_recon.wav', sample_rate, clean_recon_int)
wavfile.write('cleaned_squeek_audio.wav', sample_rate, clean_recon_int)

print("Done! Surgical reconstruction saved as 'surgical_clean_recon.wav'")


