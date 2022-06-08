# EP-PINNs
Repository holding the code and data for the project: Characterisation of the electrical properties of the human atrium using Physics-Inspired Neural Networks (PINNs)

![alt text](https://github.com/ariehlev/EP-PINNs/blob/main/Results/PINN%20diagram/PINNs%20diagram.png?raw=true)

<p align="center">
    <b><style="font-size:20px">EP-PINN diagram</b>
</p>

## Abstract

Cardiac arrhythmia, particularly atrial fibrillation (AF), does not yet have successful treatments despite being one of the most common diseases globally. It is anticipated that the ability to correctly estimate fundamental electrophysiological (EP) cardiac properties will improve the treatment and diagnosis of arrhythmias like AF by allowing the personalisation of treatment. However, this is not an easy task.

This study proposes Physics-Inspired Neural Networks (PINNs), a novel method for addressing nonlinear problems from limited data, to tackle this issue. The aims are to reproduce action potentials (AP) and estimate relevant EP parameters from the EP cardiac model presented by Fenton et al. [1]. This work shows the EP-PINNs’ ability to accurately recreate the AP propagation while estimating EP parameters relevant to AP duration from synthetically generated data with varying amounts of noise. Finally, the EP-PINNs performance is also tested on animal in-vitro preparations by describing the influence in AP duration of anti-arrhythmic drugs (AADs): Nifedipine and E-4031. The results for the synthetic data are excellent, with a mean RMSE of 0.0084 in AP recreation and a 27% mean relative error in EP parameter estimation. For the experimental data, statistically meaningful differences were found in the model parameters between the baseline and the experimental measurements.

This project is a steppingstone to encouraging further research on the applications of PINNs to the diagnosis and treatment of cardiac diseases, especially AF.

[1] F. Fenton and A. Karma, “Vortex dynamics in three-dimensional continuous myocardium with fiber rotation: Filament instability and fibrillation a…,” 1998. [Online]. Available: http://ojps.aip.org/chaos/chocr.jsp




