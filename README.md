

This code gives the effective areas of IceCube event selections at different declinations.

**WARNING: The generation of neutrino alerts is a process dominated by Poisson fluctuations. Great care must be taken to correctly interpret the values derived from effective areas, which only tell you the flux value at which one neutrino alert can be expected. However, the detection of a neutrino event from a given source does not at all imply that the source had an expectation of one neutrino. Only an upper limit on neutrino flux can be robustly derived using single high-energy neutrinos.**

For an excellent description of this problem, which is known as the Eddington Bias, please refer to ([Strotjohann et al., 2019](https://arxiv.org/abs/1809.06865)).

As a default, a combined effective area for all streams is used. *In almost all cases, this is the correct value to use.*
Unless you are sure that you would only perform a follow-up analysis of a given alert if it had a specific topology, such as starting track, then using the effective area of a sub-selection will give you a biased estimate of the neutrino flux. 

Using i3alerts

You can specify a selection to choose a given iteration of the realtime pipeline. Currently available selections are:

* **"alerts_v2"**: Selection in operation from June 2019 onwards ([Blaufuss et. al 2019](https://arxiv.org/abs/1908.04884)).
* **"alerts_v1"**: Original selection in place from 2016 to June 2019, consisting of two public selections EHE+HESE. This selection was in place for the detected coincidence of IC17092A and the flaring blazar TXS 0506+056, and was used in the corresponding archival alert analysis.
