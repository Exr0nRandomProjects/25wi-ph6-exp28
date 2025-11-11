#import "../../../templates/template v9.typ": *
#show: doc => config(title: "ph6 experiment 28a report", date: datetime.today(), theme_name: "light", features: "latex units subscripts hide-doublespace expand-scientific", doc)

/*
overall fitting 
- cut off tails of resonances, remove specific sus points
- re-fit constants, discuss chi-squared, max error percent, residuals, and downstream values/errors 
- downstream: peak reduction percentage, fwhm 

data to include
- raw data table/graph if discussing individual points (anything that you refer to)
- mention how uncertainties are propagated for all values 

discuss systematic error
- mention assumptions, eg. air vs vacuum (voltmeter, exp 7)
- discuss drift, eg. look for other trends in residuals 

mention combos 
- mention all combos: compare between elements, what things were the same vs what was different, what physical differences could cause this
*/

/* 
understanding
- time-energy uncertainty:
  - some kind of "expected time taken for a state to change", in this case, to decay? 
  - if you knew how long it is going to take precisely, then you can't know the energy that well? how is time to energy as position is to momentum
  - via https://math.ucr.edu/home/baez/uncertainty.html
*/

#let fits_counter = counter("fits")
#let fit_figure(number, cols: (1fr, 0.9fr, 0.75fr), caption: [], children: none, label: none) = {
  // fits_counter.step();
  // let n = fits_counter.get().at(0);
  let n = number;
  multifig(
    tag_fn: none,
    cols: cols,
    gutter: 0pt,
    ..{
      // let n() = { (context fits_counter.get().at(0))};
      (
    image("media/exp_28_fig0_1.png".replace("0", str(n))),
    image("media/exp_28_fig0_2.png".replace("0", str(n))),
    [
      #align(horizon + center)[
        #rect(stroke: 0.3pt)[
      #table(
        columns: 2,
        align: (center, left),
        .. (if children != none {children} else {
        csv("./media/exp_28_fig0_table.csv".replace("0", str(n))).flatten().map(it => eval(it, mode: "markup"))}),
      )<baldtable>
      ]]
    ],
      )
    },
    caption: caption,
  )
}

= Introduction
In this experiment, we use the Doppler effect to measure the highly selective emission/absorption of gamma rays by $zws^(57)$Fe. This phenomenon requires the Mossbauer effect, wherein nuclear decay in a crystal can emit a photon of great energy by recoiling as a crystal unit, dumping momentum with minimal kinetic energy.

The primary sources of systematic error are in the measurement of the track length, and possible drift in the experiment electronics. The track length was measured by manually driving the carriage back and forth five times, and measuring the distance between the LED turning on and off in each direction. There was some deadspace on each end (where the LED switched at the end of that region, relative to the direction the carriage was moving), which could be unequal. This would create a mixture of populations with ±0.5% bias in either direction, but at least the variance is captured in the standard deviation. The distance measurement was 24.38 (±0.45%) mm.
Electronics drift is characterized below.

= Lorentzian Fit 
We first fit a Lorentzian by minimizing the variance-weighted square residuals of 

$
  f_l (x) = c + a (gamma slash 2)^2 / ((x - mu_0)^2 + (gamma slash 2)^2).
$

#fit_figure(0,
  cols: (1fr, 0.959fr, 0.75fr),
  caption: [Full data fit on a Lorentzian distribution using `scipy.optimize.curve_fit`.#footnote[Fitting and analysis at #link("https://github.com/Exr0nRandomProjects/25wi-ph6-exp28/blob/main/fit.py").] We follow the CurveFit convention of squaring the numerator so that the $a$ parameter represents the scale of the distribution.]
)

With a reduced $chi^2$ of 3.28 and max point error of 1.2% around resonance, this is fit is okay. It's clear, however, that some points are noisy and there is some effect in the residuals.

Despite the suboptimal fit, we can see that the count rate is reduced by $a slash c$ = 26.7 ± 2.1% at the peak, and the relative isomeric shift is $mu_0 =$ -0.209 ± 10$zws^(-6)$ mm/s. Thus the $zws^(57)$Co is likely embedded in rhodium (expected shift -0.199 mm/s) and not palladium (-0.267 mm/s).

The FWHM $gamma = 0.574 ± 10^(-4)$, however, is not the expected value. Prelab problem 2 predicts that the FWHM of two convolved 14.4keV transition Lorentzians should be about 0.193, so we are about 3x off. We remove some of the data points around the -0.19 mm/s clump to smooth out the curve and try refitting, but this has little impact on the fit FWHM.

#fit_figure(1, 
  cols: (1fr, 0.9fr, 0.75fr),
  caption: [Selected data fit on a Lorentzian distribution. Data points were removed until the curve seemed smooth, resulting in the removal of three points. Though the $chi^2$ is reduced, the fit parameters are similar to the previous fit.]
)

We can also cut off the tails to try to fit the resonance peak only. In particular, we remove the point at 0.5 mm/s, because it has a large residual and thus doesn't match the fit well.

#fit_figure(2,
  cols: (1fr, 0.95fr, 0.75fr),
  caption: [Further selected data "Peak (wide)" fit on a Lorentzian distribution. Compared to the "Selected" dataset, the 0.5 mm/s data point is removed which results in a better fit of the resonance.]
)<lorentz-peakwide>
This is a better fit of the resonance, with a reduced $chi^2$ of 1.44 and max point deviation < 1%. The FWHM $gamma = $ 0.594 ± 0.1% has increased and become less certain, but it's not much better (if at all)—we're still 3x off. A closer crop of the resonance would remove the flare that determines the peak scale, resulting in wildly uncertain fit parameters (@cropped-too-close).

#fit_figure(3,
  cols: (1fr, 0.95fr, 1.5fr),
  caption: [An even narrower crop ("Peak (narrow)") which produces a better $chi^2$ but no longer constrains the peak size.],
)<cropped-too-close>

= Gaussian Fit 
Stainless steel is an alloy, which means the that different $zws^57$Fe nuclei absorption profiles will be Lorentzians with different isometric shifts. The average absorption will thus approach a Gaussian by the CLT. Thus, we may attempt a Gaussian fit $f(x) = c + a exp(-(x-m)^2 / (2 s ^2))$:
#fit_figure(4,
  cols: (1fr, 0.95fr, 0.75fr),
  caption: [Fitting a Gaussian to the to the peak-cropped data (wide).],
)
The Gaussian seems to fit this data set better than the Lorentzian (@lorentz-peakwide), with a reduced $chi^2$ of 0.943 (vs 3.28). The maximum point deviation is similar at about 1%. Under this model, the peak count reduction is 21.7 ± 1.6 %, and the FWHM is 0.44; somewhat lower than the Lorentzian fit but still 2.3x the expected. The residuals also look better—the sinusoidal behavior is less pronounced. Re-introducing the 0.5 mm/s data point results in a worse fit (by $chi^2$) and only changes the values by ±5% (@gauss-select), so we'll leave it out.
#fit_figure(5,
  cols: (1fr, 0.95fr, 0.75fr),
  caption: [Fitting a Gaussian to the to selected full-range data. The 0.5 mm/s point doesn't fit and was rightly ignored. ],
)<gauss-select>

// #pagebreak()
= Voigt Fit  
We actually expect the distribution to be a convolution of a Lorentzian (from the emission) and the Gaussian (from the absorption). This is a Voigt function, fit below (@voigt-select). 

This fit is similar to the Gaussian fit (@gauss-select), with a reduced $chi^2$ of 0.996 and a max point error of 0.7% (compared to 0.943 and 0.9%). Though the reduced $chi^2$ is technically higher, the $chi^2$ itself is lower, which is why the fitting algorithm converged to this. Miraculously, the $gamma$ = 0.0881 ± 2.6% value is within 0.9% of the expected FWHM of the unconvolved Lorentzian ($gamma_t$ = 0.0967). Unfortunately, the value is negative, and it's not clear what influence this has in SciPy implementation of the Voigt function, though it seems to come down to #link("https://github.com/scipy/scipy/blob/08c825927d657cccc749154992a1a0487e142352/scipy/special/xsf/faddeeva.h#L635C65-L635C66")[`scipy.special.xsf.faddeeva.h` line 635]. #footnote[In the computation of the Voigt profile, the sign of $gamma$ is only used here: #link("https://github.com/scipy/scipy/blob/08c825927d657cccc749154992a1a0487e142352/scipy/special/xsf/faddeeva.h#L635C65-L635C67")[https://github.com/scipy/scipy/blob/08c825927d657cccc749154992a1a0487e142352/scipy/special/xsf/faddeeva.h#L635C65-L635C66]]

#fit_figure(6,
  cols: (1fr, 0.95fr, 0.8fr),
  caption: [Fitting a Gaussian to the to selected full-range data. The 0.5 mm/s point doesn't fit and was rightly ignored. ],
)<voigt-select>

In either case, the fit was underconstrained and the parameters very sensitive to the specific data points included. Constraining $gamma > 0$ gave $gamma$ = 0, $sigma$ = 0.187, and $chi^2/(n-5)$ = 0.999; and $gamma in [0.08, 0.1]$ gave $gamma$ = 0.08, $sigma$ = 0.173, and $chi^2/(n-5)$ = 1.006, suggesting that there are too many degrees of freedom for the $chi^2$ criterion to distinguish the quality of different $gamma$s. If we were able to predict $sigma$, maybe we could fit the best $gamma$ given that constraint; but as it stands,  it's difficult to conclude any $gamma$ values from a Voigt fit.

= Residual and Drift Analysis 
We see a similar pattern of residuals in each of the curve fits, with a peak around -0.5 mm/s, a dip around -0.25 mm/s, and another peak near -0.2mm/s. A shift in $mu_0$ would cause this pattern, but the fit $mu_0$ certainty is high and constraining it to the theoretical value results in a worse fit ($chi^2/(n-4)$ = 1.47). Perhaps some systematic error (such as differing cart travel distances in the forward and backward direction) are skewing the data points in a manner that interacts with the fit, or there is some higher order phenomenon (such as interaction with the rest of the crystal lattice) that skews the distribution away from a Lorentzian shape.


#grid(
  columns: (1fr, 1.6fr),
  [#figimg(
    image("./media/exp_28_fig8_2.png", width: 100%),
    caption: [Resid. of Gaussian on all data.]
  )
  ],
  [
  We also check the residuals for any time dependence. Here, the dark purple points were taken earlier, and the bright yellow points taken later. There seems to be no trend of between residual sign and point time, which suggests that any systematic drift was not monotonic. 

  The fact that the zero points (and their residuals) are outside of one anothers' error bars suggests that the Poisson statistics may underestimate our point uncertainties. So, there is some systematic error (as sene in the inconclusivity of the results above), but it is not a simple drift in count rates over time.

  ]
)

// TODO: voigt dist is neg 
/*
- sign of y only used here: https://github.com/scipy/scipy/blob/08c825927d657cccc749154992a1a0487e142352/scipy/special/xsf/faddeeva.h#L635C65-L635C67
- couldn't figure out the transform with my manual checking tho? 
- if you constrain it, the chi squared is like 0.99 vs 1.01, so basically the problem is underconstrained, the gaussian is very mildly better. maybe find a theory value of the gaussian and then fit ? 
*/

// TODO: electronics drift? 