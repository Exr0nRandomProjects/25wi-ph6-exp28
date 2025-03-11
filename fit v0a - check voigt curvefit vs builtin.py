
from scipy.special import voigt_profile
from matplotlib import pyplot as plt
import numpy as np 

# if __name__ == '__main__':
#     c, a, m, s, g = 0, 1, 0, 0, 1
    # lorentzian_custom = lambda x: c + a * (g/2)**2 / ((x - m)**2 + (g/2)**2)
#     x = np.linspace(-0.5, 0.5, 100)
#     y1 = lorentzian_custom(x)
#     y2 = c + a * voigt_profile(x-m, s, g)
#     y2 = c + a * 

#     fig, ax = plt.subplots()
#     ax.plot(x, y1, label='custom lorentz')
#     ax.plot(x, y2, label='builtin voigt')
#     ax.legend()

if __name__ == '__main__':
    from scipy.signal import convolve
    x, dx = np.linspace(-10, 10, 500, retstep=True)
    def gaussian(x, sigma):
        return np.exp(-0.5 * x**2/sigma**2)/(sigma * np.sqrt(2*np.pi))
    # def cauchy(x, gamma):
    #     return gamma/(np.pi * (np.square(x)+gamma**2))


    cauchy = lambda x, g: g/2 / ((x)**2 + (g/2)**2)
    sigma = 0
    gamma = 1
    gauss_profile = gaussian(x, sigma)
    cauchy_profile = cauchy(x, gamma)
    convolved = dx * convolve(cauchy_profile, gauss_profile, mode="same")
    voigt = np.pi * voigt_profile(x, sigma, gamma/2)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x, gauss_profile, label="Gauss: $G$", c='b')
    ax.plot(x, cauchy_profile, label="Cauchy: $C$", c='y', ls="dashed", lw=10)
    xx = 0.5*(x[1:] + x[:-1])  # midpoints
    ax.plot(xx, convolved[1:], label="Convolution: $G * C$", ls='dashdot',
            c='k')
    ax.plot(x, voigt, label="Voigt", ls='dotted', c='r')
    ax.legend()
    plt.show()