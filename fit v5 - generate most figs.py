# getting desperate for fitting voigt for ph6 
import pandas as pd
import matplotlib.pyplot as plt
from wheelbarrow.albert import style_matplotlib; style_matplotlib(plt)
from wheelbarrow.albert.errorprop import ErroredValue as val
from plot import plot_fit_res, plot_fit, plot_xyo, plot_residuals
from scipy.optimize import curve_fit
from scipy.stats import cauchy
from scipy.special import voigt_profile
import numpy as np


def get_labels(lambda_fn):
    import inspect
    sig = inspect.signature(lambda_fn)
    args = [param.name for param in sig.parameters.values()]
    MATH_NAMES = {
        'ymax': 'a',
        'm': r'mu_0',
        's': r'sigma',
        'g': r'gamma',
    }
    return [MATH_NAMES[n] if n in MATH_NAMES else n for n in args]
def fit_fn(xyo, fn, p0, constrain=False):
    x,y,o = xyo.T
    constrain = {}
    # constrain = { 'bounds': (([-np.inf]*(len(p0)-1) + [0.08], [np.inf]*(len(p0)-1) + [0.1])) } if constrain else {}
    # constrain = { 'bounds': (([-np.inf]*(len(p0)-1) + [0], [np.inf]*(len(p0)-1) + [np.inf])) } if constrain else {}
    g = curve_fit(
        f=fn,
        p0=p0,
        xdata=x,
        ydata=y,
        sigma=o,
        absolute_sigma=True,
        maxfev=int(1e7),
        full_output=True,
        **constrain,
    )
    p, cov, info, *_ = g
    chi = np.linalg.norm(info['fvec'])
    return p, np.diag(cov), chi **2 / (len(x) - len(p0))
def make_xyo(fpath):
    df = pd.read_csv(fpath, index_col=False, names=['x', 'y', 'o', ''], sep='\t')
    df['x'] *= 10 # cm/s to mm/s
    xyo = df[['x', 'y', 'o']].to_numpy()
    return xyo

fn_descs = [
    ['lorentzian builtin', lambda x, c, a, m, g: c + a * cauchy.pdf(x, m, g), lambda c, a, m, g: g, [-0.021, 0.5, 6e4, -1e5] ],
    ['CF Lorentzian', lambda x, c, ymax, m, g: c + ymax * (g/2)**2 / ((x - m)**2 + (g/2)**2), lambda c, a, m, g: g,
        # [1460, -830, -0.021, 0.15]
        [8e2, -200, -0.2, 0.5]
    ],
    ['Lorentzian', lambda x, c, ymax, m, g: c + ymax * (g/2) / ((x - m)**2 + (g/2)**2), lambda c, a, m, g: g,
        # [1460, -830, -0.021, 0.15]
        [8e2, -50, -0.2, 0.5]
    ],
    ['Gaussian', lambda x, c, ymax, m, s: c + ymax * np.exp(-(x - m)**2/(2*s**2)), lambda c, a, m, s: 2 * s * np.sqrt(2 * np.log(2)),
        [800, -200, -0.2, 0.2]
    ],

    ['Voigt', lambda x, c, a, m, s, g: c + a * np.pi * voigt_profile(x-m, s, g/2), lambda c, a, m, s, g: 0.5346 * (2.35482*s) + (0.2166 * (2.35482*s)**2 + g**2)**0.5,
        # [800, -200, -0.02, -0.019, 0.05468]   # guess from params of prev fits
        # [800, -40, -0.2, 0.2, 0]               # just use gaussian
        # [800, -20, -0.2, 0.2, 0.09]               # just use lorentzian
        # [800, 100, -0.021, -0.015, -0.085]     # from fit results of above, seems pretty stable
        [ 797, -23, -0.21,  0.15, 0.088]    # manual starting with the right fwhm
    ],
    ['Voigt Centered', lambda x, c, a, s, g: c + a * np.pi * voigt_profile(x-0.199, s, g/2), lambda c, a, s, g: 0.5346 * (2.35482*s) + (0.2166 * (2.35482*s)**2 + g**2)**0.5,
        # [800, -200, -0.02, -0.019, 0.05468]   # guess from params of prev fits
        # [800, -40, -0.2, 0.2, 0]               # just use gaussian
        # [800, -20, -0.2, 0.2, 0.09]               # just use lorentzian
        # [800, 100, -0.021, -0.015, -0.085]     # from fit results of above, seems pretty stable
        [ 797, -23, 0.15, 0.088]    # manual starting with the right fwhm
    ]
]

data_descs = [
    ['~/Desktop/experiment 28/data_superselect.dat', 'Selected 2'],
    ['~/Desktop/experiment 28/data.dat', 'Full Data'],
    ['~/Desktop/experiment 28/data_selected.dat', 'Selected'],
    ['~/Desktop/experiment 28/data_resonance.dat', 'Peak (narrow)'],
    ['~/Desktop/experiment 28/data_resonance_wider.dat', 'Peak (wide)'],
    ['~/Desktop/experiment 28/data_resonance_wider_2.dat', 'Peak (wide2)'],
]

def str_percent(v, p=4):
    def h(v, p=2):
        if v < 10**(-p):
            return f'{v:.0e}'
        elif v < 1:
            return v.__format__(f'.{p}f')
        elif v < 10**(p):
            return v.__format__(f'.{p}g')
        elif v < 10**(p+1):
            return v.__format__(f'.{p+1}g')
            # return v.__format__(f'.1g')
            # return v.__format__('')
        else:
            return v.__format__(f'.0e')
    return f'{float(v.value).__format__(f".{p if v.value > 1 else p-1}g")} ± {h(abs(float(v.delta_rel)))}%'

def make_fig(fig_i, d_idx, fn_idx):
    fpath, dname = data_descs[d_idx]
    fnname, fn, get_fwhm, p0 = fn_descs[fn_idx]

    xyo = make_xyo(fpath)

    # plot_fit_res(xyo, title=fpath.split('/')[-1], xlabel='count rate', ylabel='v [mm/s]')

    p, sigs, csq = fit_fn(xyo, fn, p0, constrain=fig_i == 6) 

    fig, ax, fig2, ax2 = plot_fit_res(
        xyo,
        title=f'{dname} · {fnname}',
        fn=lambda x: fn(x, *p),
        # fn0=lambda x: fn(x, *p0),
        xlabel='count rate',
        ylabel='v [mm/s]',
        fname=f'./media/exp_28_fig{fig_i}',
    )
    plt.show()

    print(p, sigs, csq, '\n')
    vals = []
    table_str = []
    for v, vs, label in zip(p, sigs, get_labels(get_fwhm)):
        vl = val(v, vs)
        # table_str.append((f'${label:11}$', f'{v:.3g} ± {abs(float(vl.delta_rel)*100):.2g}%'))
        table_str.append((f'${label:11}$', str_percent(vl)))
        vals.append(vl)
    table_str.append((f'$chi^2/(n-{len(p0)})$', f'{csq:.3g}'))
    with open(f'./media/exp_28_fig{fig_i}_table.csv', 'w') as f:
        import csv
        csvw = csv.writer(f)
        csvw.writerows(table_str)
    print('\n'.join(f'{a}: {b}' for a, b in table_str))

    c, a, m, *_ = vals
    fwhm = get_fwhm(*vals)

    print()
    print(f'count reduction', (a / c * 100), '%')
    print(f'fwhm           ', fwhm)


figures = [
    (1, 1), # lorentzian on everything
    (2, 1), # lorentzian on selected
    (4, 1), # lorentzian on resonance (wide)
    (3, 1), # lorentzian on resonance (narrow)
    (4, 3), # gaussian   on resonance (wide)
    (2, 3), # gaussian   on selected
    (4, 4), # voigt      on resonance (wide)
    (4, 5), # voigt c    on resonance (wide)
]

if __name__ == '__main__':
    # print('dist', val([2.44, 2.44, 2.45, 2.42, 2.44])*10, 'mm')

    for i, f in enumerate(figures):
        print(f'{'#'*30}\nFigure {i+1}/{len(figures)}')
        make_fig(i, *f)

    # make scatter plot 


    # x = val(123456.789, 1.987654321)
    # for i in range(12):
    #     print(str_percent(x))
    #     x /= 10 
    #     x.delta = 1.987654321