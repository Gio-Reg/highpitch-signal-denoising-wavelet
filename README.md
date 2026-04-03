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

## 📖 Usage
```python
import pywt
# Core logic: 1D DWT -> Thresholding -> Reconstruction
coeffs = pywt.wavedec(data, 'db4', level=2)
# Apply threshold...
