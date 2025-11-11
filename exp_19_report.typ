#import "../../../templates/template v9.typ": *
#show: doc => config(title: "ph6 experiment 19 report", date: datetime.today(), theme_name: "light", features: "latex units subscripts hide-doublespace chem", doc)

#show regex("(\d|\.)+e-?(\d+)"): it => {
  let (b, e) = it.text.match(regex("((?:\d|\.)+)e-?0*(\d+)")).captures
  $#b times 10^(-#e)$
}

/*
how to do the report better 

from alex (exp 28a mossbauer)
- put the actual chi-squared number and "greatest deviation %"
- analyze specific data points in the data/residual. eg. plot against time.
  (attempt to account for drift, chi-squared increases. but you attempt)
from experiment 7 (kelvin absolute voltmeter)
- check assumptions by comparing to a better model (eg. vacuum instead of air in voltmeter (exp 7))
- check all error sources (eg. mention V uncertanties)
from experiment 12 (electron diffraction)
- mention all combos: compare between elements, what things were the same vs what was different, what physical differences could cause this
- [x] analyze residual plots (talk about if theres a correlation, look at specific points)
- [x] detail error propogation and sources. talk about all error sources!

*/

= Introduction

In this experiment, we measure the index of refraction of air, CO2, and He gas by counting the number of wavelength shifts caused by a gas as we vary chamber pressure.

Because the experiment was relatively automated, the major sources of systemic error are in miscalibrated measuring instruments (eg. calipers, thermometer, and barometer). The temperature was re-measured before and after the trials for each gas, and the mean was used (and standard deviation propagated) in the calculations. Section 2 is also sensitive to the imperfection of the vacuum pump. Section 3 reduces this sensitivity by comparing relative fringe counts, though it may still be affected by a drift in vacuum pump efficacy. 

= Indices of Refraction

First, we determine the index of refraction using the equation from Prelab Problem 1:
$
m = 2(n-1) L / lambda_"vac" quad => quad n-1 = m/2 lambda_"vac"/L
$<n-basic>
where $m$ is the difference in number of wavelengths between the cell near vacuum and at 1 atmosphere, which is also the fringe count. 
By the ideal gas law, $N prop P / T$
so we find $(n-1)$ at standard temperature and pressure (0.C, 1 atm) by multiplying
$ (n-1)' = (n-1) (P' T_0)/(T' P_0). $<n-adj>

Using $L = 18.6926 ± 0.011$ cm, and standard values for the $lambda_"vac"$ for red (632.99 nm) and green (543.52 nm) light, and propagating uncertainties, #footnote([#link("https://github.com/Exr0nProjects/pyerr/blob/25wi-ph6/ph6_exp19.py")]) we obtain @indices-of-refraction.

#tablefig(
  // title: "Indices of Refraction",
  header: ("Gas", "Light", [Measured $n-1$], [$n-1$ \@ STP], [$plus.minus sigma$], /*[Error from Accepted]*/),
[Air], [Red],   [2.589e-04], [2.883e-04], [±0.20%], 
[Air], [Green], [2.602e-04], [2.897e-04], [±0.16%],
[CO2], [Red],   [3.946e-04], [4.401e-04], [±0.12%],
[CO2], [Green], [3.967e-04], [4.425e-04], [±0.20%],
[He], [Red],    [3.271e-05], [3.647e-05], [±1.20%],
[He], [Green],  [3.254e-05], [3.628e-05], [±0.50%],
caption: [Measured and adjusted indices of refraction for red and green lasers in air, CO2, and He gas. Uncertainties are propagated following the computation @n-basic and @n-adj.]
)<indices-of-refraction>

Matching the data rejection in @nums-and-freqs instead gives a helium, red refractive index of $3.62 times 10^(-5)$, which is marginally closer to the accepted value of $3.485 times 10^(-5)$. #footnote([A. Ermolov, et. al. Phys. Rev. A *92*, 033821 (2015). #link("https://doi.org/10.1103/PhysRevA.92.033821").
])

// There are not many residuals to analyze, but some data points were 

// air green (use equilibrium): 2.897 -> 2.899, target 2.77 via https://refractiveindex.info/?shelf=other&book=air&page=Ciddor
// co2 green (reject low point): 3.967 -> 3.970, target: 4.504 via https://refractiveindex.info/?shelf=main&book=CO2&page=Bideau-Mehu
// helium red (reject first 2): helps a bit. target: 3.485, we got 3.647 -> 3.620 https://journals.aps.org/pra/abstract/10.1103/PhysRevA.92.033821 (via refractiveindex.info)

= Oscillation Electrons and Resonant Frequency
With the empirical indices of refraction for two wavelengths for each gas, we can compute the resonant wavelength $lambda_0$ and number of oscillating electrons $n_e$ in the model, using the equations from Prelab Problem 3. Propagating uncertainties, we obtain @nums-and-freqs.

#tablefig(
  header: ("Gas", [$lambda_0$ [m]], [$n_e$], [$E_0$ [eV]], [$plus.minus_% sigma $]),
  [Air], [7.333e-08], [4.388], [16.91], [±52.37%],
  [CO2], [7.687e-08], [6.087], [16.13], [±44.01%],
  [He], [4.925e-08], [1.231], [25.18], [±327.35%],
  caption: [Computed $lambda_0$ and $n_e$ values. Helium values are computed from restricted data, see below.]
)<nums-and-freqs>

The original helium data led to negative $n_0$ and imaginary $lambda_0$. However, upon closer inspection of the (helium, red) data, we find the first two trials yielded measurements that were 21% (41 standard deviations) higher than the measurements in the last four trials. This may be because the previous gas had not yet been fully flushed from the chamber before helium trials begun. The helium values in @nums-and-freqs are computed from the last four trials. 

$n_e$ seems to be related to the number of valence electrons in the molecule, with He < air < CO2 on the $n_e$ scale, but it's difficult to tell due to the high uncertainties in the values. 

The energies $E_0$ do miraculously seem to align with the ionization energies of the molecules. The percent error for He energy is 2.3%, and for CO2, 18%, which is within one standard deviation of uncertainty. The measured $E_0$ for air is within 8.4% of the ionization energy of N2, which is the main component of air. This makes sense if the laser light is exciting electrons, whose energies are quantized to the ionization energies. 

We can be more aggressive with data point quality. A few of the (air, green) data points were possibly taken before the apparatus equilibrated (the fringes would settle after a few seconds of jittering); we use the final values instead. One (CO2, green) data point was 1 fringe (0.4%, 10.5$sigma$) below the other data points for that condition, which we remove. Finally, the balloon seemed stuck for one data point, so we use the equilibrated fringe count after squeezing the balloon. This gives @computed-2.

#tablefig(
  header: ("Gas", [$lambda_0$ [m]], [$n_e$], [$E_0$ [eV]], [$plus.minus_% sigma $]),
  [Air], [7.657e-08], [4.019], [16.19], [±43.05%],
  [CO2], [8.175e-08], [5.372], [15.17], [±28.59%],
  [He], [4.925e-08], [1.231], [25.18], [±327.35%],
  caption: [Computed $lambda_0$ and $n_e$ values, with more aggressive data restriction. ]
)<computed-2>
The new $E_0$s have percent error 3.6%, 9.1%, and 2.3%, respectively, where air is compared to N2 ionization energy of N2 gas, though accounting for oxygen would drag it lower. The $n_e$ values more also more closely match the number of free valence electrons in each molecule (4, 4, and 2 respectively), where $n_e$ of CO2 may be inflated by the additional bonding electrons relative to N2 and O2, and the $n_e$ of He deflated due to the stronger interaction between the nucleus and the valence shell in He than in larger atoms. 

// 15.6, 13.8, 24.6