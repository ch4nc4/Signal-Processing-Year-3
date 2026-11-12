import numpy as np
import matplotlib.pyplot as plt
import time
import math
import soundfile as sf

def FFT(x):
    # input for FFT should have length of power of 2
    N = len(x)

    if N==1:
        return x.copy()

    X_even = FFT(x[::2])
    X_odd = FFT(x[1::2])
    factor = np.exp(-2j*np.pi*np.arange(N)/ N)
    
    X = np.concatenate([X_even+factor[:int(N/2)]*X_odd, X_even+factor[int(N/2):]*X_odd])
    return X

def DFT(x):
    N = len(x)
    vec = np.arange(0, N) 
    i_dot_j = np.outer(vec, vec)

    fourier_matrix = math.e**(-2 * np.pi * 1j * i_dot_j / N)

#ex1
def Lab04_ex1():
    N = [128, 256, 512, 1024, 2048, 4096, 8192]
    f = 200 # frecventa semnalului

    my_FFT = []
    my_DFT = []
    py_FFT = []
    for len in N:
        t = np.arange(len) / len
        x_n = np.sin(2 * np.pi * f * t + np.pi/2)

        t0 = time.time_ns()
        my_fft = FFT(x_n)
        t1 = time.time_ns()

        my_dft = DFT(x_n)
        t2 = time.time_ns()

        py_fft = np.fft.fft(x_n)
        t3 = time.time_ns()

        my_FFT.append(t1 - t0)
        my_DFT.append(t2 - t1)
        py_FFT.append(t3 - t2)

    bins = np.arange(7)
    fig, axs = plt.subplots(2, 2)
    axs[0][0].plot(N, my_FFT, color='red')
    axs[0][0].set_title("My FFT")
    axs[0][0].set_yscale("log")
    axs[1][0].plot(N, py_FFT, color='green')
    axs[1][0].set_title("PY FFT")
    axs[1][0].set_yscale("log")

    axs[0][1].plot(N, my_DFT, color='blue')
    axs[0][1].set_title("My DFT")
    axs[0][1].set_yscale("log")
    axs[1][1].plot(N, py_FFT, color='green')
    axs[1][1].set_title("PY FFT")
    axs[1][1].set_yscale("log")

    fig.tight_layout()
    plt.show()
    # plt.savefig("lab04_ex1_log.pdf", format="pdf")
    # plt.close()

# ex2
# pentru a observa fenomenul de aliere:
# fs = 200 # frecventa sampling
# f = 150 # frecventa semnalului
# f2 = f + fs
# f3 = f + 2fs
def Lab04_ex2(f, f2, f3, fs):
    N = 20 # nr de esantioane
    t = np.arange(N) / fs
    t_dense = np.linspace(t[0], t[-1], 5000) 

    x = np.sin(2 * np.pi * f * t)
    x_dense = np.sin(2 * np.pi * f * t_dense)
    y = np.sin(2 * np.pi * f2 * t)
    y_dense = np.sin(2 * np.pi * f2 * t_dense)
    z = np.sin(2 * np.pi * f3 * t)
    z_dense = np.sin(2 * np.pi * f3 * t_dense)

    fig, axs = plt.subplots(3)
    axs[0].plot(t, x, '.-', color='red')
    axs[0].plot(t_dense, x_dense, color='blue')
    axs[1].plot(t, y, '.-',color='red')
    axs[1].plot(t_dense, y_dense, color='blue')
    axs[2].plot(t, z, '.-',color='red')
    axs[2].plot(t_dense, z_dense, color='blue')

    plt.show()
    # plt.savefig("lab04_ex2.pdf", format="pdf")
    # plt.close()

#ex3
# pentru a nu mai observa fenomenul de aliere:
# fs_old = 200
# fs = 1300 # frecventa sampling
# f = 150 # frecventa semnalului
# f2 = f + fs_old
# f3 = f + 2fs_old
def Lab04_ex3():
    Lab04_ex2(150, 150 + 200, 150 + 400, 1600)

#ex4
# Frecventa minima cu care trebuie esantionat semnalul trece-banda este 401 - cea mai mare frecventa care trebuie capturata este 200Hz
# asa ca pentru a prinde componentele de frecventa maxima este necesar ca f < fs/2, iar 200 < 401/2

#ex5
# Putem observa ca pentru 'o' si 'u' se activeaza mai ales frecventele joase 
# Se observa cu ochiul liber unde incep si termin de spus o vocala, dar nu pot neaparat sa disting intre ele
# Mai ales ca stiu deja ordinea in care le-am spus <_>

#ex6
def Lab04_ex6():
    signal, sample_rate = sf.read("Lab4_PS_Vocale.aiff")

    N = len(signal)
    window_size = max(1, int(0.01 * N))
    hop_size = max(1, window_size // 2)

    groups = np.array([
        signal[start:start + window_size]
        for start in range(0, N - window_size + 1, hop_size)
    ])

    # Smallest power of 2 greater than or equal to window_size
    fft_size = 1 << (window_size - 1).bit_length()

    # Hann window used to reduce spectral leakage
    # The Hanning window multiplies your signal by a smooth, raised-cosine bell curve 
    # that tapers the amplitude down to zero at both ends
    window = np.hanning(window_size)

    FFT_matrix = []

    for group in groups:
        # apply Hann window
        windowed_group = group * window

        # zero-pad so that the length is a power of 2
        padded_group = np.pad(
            windowed_group,
            (0, fft_size - window_size),
            mode="constant"
        )

        spectrum = FFT(padded_group)

        # only half the positive-frequency 
        positive_spectrum = np.abs(spectrum[:fft_size // 2 + 1])

        FFT_matrix.append(positive_spectrum)

    FFT_matrix = np.array(FFT_matrix)

    # we need to convert magnitude to decibels (x axis is time, y axis is dB)
    FFT_dB = 20 * np.log10(FFT_matrix + 1e-12)

    times = np.arange(len(groups)) * hop_size / sample_rate
    frequencies = (
        np.arange(fft_size // 2 + 1) * sample_rate / fft_size
    )

    plt.figure()

    plt.pcolormesh(
        times,
        frequencies,
        FFT_dB.T,
        shading="auto",
        cmap="magma"
    )

    plt.title("Spectrogram using my FFT")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.colorbar(label="Magnitude [dB]")
    plt.ylim(0, sample_rate / 2)
    plt.tight_layout()
    plt.show()

    # plt.savefig("lab04_ex6.pdf", format="pdf")
    # plt.close()

    return FFT_matrix

mySpectogram = Lab04_ex6()

#ex7

# Puterea unui semnal este Psemnal = 90dB. Se cunoaste raportul semnal-zgomot, SNRdB = 80dB. Care este puterea zgomotului?
# SNRdB = 10(log10SNR) => 80 = 10 * (log10SNR) => SNR = 10^8
# SNR = Psemnal/Pzgomot => Pzgomot = Psemnal/SNR => Pzgomot = 90/10^8