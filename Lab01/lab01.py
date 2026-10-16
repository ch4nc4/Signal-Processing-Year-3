import numpy as np
import matplotlib.pyplot as plt

# ex1

def Lab01_ex1():
    # axa de timp (a)
    time_axis = np.arange(0, 0.03, 0.0005)

    # graficele semnalelor (b)
    # semnalele sunt: 
    # x(t) = cos(520πt + π/3), y(t) = cos(280πt − π/3), z(t) = cos(120πt + π/3).

    def x(t):
        return np.cos(520 * np.pi * t + np.pi / 3)

    def y(t):
        return np.cos(280 * np.pi * t - np.pi  / 3)

    def z(t):
        return np.cos(120 * np.pi * t + np.pi / 3)

    def plot_1_b(time_axis, axes):
        axes[0].plot(time_axis, [x(t) for t in time_axis], color='red')
        axes[1].plot(time_axis, [y(t) for t in time_axis], color='blue')
        axes[2].plot(time_axis, [z(t) for t in time_axis], color='green')

    # esantionare (c)
    def plot_1_c_sampling(sample_frecv, axes):
        axes[0].stem(sample_frecv, [x(t) for t in sample_frecv])
        axes[1].stem(sample_frecv, [y(t) for t in sample_frecv])
        axes[2].stem(sample_frecv, [z(t) for t in sample_frecv])

    fig, axs = plt.subplots(3)
    sample_frecv = np.linspace(0, 0.03, 100)
    plot_1_b(time_axis, axs)
    plot_1_c_sampling(sample_frecv, axs)

    plt.savefig("lab01_ex1.pdf", format="pdf")
    plt.close()


# ex2

# Un semnal sinusoidal de frecventa 400 Hz, care sa contina 1600 de esantioane (a)
 # formula: x[n] = sin(2 * pi * f * n/fs) 

def Lab01_ex2_a():
    f = 400 # frecventa semnalului
    fs = 20000 # frecventa sampling
    N = 1600 # nr de esantioane
    t = np.arange(N) / fs

    x_n = np.sin(2 * np.pi * f * t)
    plt.plot(t, x_n)
    plt.savefig("lab01_ex2_a.pdf", format="pdf")
    plt.close()

# Un semnal sinusoidal de frecventa 800 Hz, care sa dureze 3 secunde (b)
def Lab01_ex2_b():
    f = 800 # frecventa semnalului
    fs = 20000 # frecv sampling
    N = 60000 # nr esantioane
    t = np.arange(N) / fs

    y_n = np.sin(2 * np.pi * f * t)
    plt.plot(t, y_n)
    plt.xlim(0, 0.1) # dam zoom-in la primele 10ms ca sa putem vedea clar semnalul
    plt.savefig("lab01_ex2_b.pdf", format="pdf")
    plt.close()

# Un semnal de tip sawtooth de frecventa 240 Hz (numpy.floor sau numpy.mod) (c)
def Lab01_ex2_c():
    f = 240 # frecventa semnalului
    fs = 40000 # frecv sampling
    N = 1600 # nr esantioane
    t = np.arange(N) / fs

    z_n = f * t - np.floor(f * t)
    plt.plot(t, z_n)
    plt.savefig("lab01_ex2_c.pdf", format="pdf")
    plt.close()

# Un semnal de tip square de frecventa 300 Hz (numpy.sign) (d)
def Lab01_ex2_d():
    f = 300 # frecventa semnalului
    fs = 40000 # frecv sampling
    N = 1600 # nr esantioane
    t = np.arange(N) / fs

    w_n = np.sign(np.sin(2 * np.pi * f * t))
    plt.plot(t, w_n)
    plt.savefig("lab01_ex2_d.pdf", format="pdf")
    plt.close()

# Un semnal 2D aleator (e)
def Lab01_ex2_e():
    q_n = np.random.rand(128,128)

    plt.imshow(q_n)
    plt.savefig("lab01_ex2_e.pdf", format="pdf")
    plt.close()

# Un semnal 2D la alegerea voastra (f)
def Lab01_ex2_f():
    vals = np.linspace(0, 4 * np.pi, 128)
    q2_n = np.sin(vals[:, None]) * np.cos(vals[None, :])

    plt.imshow(q2_n, cmap="pink", aspect="auto")
    plt.savefig("lab01_ex2_f.pdf", format="pdf")
    plt.close()

# ex 3

# (a)
# frecv de esantionare de 2000 Hz => intervalul de timp dintre 2 esantioane este 1 / 2000 = 0.0005 s

# (b)
# esantion memorat pe 4 biti, 1 byte <=> 8 biti, la fiecare 0.0005s esantionam pe cate 4 biti => intr-o secunda vom ocupa 4 * 2000 = 8000 biti <=> 1000 bytes
# o ora are 60 min <=> 60 * 60 = 3600 s => o ora de achizitie va ocupa 1000 * 3600 = 3.600.000 bytes