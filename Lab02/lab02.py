import numpy as np
import matplotlib.pyplot as plt
import scipy 
import sounddevice as sd

# ex1
def Lab02_ex1():    
    f = 200 # frecventa semnalului
    fs = 20000 # frecventa sampling
    N = 1600 # nr de esantioane
    t = np.arange(N) / fs

    x_n = np.sin(2 * np.pi * f * t + np.pi/2)
    y_n = np.cos(2 * np.pi * f * t)
    fig, axs = plt.subplots(2)

    axs[0].plot(t, x_n, color = 'red')
    axs[0].set_title('sine')
    axs[1].plot(t, y_n, color = 'blue')
    axs[1].set_title('cosine')
    plt.savefig("lab02_ex1.pdf", format="pdf")
    plt.close()


# ex2
def Lab02_ex2():
    f = 200 # frecventa semnalului
    fs = 20000 # frecventa sampling
    N = 1600 # nr de esantioane
    t = np.arange(N) / fs

    def sine_with_phase(phase):
        return np.sin(2 * np.pi * f * t + phase)

    SNR = [0.1, 1, 10, 100]
    x_norm = np.linalg.norm(sine_with_phase(np.pi/3))
    z_norm = np.linalg.norm(np.random.normal(size=1600))
    x = sine_with_phase(np.pi/3)
    z = np.random.normal(size=1600)

    def get_gamma(SNR_val):
        return x_norm / (np.sqrt(SNR_val) * z_norm)

    fig, axs = plt.subplots(4)
    axis = 0
    for val in SNR:
        gamma = get_gamma(val)
        axs[axis].plot(t, x + gamma * z)
        axis += 1
        
    plt.savefig("lab02_ex2_noise.pdf", format="pdf")
    plt.close()
    
    plt.plot(t, sine_with_phase(np.pi/2), color='red')
    plt.plot(t, sine_with_phase(np.pi/3), color='blue')
    plt.plot(t, sine_with_phase(-np.pi/3), color='green')
    plt.plot(t, sine_with_phase(3 * np.pi), color='orange')
    plt.savefig("lab02_ex2_no_noise.pdf", format="pdf")
    plt.close()


# ex3
def signal_sine(f, fs, N):
    t = np.arange(N)/fs
    return np.sin(2 * np.pi * f * t)

def signal_sawtooth(f, fs, N):
    t = np.arange(N)/fs
    return f * t - np.floor(f * t)

def signal_square(f, fs, N):
    t = np.arange(N)/fs
    return np.sign(np.sin(2 * np.pi * f * t))

def Lab02_ex3():
    sd.default.samplerate = 44100
    rate = int(10e5)
    # scipy.io.wavfile.write('lab02_ex3.wav', rate, signal_sine(400, 44100, 44100))
    sd.play(signal_sine(400, 44100, 44100))
    sd.play(signal_sine(800, 44100, 3 * 44100))
    sd.play(signal_sawtooth(240, 44100, 2 * 44100))
    sd.play(signal_square(300, 44100, 2 * 44100))

    sd.wait()


# ex4
def Lab02_ex4():
    t = np.arange(1600)/44100
    x = signal_sine(600, 44100, 1600)
    y = signal_sawtooth(200, 44100, 1600)

    fig, axs = plt.subplots(3)
    axs[0].plot(t, x, color='red')
    axs[1].plot(t, y, color='blue')
    axs[2].plot(t, x + y, color = 'green')
    plt.savefig("lab02_ex4.pdf", format="pdf")
    plt.close()

# ex5
# Nota: Observam clar diferenta cand se trece de la primul semnal (de frecventa mai mica)
# la al doilea semnal (de frecventa mai inalta) prin tonalitatea mai ridicata al celui de-al doilea semnal
def Lab02_ex5():
    sine_1 = signal_sine(400, 44100, 3 * 44100)
    sine_2 = signal_sine(800, 44100, 3 * 44100)
    both_sine = np.append(sine_1, sine_2)

    rate = int(10e5)
    sd.default.samplerate = 44100
    # scipy.io.wavfile.write('lab02_ex5.wav', rate, both_sine)
    # rate, x = scipy.io.wavfile.read('lab02_ex5.wav')
    # sd.play(x)
    sd.play(both_sine)
    sd.wait()

# ex 6
# Nota: Din formula pentru semnale sinusoidale: sin(2 * pi * f * N / fs) observam urmatoarele
# f = fs/2 => semnalul va fi sin(pi * N) = 0 => graficul arata ca o linie dreapta trecand prin origine
# f = fs/4 => semnalul va fi sin(pi/2 * N) = +-(1) => graficul arata ca niste zimti de cu varfurile in 1 si -1
# f = 0 Hz => semnalul va fi sin(0) = 0 => graficul arat ca o linie dreapta trecand prin origine

# in plus: original primul semnal sinusoidal (cu f = fs/2) este plotat cu precizie foarte mare
# astfel incat sa se poata vedea micile oscilatii ale lui sin(pi * N) in jurul lui 0
# la scara mai mare a axei y ([-1, 1] sa zicem) ele nu mai sunt vizibile
def Lab02_ex6():
    t = np.arange(1600)/4000
    sine_a = signal_sine(2000, 4000, 1600) # f = fs/2
    sine_b = signal_sine(1000, 4000, 1600) # f = fs/4
    sine_c = signal_sine(0, 4000, 1600) # f = 0 Hz

    fig, axs = plt.subplots(3)
    axs[0].plot(t, sine_a, color='green')
    axs[0].set_xlim(0, 0.05)
    axs[1].plot(t, sine_b, color='blue')
    axs[1].set_xlim(0, 0.05)
    axs[2].plot(t, sine_c, color='red')
    axs[2].set_xlim(0, 0.05)
    plt.savefig("lab02_ex6.pdf", format="pdf")
    plt.close()

# ex 7
# Nota: Pentru ca am rarit punctele de sampling (prin decimare) nu mai putem sa surprindem acelasi semnal (avem prea putine puncte de sampling)
# prin a decima la acelasi rate dar incepand de la al doilea element din array adaugam practic o faza semnalului decimat
def Lab02_ex7():
    t_initial = np.arange(900)/1000
    t_first = t_initial[::4]
    t_second = t_initial[1::4]

    initial_signal = signal_sine(800, 1000, 900)
    decimate_first = np.array([])
    decimate_second = np.array([])

    for idx in range(0, np.size(initial_signal)):
        if(idx % 4 == 0):
            decimate_first = np.append(decimate_first, initial_signal[idx])

    idx = 1;
    while(idx < np.size(initial_signal)):
        decimate_second = np.append(decimate_second, initial_signal[idx])
        idx += 4

    fig, axs = plt.subplots(3)
    axs[0].plot(t_initial, initial_signal, '.-', color='red')
    axs[0].set_xlim(0, 0.2)
    axs[1].plot(t_first, decimate_first, '.-', color='blue')
    axs[1].set_xlim(0, 0.2)
    axs[2].plot(t_second, decimate_second, '.-', color='green')
    axs[2].set_xlim(0, 0.2)
    plt.savefig("lab02_ex7.pdf", format="pdf")
    plt.close()

# ex 8
def Lab02_ex8():
    bins = np.arange(-np.pi/2, np.pi/2, 0.01)
    fig, axs = plt.subplots(4, 2)
    pade = (bins - 7 * pow(bins, 3)/60)/(1 + pow(bins, 2)/20)

    axs[0][0].plot(bins, np.sin(bins), color='red')
    axs[0][0].plot(bins, bins, color='blue')
    axs[0][0].grid()

    axs[1][0].plot(bins, abs(np.sin(bins)-bins), color='green')
    axs[1][0].grid()

    axs[2][0].plot(bins, np.sin(bins), color='red')
    axs[2][0].plot(bins, pade, color='blue')
    axs[2][0].grid()

    axs[3][0].plot(bins, abs(np.sin(bins)-pade), color='green')
    axs[3][0].grid()

    axs[0][1].plot(bins, np.sin(bins), color='red')
    axs[0][1].plot(bins, bins, color='blue')
    axs[0][1].set_yscale('log')
    axs[0][1].grid()

    axs[1][1].plot(bins, abs(np.sin(bins)-bins), color='green')
    axs[1][1].set_yscale('log')
    axs[1][1].grid()

    axs[2][1].plot(bins, np.sin(bins), color='red')
    axs[2][1].plot(bins, pade, color='blue')
    axs[2][1].set_yscale('log')
    axs[2][1].grid()

    axs[3][1].plot(bins, abs(np.sin(bins)-pade), color='green')
    axs[3][1].set_yscale('log')
    axs[3][1].grid()

    plt.savefig("lab02_ex8.pdf", format="pdf")
    plt.close()

