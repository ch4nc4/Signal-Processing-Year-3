import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv

def Lab05():
    # (a)
    # exista 18288 de esantioane, din ora in ora cate unul 
    # fs = 1/T unde T este distanta in secunde intre 2 esantioane
    # hence, fs = 1/T = 1/3600 (o ora are 3600 secunde cred lol)

    # (b)
    # intervalul de timp acoperit este 25-08-2012 00:00 - 25-09-2014 23:00

    # (c)
    x = np.genfromtxt('Train.csv', delimiter=',', usecols=[2])
    x = x[np.isfinite(x)]

    T = 3600
    fs = 1/T
    N = x.size

    X = np.fft.fft(x-np.mean(x))
    X_w_mean = np.fft.fft(x)

    X_positive = X[:N // 2]
    X_positive_w_mean = X_w_mean[:N // 2]

    f = fs * np.arange(N // 2) / N
    amplitude_mean_rm = np.abs(X_positive) / N
    amplitude_w_mean = np.abs(X_positive_w_mean) / N
    peak_idx = np.argmax(amplitude_mean_rm[1:])+1

    dominant_freq = f[peak_idx]
    print(f'Dominant frequency: {dominant_freq}')

    # (d)
    # plt.plot(f, amplitude_w_mean, color='red')
    # plt.yscale('log')

    #(e)
    # este clar ca semnalul are o componenta continua, observam ca atunci cand nu scadem media avem amplitudine maxima la frecv zero
    # in schimb daca scadem media, aceasta amplitudine maxima este > 0
    # plt.stem(f, amplitude_mean_rm, label="Mean removed")
    # plt.scatter(f, amplitude_w_mean, label="Original", color='blue')
    # plt.legend()

    # amplitude_mean_rm[0] = 0;
    # plt.plot(f, amplitude_mean_rm)
    # plt.yscale('log')
    # plt.savefig("lab05_amplitude_log.pdf")

    #(f)
    peaks = np.where(
        (amplitude_mean_rm[1:-1] > amplitude_mean_rm[:-2]) &
        (amplitude_mean_rm[1:-1] >= amplitude_mean_rm[2:])
    )[0] + 1

    # Perioade de max 30 de zile
    period_days = 1 / (f[peaks] * 86400)
    peaks = peaks[period_days <= 30]

    idx = peaks[np.argsort(amplitude_mean_rm[peaks])[::-1][:4]]

    for i in idx:
        period_hours = 1 / (f[i] * 3600)

        print(
            f"Frequency: {f[i]:.10e} Hz, "
            f"Amplitude: {amplitude_mean_rm[i]:.4f}, "
            f"Period: {period_hours:.2f} hours"
        )

    #(g)
    start_idx = 1056                 # luni, 08-10-2012, ora 00:00
    month_samples = 30 * 24          # aproximam o lună prin 30 de zile
    end_idx = start_idx + month_samples

    x_month = x[start_idx:end_idx]

    # timpul exprimat în zile 
    t_month = np.arange(month_samples) / 24

    # plt.figure(figsize=(14, 5))
    # plt.plot(t_month, x_month)

    # plt.title("Trafic pe durata unei luni, incepand de luni")
    # plt.xticks(np.arange(0, 31, 1)) # ticks corespund zilelor dintr-o luna
    # plt.grid()
    # plt.tight_layout()
    # plt.show()

    #(h)
    # Putem observa periodicitatea semnalului zilnic (prin cresterea nivelului de trafic in fiecare seara)
    # Am observat ca se deduc si saptamanile (prin cresterea nivelului de trafic in weekend-uri)
    # astfel putem vedea cate zile si saptamani au fost "recorded" de semnalul nostru, si eventual daca am surprinde mai mult de un an am gasi
    # periodicitati inclusiv anuale (sarbatori) si de acolo sa stim clar care exact a fost luna saptamana si ziua first recorded in semnalul nostru

    # (i)
    cutoff_period_hours = 6
    cutoff_frequency = 1 / (cutoff_period_hours * 3600)

    # frecventele care corespund fiecarui coeficient FFT
    frequencies_full = np.fft.fftfreq(N, d=T)

    # coeficientii FFT for real gens
    X_filtered = X_w_mean.copy()

    # eliminam frecventele care corespund unor perioade sub 6 ore
    X_filtered[np.abs(frequencies_full) > cutoff_frequency] = 0

    # revenim în domeniul timp
    x_filtered = np.real(np.fft.ifft(X_filtered))


Lab05()

