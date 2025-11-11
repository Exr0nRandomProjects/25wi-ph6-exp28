# getting desperate for fitting voigt for ph6 
import pandas as pd
import matplotlib.pyplot as plt
from wheelbarrow.albert import style_matplotlib; style_matplotlib(plt)
from plot import plot_fit_res, plot_fit
from scipy.optimize import curve_fit
from scipy.stats import cauchy
import numpy as np

# fpath = '~/Desktop/experiment 28/data_superselect.dat'
# fpath = '~/Desktop/experiment 28/data_resonance.dat'
fpath = '~/Desktop/experiment 28/data.dat'

# fnname, fn, p0 = 'lorentzian', lambda x, m, g, c, a: c + a * cauchy.pdf(x, m, g), [-0.021, 0.5, 6e4, -1e5]
fn_descs = [
    ['lorentzian builtin', lambda x, c, a, m, g: c + a * cauchy.pdf(x, m, g), [-0.021, 0.5, 6e4, -1e5] ],
    ['lorentzian curvefit', lambda x, c, ymax, m, g: c + ymax * (g/2)**2 / ((x - m)**2 + (g/2)**2),
        # [1460, -830, -0.021, 0.15]
        [8e2, -2e2, -0.02, 0.05]
    ],
    ['gaussian curvefit', lambda x, c, ymax, m, s: c + ymax * np.exp(-(x - m)**2/(2*s**2)),
        [800, -200, -0.02, 0.02]
    ]
]
fnname, fn, p0 = fn_descs[2]

def fit_fn(xyo, fn, p0):
    x,y,o = xyo.T
    g = curve_fit(
        f=fn,
        p0=p0,
        xdata=x,
        ydata=y,
        sigma=o,
        absolute_sigma=True,
        maxfev=int(1e5),
        full_output=True,
    )
    p, cov, info, *_ = g
    chi = np.linalg.norm(info['fvec'])
    return p, np.diag(cov), chi **2 / (len(x) - len(p0))

if __name__ == '__main__':
    df = pd.read_csv(fpath, index_col=False, names=['x', 'y', 'o', ''], sep='\t')
    xyo = df[['x', 'y', 'o']].to_numpy()
    print(df)

    plot_fit_res(xyo, title=fpath.split('/')[-1])

    p, sigs, csq = fit_fn(xyo, fn, p0)
    print(p, sigs, csq)

    fig, ax, *_ = plot_fit_res(xyo, title=fpath.split('/')[-1] + f' {fnname}', fn=lambda x: fn(x, *p))
    fig, ax = plot_fit(fig, ax, lambda x: fn(x, *p0), label='init', color='gray')
    


# confirm scale param is sharpness, not constant
# if __name__ == '__main__':
#     # x = np.linspace(-1, 1, 100)
#     x = np.linspace(-0.14, 0.1, 100)
#     # y1 = cauchy.pdf(x)
#     # y2 = cauchy.pdf(x, 0, 0.5)
#     c, ymax, g, x0 = 1459.3, -828.693, 0.122531, -0.021179
#     g = 2
#     c, ymax, g, x0 = 0, 1, 1, 0
#     y3 = c + ymax * cauchy.pdf(x, x0, g)
#     y4 = c + ymax * (g/2)**2 / ((x - x0)**2 + (g/2)**2)
#     y5 = c + ymax * (g/2) / ((x - x0)**2 + (g/2)**2)
#     fig, ax = plt.subplots()
#     # ax.plot(x, y1, label='cauchy')
#     # ax.plot(x, y1*2, label='cauchy * 2')
#     # ax.plot(x, y2, label='cauchy 2')
#     ax.plot(x, y3, label='builtin')
#     ax.plot(x, y4, label='curvefit')
#     ax.plot(x, y5, label='curvefit corrected')
#     ax.legend()
#     # builtin vs custom comparison conclusion: params/fns don't line up
