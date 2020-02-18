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

def base_aeff(declination_deg, energy_pdf, selection="alerts_v2", purity="bronze"):

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

def get_aeff(declination_deg, energy_pdf, selection="alerts_v2", purity="bronze"):

    a_eff = base_aeff(declination_deg, energy_pdf, selection, purity)

    logging.info(f"Flux-averaged effective area is {a_eff:.2g} for each particle emitted between "
                 f"{energy_pdf.e_min:.2g} GeV and {energy_pdf.e_max:.2g} GeV ")

    return a_eff

def get_threshold_flux(declination_deg, energy_pdf, selection="alerts_v2", purity="bronze", norm_energy=10*u.GeV):

    try:
        norm_energy.to("GeV")
    except u.core.UnitConversionError as err:
        raise u.core.UnitConversionError(f"Use a unit of energy for your flux normalisation energy! "
                                         f"You provided {norm_energy} as a norm_energy") from err

    if not np.logical_and(
            norm_energy.to("GeV").value < energy_pdf.e_max,
            norm_energy.to("GeV").value > energy_pdf.e_min):
        raise ValueError(f"Normalisation energy of {norm_energy} lies outside the energy range of "
                         f"{energy_pdf.e_min:.2g} GeV - {energy_pdf.e_max:.2g} GeV "
                         f"for which you have defined your energy PDF.")

    a_eff = get_aeff(declination_deg, energy_pdf, selection, purity)

    flux_threshold_int = 1./a_eff

    flux_threshold_norm = flux_threshold_int * (energy_pdf.f((norm_energy/u.GeV).to("")))

    logging.info(f"For this spectrum, we requires a flux of {flux_threshold_norm.to('GeV^-1 cm^-2'):.2g} "
                 f"at {norm_energy:.2g}")
    get_e2dnde(flux_threshold_norm, norm_energy)

    return flux_threshold_norm


def power_law_threshold_flux(declination_deg, spectral_index=2.0, e_min_gev=10.**2., e_max_gev=10.**7.,
                             selection="alerts_v2", purity="bronze", norm_energy=10*u.GeV):

    e_pdf_dict = {
        "energy_pdf_name": "power_law",
        "gamma": spectral_index,
        "e_min_gev": e_min_gev,
        "e_max_gev": e_max_gev
    }

    logging.info(f"Assuming a power law with index {spectral_index:.2f} "
                 f"between {e_min_gev:.2g} GeV and {e_max_gev:.2g} GeV.")

    epdf = EnergyPDF.create(e_pdf_dict)



    return get_threshold_flux(declination_deg, epdf, selection=selection, purity=purity, norm_energy=norm_energy)

def get_e2dnde(flux_norm, norm_energy):

    e2dnde = flux_norm * norm_energy**2.

    if (flux_norm/(1./u.GeV /u.cm**2)).decompose().unit == "":
        e2dnde = e2dnde.to("erg cm^-2")
    else:
        e2dnde = e2dnde.to("erg cm^-2 s^-1")

    logging.info(f"This corresponds to E^2dN/dE = {e2dnde:.2g} "
                 f"at {norm_energy:.2g}")

    return e2dnde

def get_nexp(flux_norm, declination_deg, energy_pdf, selection="alerts_v2", norm_energy=10*u.GeV):

    flux_threshold = get_threshold_flux(
        declination_deg,
        energy_pdf=energy_pdf,
        norm_energy=norm_energy,
        selection=selection
    )

    n_exp = (flux_norm/flux_threshold).to(" ")

    logging.info(f"Given a flux of {flux_norm:.2g} at {norm_energy:.2g}, we have an expectation of {n_exp:.2g}")

    return n_exp