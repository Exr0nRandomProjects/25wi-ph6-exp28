#import "../../../templates/template v9.typ": *
#show: doc => config(title: "ph6 experiment 27 report", date: datetime.today(), theme_name: "light", features: "latex units subscripts hide-doublespace", doc)

// conditionally number equations: https://forum.typst.app/t/how-to-conditionally-enable-equation-numbering-for-labeled-equations/977/16
#set math.equation(numbering: "(1)")
#show math.equation: it => {
  if it.block and not it.has("label") [
    #counter(math.equation).update(v => v - 1)
    #math.equation(it.body, block: true, numbering: none)#label("")
  ] else {
    it
  }  
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
= Procedure 
In this experiment, we aim to measure the electron charge-to-mass ratio by observing how the spectral lines of neon shift under a magnetic field. For each data point, the magnetic field voltage was varied until the spectral lines visually had a shift of $Delta m$, then the magnetic field was measured using a hall probe.

To decrease systematic error from voltage set point and hall probe placement, those sources of error were incorporated into the data sampling cycle: for each point, the electromagnet voltage was adjusted randomly up or down away from the target $Delta m$, then adjusted back until the $Delta m$ matched visually. Then the neon lamp was lowered, the hall probe was inserted, the measurement was taken to be the first number seen on the hall probe voltmeter (which fluctuates at a few hertz). The voltage was adjusted randomly up and down between measurements to reduce any systematic error that could be caused by always adjusting in one direction.

= Curve Fitting

In this experiment, we manipulate a the electromagnet voltage and measure the hall effect voltage. We have the relation 
$
  B = (2 pi c)/d m/abs(e) Delta m
$<og-eqn>
which predicts that the strength of the $B$-field is proportional to $Delta m$. We assume that the Hall effect is linear and proxy $B$ from our measured voltages with 1 $mu$V = 1 Gauss = 0.1 mT. 

Though the hall probe was zeroed before the experiment, the magnetic field value in the magnet with electromagnet voltage set to zero was measured at $38.356 ±_sigma 0.0185$ mT, so some constant offset is expected. We use a linear fit, and indeed see a constant offset that's within 5.8% the measured constant offset.

#multifig(
  tag_fn: none,
  cols: (1fr, 1fr, 0.5fr),
  image("media/2025-02-22-16-59-00.png"),
  image("media/2025-02-22-16-58-04.png"),
  [
    #align(horizon + center)[
      #rect(stroke: 0.3pt)[
    #table(
      columns: 2,
      align: (center, left),
      [$a$], [40.5628],
      [$b$], [788.837],
      [$sigma_a$], [0.0870],
      [$sigma_b$], [1.642],
      [$chi^2/(n-1)$], [1.729]
    )<baldtable>
    ]]

  ],
  caption: [Linear fit of $B$ against $Delta m$. The fit seems decent, with a maximum point deviation 6.7% and a reduced chi-squared that suggests the model holds with some systematic error. We see evidence of this in the residuals.]
)
Before fitting, uncertainties were assigned and the Y values were divided by 10 to convert from Gauss to milliteslas.

This data looks acceptably linear, with a maximum individual data point deviation of 6.7% in the highest uncertainty region $Delta m = 2$. The reduced chi-squared of 1.729 agrees that this fit captures the main trend of the data, though the noise is high. 

Examining the residual plot, we see that the $Delta m$ values with the highest spread are 0.5, 1, and 2. These are the values where the interference pattern had the most overlap, which also meant there were fewer signs of the $Delta m$ being slightly off, leading to a greater spread. 

On the other hand, the $Delta m in {1/3, 2/3, 4/3, 5/3}$ data points have a smaller standard deviation.
This may be because for these data points, I stopped inserting the hall probe visually, and instead started aligning it by matching the back of the sliding base to the slider guide, which would decrease variance but possibly introduce another constant offset relative to our zero reference (possibly explaining our 5.8% deviation from the expected constant offset).

This may also be because these data points were gathered by adjusting the electromagnet until the interference pattern was "equally between" the $n + 0.5$ pattern and the $n in NN$ pattern, ie. it didn't look more like one than the other. This was a much finer adjustment procedure, which understandably led to a tighter spread. This different adjustment procedure would introduce a systematic error in these $Delta m$ values, because I was looking for a pattern that may not correspond to $Delta m = n 1/3$. The systematic error introduced would by symmetric about $Delta m = 0.5, 1.5$, and indeed we see that the means at $Delta m = 1/3, 4/3$ are skewed higher than the means seen at $Delta m = 2/3, 5/3$. Thus, these data points are systematically deviant from the model and our fit and results may be improved if we remove them. 

Thus we repeat the fitting analysis using only $Delta m in {0, 0.5, 1, 1.5, 2}$: 
#multifig(
  tag_fn: none,
  cols: (1fr, 1fr, 0.5fr),
  image("media/2025-02-22-17-41-01.png"),
  image("media/2025-02-22-17-41-08.png"),
  [
    #align(horizon + center)[
      #rect(stroke: 0.3pt)[
    #table(
      columns: 2,
      align: (center, left),
      [$a$], [40.565],
      [$b$], [797.594],
      [$sigma_a$], [0.08703],
      [$sigma_b$], [5.193],
      [$chi^2/(n-1)$], [0.915]
    )<baldtable>
    ]]

  ],
  caption: [Linear fit of $B$ against $Delta m$, using only the data from $Delta m = n/2, n in NN$. Though $sigma_b$ is larger, we have reduced the systematic error, leading to a $chi^2/(n-1)$ < 1 and relatively independent residuals.]
)

This fit looks far better. Though the uncertainty in $b$ is higher, it is probably more representative of the true error of the experiment (because we have cut much of the systematic error). Our improved reduced chi-squared is also encouraging.

= Computation 

We'll calculate the the electron charge-to-mass ratio $abs(e)/m$ using @og-eqn:
$
  B = (2 pi c)/d m/abs(e) Delta m quad => quad abs(e)/m  = (2 pi c)/d (Delta m)/B = (2 pi c)/(d b)
$
where $b$ is the experimental $B / (Delta m)$ with uncertainty from the curve fits.

This experimental $b$ uncertainty includes the empirical noise (but not systematic error) uncertainty from the experimental process, including noise in the electromagnet power supply voltage, visual $Delta m$ readings, etalon alignment and optical focus, and hall probe placement. Any constant offset due in the calibration of the hall probe or electromagnet strength should be captured by the constant offset term in the curve fit, and thus sufficiently accounted for. 

A systematic drift in the hall probe would not be accounted for, so we must measure it separately. The magnetic field at the resting position of the hall probe was measured after zeroing before and after the experiment. The value (average of five samples) was 5.436 ± 0.010 mT before and 5.388 ± 0.024 after, for a drift of $8.768 times 10^(-3)$, which is within a noise standard deviation. Thus, the drift will not be significant in the following computation.

Having accounted for the drift, $abs(e)/m$ was calculated, with error propagation,#footnote[See error propagation at #link("https://github.com/Exr0nProjects/pyerr/blob/25wi-ph6/ph6_exp27.py").] from the values $d = 13.16 ± 0.0490$ mm, $b = 788.837 ± 1.642$ mT, resulting in 
$
  1.8145 times 10^(11) space (± 0.43%) space "C"slash"kg"
$

If we instead use $b = 797.594 ± 5.193$ mT from the second fit on pruned data, we get 
$
  1.79458 times 10^(11) space (±0.75%) space "C"slash"kg"
$
which is within $2.1%$ of the accepted value of $1.758820 times 10^(11)$ C/kg. The primary source of noise uncertainty was $b$ at ±0.67%, compared to the ±0.37% for $d$. However, the accepted value does not fall within a few noise standard deviations of our value, so there is still some systematic error not captured by the propagated uncertainty. 

