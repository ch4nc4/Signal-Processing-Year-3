import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

def plot_real_pts(axis, line):
    axis.plot(np.real(line), color='red')

def plot_imag_pts(axis, line):
    axis.plot(np.imag(line), color='blue')

def signal_sine(f, fs, N):
    t = np.arange(N)/fs
    return np.sin(2 * np.pi * f * t)

# ex1
def Lab03_ex1():
    N = 8

    vec = np.arange(0, N) 
    i_dot_j = np.outer(vec, vec)

    fourier_matrix = math.e**(-2 * np.pi * 1j * i_dot_j / N)

    F_H = fourier_matrix.conjugate().T
    F_H_F = F_H @ fourier_matrix
    is_unitary = np.allclose(F_H_F, N * np.identity(N))
    print("Fourier Matrix is unitary: ", is_unitary)

    fig, axs = plt.subplots(8, 2)
    plot_real_pts(axs[0][0], fourier_matrix[0])
    plot_imag_pts(axs[0][1], fourier_matrix[0])

    plot_real_pts(axs[1][0], fourier_matrix[1])
    plot_imag_pts(axs[1][1], fourier_matrix[1])

    plot_real_pts(axs[2][0], fourier_matrix[2])
    plot_imag_pts(axs[2][1], fourier_matrix[2])

    plot_real_pts(axs[3][0], fourier_matrix[3])
    plot_imag_pts(axs[3][1], fourier_matrix[3])

    plot_real_pts(axs[4][0], fourier_matrix[4])
    plot_imag_pts(axs[4][1], fourier_matrix[4])

    plot_real_pts(axs[5][0], fourier_matrix[5])
    plot_imag_pts(axs[5][1], fourier_matrix[5])

    plot_real_pts(axs[6][0], fourier_matrix[6])
    plot_imag_pts(axs[6][1], fourier_matrix[6])

    plot_real_pts(axs[7][0], fourier_matrix[7])
    plot_imag_pts(axs[7][1], fourier_matrix[7])

    plt.savefig("lab03_ex1.pdf", format="pdf")
    plt.close()


# ex2
def OnUnitCircle(omega, frecv):
    t = np.arange(0, 1, 0.001)
    x = np.sin(2 * np.pi * frecv * t)
    y = x * math.e**(-2 * np.pi * 1j * omega * t)

    distances = np.abs(y)

    return y, distances

def Lab03_ex2_plots():
    fig, axs = plt.subplots(2, 2)

    val, dist = OnUnitCircle(1, 10)   
    im = axs[0][0].scatter(
        val.real, val.imag,
        c = dist,
        cmap="plasma",
        s=5
    )
    axs[0][0].set_title("omega = 1")
    axs[0][0].grid()
    axs[0][0].set_aspect("equal")

    val, dist = OnUnitCircle(2, 10)
    im = axs[0][1].scatter(
        val.real, val.imag,
        c = dist,
        cmap="plasma",
        s=5
    )
    axs[0][1].set_title("omega = 2")
    axs[0][1].grid()
    axs[0][1].set_aspect("equal")

    val, dist = OnUnitCircle(10, 10)
    im = axs[1][0].scatter(
        val.real, val.imag,
        c = dist,
        cmap="plasma",
        s=5
    )
    axs[1][0].set_title("omega = 10 (eq to signal frequency)")
    axs[1][0].grid()
    axs[1][0].set_aspect("equal")

    val, dist = OnUnitCircle(7, 10)
    im = axs[1][1].scatter(
        val.real, val.imag,
        c = dist,
        cmap="plasma",
        s=5
    )
    axs[1][1].set_title("omega = 7")
    axs[1][1].grid()
    axs[1][1].set_aspect("equal")

    fig.tight_layout()

    plt.show()
    # plt.savefig("lab03_ex2_colors.pdf", format="pdf")
    # plt.close()

def AnimatePlots(fig, ax, omega):
    val, dist = OnUnitCircle(omega, 10)   
    points = np.column_stack((val.real, val.imag))

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect("equal")
    ax.grid()
    ax.set_title(f"omega = {omega}")

    # Initially empty trail
    trail = ax.scatter(
        [], [], c=[], cmap="viridis",
        vmin=0, vmax=1, s=5
    )

    # Marker showing the current point
    head, = ax.plot([], [], "ro", markersize=6)

    def update(i):
        # Show samples 0 through i
        trail.set_offsets(points[:i + 1])
        trail.set_array(dist[:i + 1])

        # Move the red marker to sample i
        head.set_data([val.real[i]], [val.imag[i]])

        return trail, head

    ani = FuncAnimation(
        fig,
        update,
        frames=len(val),
        interval=20,   # Delay between frames, in milliseconds
        blit=True,
        repeat=False
    )
    return ani

def Lab03_ex2_animations(omegas):
    fig, axs = plt.subplots(2, 2)

    animations = [
        AnimatePlots(fig, ax, omega)
        for ax, omega in zip(axs.flat, omegas)
    ]

    fig.tight_layout()
    plt.show()

    return animations

    # code for saving the animations one by one
    # for omega in omegas:
    #     fig, ax = plt.subplots()

    #     ani = AnimatePlots(fig, ax, omega)
    #     fig.tight_layout()

    #     ani.save(
    #         f"omega_{omega}.gif",
    #         writer="pillow",
    #         fps=50
    #     )
    #     plt.close(fig)


#ex 3
def Lab03_ex3():
    f1 = 3
    f2 = 7
    f3 = 10
    N = 1000
    fs = 1000

    n = np.arange(N)
    t = np.arange(N)/fs
    x = np.cos(2 * np.pi * f1 * t) + 2 * np.cos(2 * np.pi * f2 * t) + 0.5 * np.cos(2 * np.pi * f3 * t)

    bins = np.arange(31)
    magnitudes = []
    for k in bins:
        X = np.sum(x * np.exp(-2j * np.pi * n * k / N))
        magnitudes.append(np.abs(X))

    plt.stem(bins, magnitudes)
    # plt.show()
    plt.savefig("lab03_ex3.pdf", format="pdf")
    plt.close()

Lab03_ex3()