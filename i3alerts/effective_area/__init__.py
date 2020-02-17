import logging
import numpy as np
from astropy import units as u
from flarestack.core.energy_pdf import EnergyPDF
from i3alerts.effective_area.alerts_v1 import load_v1_aeff
from i3alerts.effective_area.alerts_v2 import load_v2_aeff

def load_aeff(declination_deg, selection, purity):

    if selection == "alerts_v2":
        aeffs = load_v2_aeff(declination_deg)
    elif selection == "alerts_v1":
        aeffs = load_v1_aeff(declination_deg)
    else:
        raise ValueError(f"Selection '{selection}' not recognised. \n"
                         f"The following elections are available: alerts_v1, alerts_v2")

    return aeffs

def integrate_aeff(aeff_df, energy_pdf):
    n_iter = int(len(aeff_df["E_TeV"]) / int(2))

    a_eff = 0.

    for i in range(n_iter):
        lower = 2 * i
        upper = 2 * i + 1
        e_min = aeff_df["E_TeV"][lower] * 10 ** 3
        e_max = aeff_df["E_TeV"][upper] * 10 ** 3

        if np.logical_and(e_min > energy_pdf.e_min, e_min < energy_pdf.e_max):
            int_factor = energy_pdf.flux_integral(e_min, e_max) * u.GeV
            aeff = np.mean([aeff_df["A_eff"][lower], aeff_df["A_eff"][upper]]) * u.m ** 2
            a_eff += int_factor * aeff

    return a_eff

def get_aeff(declination_deg, energy_pdf, selection="alerts_v2", purity="bronze"):

    logging.info(f"You have selected a source at a declination of {declination_deg:.2g} deg, "
                 f"with the {selection} selection and purity {purity}.")

    aeffs = load_aeff(declination_deg, selection, purity)
    
    a_eff = 0.

    for aeff_df in aeffs:
        a_eff += integrate_aeff(aeff_df, energy_pdf)
        
    return a_eff

def divide_time(flux, time_period):

    if not isinstance(time_period, u.Quantity):
        raise ValueError("Variable 'time_period' does have an associated astropy unit. "
                         "Please use astropy.units to specify the unit of the time-period.")

    try:
        time_period = time_period.to("s")
    except u.core.UnitConversionError as err:
        raise u.core.UnitConversionError(f"Use a unit of time for your time period! "
                                         f"You provided {time_period} as a time_period") from err

    div_flux = flux/time_period

    logging.info(f"Dividing by {time_period:.2g} ({time_period.to('year'):.2g}) gives: {div_flux:.2g}")

    return div_flux

def convert_aeff(declination_deg, energy_pdf,  selection="alerts_v2", purity="bronze"):
    a_eff = get_aeff(declination_deg, energy_pdf, selection, purity)
    norm_1gev = ((1. * u.GeV) ** 2. / a_eff).to("erg cm^-2")
    flux_norm = norm_1gev.to("GeV cm^-2") / (1. * u.GeV ** 2)
    logging.info(f"Requires a time-integrated flux normalisation of {norm_1gev:.2g} at 1GeV")
    return flux_norm

def power_law_aeff(declination_deg, spectral_index=2.0, e_min_gev=10.**2., e_max_gev=10.**7.):

    e_pdf_dict = {
        "energy_pdf_name": "power_law",
        "gamma": spectral_index,
        "e_min_gev": e_min_gev,
        "e_max_gev": e_max_gev
    }

    logging.info(f"Assuming a power law with index {spectral_index:.2f}"
                 f"between {e_min_gev:.2g} GeV and {e_max_gev:.2g}.")

    epdf = EnergyPDF.create(e_pdf_dict)

    return convert_aeff(declination_deg, epdf)

    
if __name__ == "__main__":

    logging.getLogger().setLevel("DEBUG")

    res = power_law_aeff(declination_deg=35.)

    divide_time(res, 0.5*u.year)

    # if subselection:
    #     logging.warning(f"Warning: You have specified the following subselection: {subselection}. "
    #                     f"Are you sure that you require only these alerts, rather than the full selection?"
    #                     )