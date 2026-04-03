# Precision Signal Denoising via Continuous Wavelet Transform (CWT)
Cleaning sound signals with high frequency spikes. 

A specialized Python utility for cleaning "spiky" non-stationary noise from audio or sensor data. 
Unlike standard Fourier Transforms, this Wavelet-based approach preserves time-localization, 
making it ideal for transient-heavy signals like music or mechanical data.

## 🚀 Key Features
* **Multi-resolution Analysis:** Decomposes signals into approximation and detail coefficients.
* **Soft Thresholding:** Intelligently filters high-frequency noise while preserving signal integrity.
* **Basis Flexibility:** Supports Daubechies (db4), Haar, and Symlets via `PyWavelets`.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Core Libraries:** NumPy, PyWavelets (pywt), Matplotlib

## 📈 Performance
By utilizing a **Morlet wavelet basis**, this implementation effectively targets "spiky" artifacts that traditional low-pass filters often smear across the time domain.

## 🧪 Results (Demonstration)
To demonstrate the filter's efficacy on high-pitch interference:
* **Original:** [(https://github.com/Gio-Reg/highpitch-signal-denoising-wavelet/edit/main/README.md#:~:text=squeek_audio.wav-,squeek_original,-.mp4)] - Notice the high-frequency "hiss" or "spike."
* **Processed:** [https://github.com/Gio-Reg/highpitch-signal-denoising-wavelet/edit/main/README.md#:~:text=cleaned_squeek_audio.wav-,final_video,-.mp4] - Cleaned via DWT Reconstruction.

The transformation successfully isolated the signal of interest without the "ghosting" effects common in standard FFT-based notch filters.
