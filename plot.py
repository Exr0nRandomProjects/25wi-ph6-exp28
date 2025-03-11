import matplotlib.pyplot as plt
import numpy as np
from ErrorProp import ErroredValue as val

import re

# experiment 7
# s = '''
#     List(List(20.,Around(140625.,1912.132317597294)),List(20.,Around(141376.,1917.231337110887)),
#      -  List(20.,Around(142884.,1927.4293761380725)),List(20.,Around(144400.,1937.627415165258)),
#      -  List(20.,Around(145161.,1942.7264346788509)),List(50.,Around(343396.,2822.549769268914)),
#      -  List(50.,Around(343396.,2822.549769268914)),List(50.,Around(348100.,2841.816320594982)),
#      -  List(50.,Around(348100.,2841.816320594982)),List(50.,Around(349281.,2846.632958426499)),
#      -  List(100.,Around(708964.,2300.782011983462)),List(100.,Around(708964.,2300.782011983462)),
#      -  List(100.,Around(712336.,2306.2470523919733)),List(100.,Around(712336.,2306.2470523919733)),
#      -  List(100.,Around(714025.,2308.9795725962294)),List(100.,Around(714025.,2308.9795725962294)),
#      -  List(200.,Around(1.380625e6,12806.96099783239)),List(200.,Around(1.387684e6,12839.659621656643)),
#      -  List(200.,Around(1.3924e6,12861.458704206145)),List(200.,Around(1.401856e6,12905.056869305148)),
#      -  List(200.,Around(1.413721e6,12959.554575678903)),List(300.,Around(2.082249e6,20407.10170504376)),
#      -  List(300.,Around(2.108304e6,20534.380925657337)),List(300.,Around(2.117025e6,20576.80733252853)),
#      -  List(300.,Around(2.128681e6,20633.375875023456)),List(300.,Around(2.134521e6,20661.66014627092)),
#      -  List(400.,Around(2.748964e6,29342.384442986226)),List(400.,Around(2.765569e6,29430.87173020874)),
#      -  List(400.,Around(2.775556e6,29483.96410254225)),List(400.,Around(2.808976e6,29660.93867698728)),
#      -  List(400.,Around(2.819041e6,29714.03104932079)),List(600.,Around(4.157521e6,29547.917185480263)),
#      -  List(600.,Around(4.169764e6,29591.391315718833)),List(600.,Around(4.2025e6,29707.322329688348)),
#      -  List(600.,Around(4.214809e6,29750.796459926918)),List(600.,Around(4.227136e6,29794.270590165484)),
#      -  List(800.,Around(5.546025e6,43805.532184873635)),List(800.,Around(5.583769e6,43954.340786775545)),
#      -  List(800.,Around(5.597956e6,44010.14401248876)),List(800.,Around(5.621641e6,44103.14938867745)),
#      -  List(800.,Around(5.6644e6,44270.55906581709)))
#     '''
# # fn = lambda x: 2206.7877118076212 + 7041.801171971989 * x
# fn = lambda x: 7062.3 * x


# experiment 27
# s = '''
# List(List(0.,Around(40.44,0.17406895185529223)),List(0.,Around(40.47,0.17406895185529223)),
#      -  List(0.,Around(40.53,0.17406895185529223)),List(0.,Around(40.82,0.17406895185529223)),
#      -  List(0.3333,Around(246.33000000000004,24.22758654922111)),List(0.3333,Around(288.26,24.22758654922111)),
#      -  List(0.3333,Around(291.71,24.22758654922111)),List(0.3333,Around(297.66,24.22758654922111)),
#      -  List(0.3333,Around(310.59000000000003,24.22758654922111)),List(0.5,Around(387.3,45.370641057847095)),
#      -  List(0.5,Around(416.78999999999996,45.370641057847095)),List(0.5,Around(429.14,45.370641057847095)),
#      -  List(0.5,Around(435.71000000000004,45.370641057847095)),List(0.5,Around(509.8,45.370641057847095)),
#      -  List(0.6666,Around(511.03000000000003,17.772730516158735)),
#      -  List(0.6666,Around(527.72,17.772730516158735)),List(0.6666,Around(529.45,17.772730516158735)),
#      -  List(0.6666,Around(540.45,17.772730516158735)),List(0.6666,Around(559.2,17.772730516158735)),
#      -  List(1.,Around(769.4100000000001,53.07190292424045)),
#      -  List(1.,Around(771.9300000000001,53.07190292424045)),
#      -  List(1.,Around(806.6100000000001,53.07190292424045)),
#      -  List(1.,Around(825.5500000000001,53.07190292424045)),
#      -  List(1.,Around(899.5700000000002,53.07190292424045)),List(1.3333,Around(1100.76,10.303120482002821)),
#      -  List(1.3333,Around(1101.34,10.303120482002821)),List(1.3333,Around(1113.8,10.303120482002821)),
#      -  List(1.3333,Around(1122.03,10.303120482002821)),List(1.5,Around(1209.04,19.655662542890827)),
#      -  List(1.5,Around(1239.33,19.655662542890827)),List(1.5,Around(1242.73,19.655662542890827)),
#      -  List(1.5,Around(1244.0700000000002,19.655662542890827)),
#      -  List(1.5,Around(1263.7200000000003,19.655662542890827)),List(1.6666,Around(1337.66,7.316778662772288)),
#      -  List(1.6666,Around(1349.83,7.316778662772288)),
#      -  List(1.6666,Around(1353.3000000000002,7.316778662772288)),
#      -  List(1.6666,Around(1353.9700000000003,7.316778662772288)),
#      -  List(1.6666,Around(1355.94,7.316778662772288)),List(2.,Around(1562.63,59.8277598611214)),
#      -  List(2.,Around(1587.,59.8277598611214)),List(2.,Around(1641.38,59.8277598611214)),
#      -  List(2.,Around(1658.5500000000002,59.8277598611214)),
#      -  List(2.,Around(1713.7900000000002,59.8277598611214)))
# '''
# fn = lambda x: 40.5628 + x * 788.837
# experiment 27 fit 2
s = ''' List(List(0.,Around(40.44,0.17406895185529223)),List(0.,Around(40.47,0.17406895185529223)),
     -  List(0.,Around(40.53,0.17406895185529223)),List(0.,Around(40.82,0.17406895185529223)),
     -  List(0.5,Around(387.3,45.370641057847095)),List(0.5,Around(416.78999999999996,45.370641057847095)),
     -  List(0.5,Around(429.14,45.370641057847095)),List(0.5,Around(435.71000000000004,45.370641057847095)),
     -  List(0.5,Around(509.8,45.370641057847095)),List(1.,Around(769.4100000000001,53.07190292424045)),
     -  List(1.,Around(771.9300000000001,53.07190292424045)),
     -  List(1.,Around(806.6100000000001,53.07190292424045)),
     -  List(1.,Around(825.5500000000001,53.07190292424045)),
     -  List(1.,Around(899.5700000000002,53.07190292424045)),List(1.5,Around(1209.04,19.655662542890827)),
     -  List(1.5,Around(1239.33,19.655662542890827)),List(1.5,Around(1242.73,19.655662542890827)),
     -  List(1.5,Around(1244.0700000000002,19.655662542890827)),
     -  List(1.5,Around(1263.7200000000003,19.655662542890827)),List(2.,Around(1562.63,59.8277598611214)),
     -  List(2.,Around(1587.,59.8277598611214)),List(2.,Around(1641.38,59.8277598611214)),
     -  List(2.,Around(1658.5500000000002,59.8277598611214)),
     -  List(2.,Around(1713.7900000000002,59.8277598611214)))'''
fn = lambda x: 40.5649 + x * 797.594
title = r'$B$ by $\Delta m$'
xlabel = r'$\Delta m$'
ylabel = r'$B$ [mT]'


def parse_fortran(s):
    s = s.strip()[5:-1].replace(' - ', '')
    s = s[4:-1]
    s = re.sub(r'\s*', '', s)
    s = s.split(',List')
    def per_line(l):
        l = l.strip()
        l = l.replace('(', ',').replace(')', '').split(',')
        l = l[1], l[3], l[4]
        l = [float(x) for x in l]
        return l
    s = [per_line(l) for l in s]
    return np.array(s)

def plot_xyo(fig, ax, xyo, title='', xlabel='mass [mg]', ylabel='(volts [V])$^2$', scatter_kwargs={}):
    x, y, o = xyo.T

    ax.scatter(x, y, **{ 'color': 'gray', 'edgecolor': 'black', 's': 80, **scatter_kwargs })
    ax.errorbar(x, y, yerr=o, fmt='none', color='black', elinewidth=0.5, capthick=0.5, capsize=4)
    # ax.scatter(x, y, color='yellow', edgecolor='maroon', s=80)
    # ax.errorbar(x, y, yerr=o, fmt='none', color='black', elinewidth=0.5, capthick=0.5, capsize=4)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    # ax.set_aspect("equal")

    return fig, ax

def plot_fit(fig, ax, fn, label='fit', color='maroon'):
    lo, hi = ax.get_xbound()
    scale = 0.98
    x = np.linspace(lo + (hi-lo)*(1-scale), hi-(hi-lo)*(1-scale), 100)
    y = [fn(x_) for x_ in x]
    ax.plot(x, y, label=label, color=color, lw=3)
    return fig, ax

def plot_residuals(fig, ax, xyo, fn, **kwargs):
    x, y, o = xyo.T
    yo = [val(y, o) for y, o in xyo[:, 1:]]

    residuals = [y_ - fn(x_) for x_, y_ in zip(x, yo)]


    y = [r.value for r in residuals]
    o = [r.delta for r in residuals]
    xyo = np.vstack([x, y, o]).T

    fig, ax = plot_xyo(fig, ax, xyo, **kwargs)
    ax.axhline(ls='--', color='black', lw=3)
    return fig, ax


def plot_fit_res(xyo, title='', xlabel='', ylabel='', fn=None, fn0=None, fname=None):
    # xyo = df[['x', 'y', 'o']].to_numpy()
    ret = []

    fig1, ax = plt.subplots(figsize=(5, 4))
    fig1, ax = plot_xyo(fig1, ax, xyo, title=title, xlabel=xlabel, ylabel=ylabel)
    if fn0 is not None: fig1, ax = plot_fit(fig1, ax, fn0, color='lightgray', label='init fit')
    if fn is not None: fig1, ax = plot_fit(fig1, ax, fn)
    fig1.set_size_inches(5, 4)
    plt.show()
    if fname is not None: fig1.savefig(fname + '_1.png')
    ret = [fig1, ax]

    if fn is not None:
        fig2, ax = plt.subplots(figsize=(4.8, 4))
        fig2, ax = plot_residuals(fig2, ax, xyo, fn, title='Residuals', xlabel=xlabel, ylabel=None)
        fig2.set_size_inches(4.8, 4)
        ret += [fig2, ax]
        if fname is not None: fig2.savefig(fname + '_2.png')

    return ret 



if __name__ == '__main__':
    plt.rcParams['figure.dpi'] = 200
    plt.rcParams['savefig.dpi'] = 200
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['font.size'] = 18
    plt.rcParams['axes.labelweight'] = 'bold'

    xyo = parse_fortran(s)


    fig, ax = plt.subplots(figsize=(6, 5))
    fig, ax = plot_xyo(fig, ax, xyo, title=title, xlabel=xlabel, ylabel=ylabel)
    fig, ax = plot_fit(fig, ax, fn)
    fig.set_size_inches(6, 5)

    plt.show()

    fig, ax = plt.subplots(figsize=(6, 5))
    fig, ax = plot_residuals(fig, ax, xyo, fn, title='Residuals', xlabel=xlabel, ylabel=ylabel)
    fig.set_size_inches(6, 5)

    plt.show()



