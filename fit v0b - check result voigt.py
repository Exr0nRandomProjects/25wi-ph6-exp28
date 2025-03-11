import numpy as np
from matplotlib import pyplot as plt 
from fit import make_xyo, data_descs
from scipy.special import voigt_profile

fpath, dname = data_descs[4]

if __name__ == '__main__':
    # p = [ 8.20688526e+02, -3.52269968e+01, -2.10722683e-01,  1.57177662e-01, 1.71562734e-01] 
    p = [ 7.97570111e+02, -2.23255455e+01, -2.10905894e-01,  2.00861895e-01, -8.80443500e-02]  # best fit, but neg gamma
    p_massage = [ 7.97570111e+02, -2.23255455e+01, -2.10905894e-01,  2.00861895e-01, -8.80443500e-02]  # best fit, but neg gamma
    # p = [ 7.97570111e+02, -23.3255455, -2.10905894e-01,  0.15, 8.80443500e-02]    # manual fit
    c, a, m, sigma, gamma = p
    # gamma = 0.0967

    xyo = make_xyo(fpath)

    fig, ax = plt.subplots()
    ax.scatter(xyo[:, 0], xyo[:,1])


    from scipy.signal import convolve
    x, dx = np.linspace(-0.7, 0.7, 500, retstep=True)
    def gaussian(x, sigma):
        return np.exp(-0.5 * x**2/sigma**2)/(sigma * np.sqrt(2*np.pi))
    def cauchy(x, g):
        return (g/2) / ((x)**2 + (g/2)**2)

    gauss_profile = gaussian(x, sigma)
    cauchy_profile = cauchy(x, gamma)
    convolved = dx * convolve(cauchy_profile, gauss_profile, mode="same")
    voigt = lambda x, c, a, m, s, g: c + a * np.pi * voigt_profile(x-m, s, g/2)

    ax.plot(x+m, c+a*convolved, label='fit')
    ax.plot(x+m, voigt(x, c, a, 0, sigma, gamma), label='voigt')
    # ax.plot(x+m, c+a*gaussian(x, sigma), label='gaussian')
    # ax.plot(x+m, c+a*cauchy(x, gamma), label='lorentian')

    # ax.plot(x+m, c+a*cauchy(x, 0.19), label='convolved 2 lorentzs')
    # ax.plot(x+m, c+a*1.3*cauchy(x, 0.47), label='lorentz w that fwhm')
    ax.legend()

    plt.show()

    f_g = 2 * sigma * np.sqrt(2 * np.log(2))
    f_l = gamma
    print('fwhm of voigt!', 0.5346 * f_l + np.sqrt(0.2166 * f_l**2 + f_g**2))



    
