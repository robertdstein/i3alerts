import pandas as pd
import numpy as np
from flarestack.data.public import icecube_ps_3_year

ps = icecube_ps_3_year.get_single_season("IC86-2012")

def load_ic86_aeff(declination_deg):
    eff_a_f = ps.load_effective_area()

    vals = eff_a_f(ps.log_e_bins, np.sin(np.radians(declination_deg)))

    e_vals_tev = 10.**ps.log_e_bins *10. ** -3

    aeff = pd.DataFrame(zip(e_vals_tev, vals), columns=["E_TeV", "A_eff"])

    return [aeff]


