import logging
import unittest
from astropy import units as u
from i3alerts.effective_area import get_nexp, get_e2dnde, get_aeff, get_threshold_flux, divide_time, EnergyPDF

logger = logging.getLogger()
logger.setLevel("ERROR")

class TestTimeIntegrated(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_aeff(self):

        epdf = EnergyPDF.create({
            "energy_pdf_name": "power_law",
            "gamma": 2.0,
            "e_min_gev": 2 * 10. ** 5,
            "e_max_gev": 10. ** 7
        })

        decs = [-45., 0., 45.]

        for selection in ["alerts_v1", "alerts_v2"]:
            for dec in decs:
                try:
                    get_aeff(declination_deg=dec, energy_pdf=epdf, selection=selection)
                except NotImplementedError:
                    logging.warning(f"Skipping selection {selection} at dec {dec} deg,"
                                    f"as this has not yet been implemented")
                    pass

        # res = power_law_aeff(declination_deg=10.)
        #
        # divide_time(res, 0.5 * u.year)
        #
        # norm_energy = 1. * u.PeV
        #
        # txs_value_100tev = 2. * 0.5 * u.year * 1.6e-15 / u.TeV / u.cm ** 2 / u.s
        # txs_value_at_norm = (txs_value_100tev * (norm_energy / (100 * u.TeV)) ** -2.).to("GeV^-1 cm^-2")
        #
        # # get_threshold_flux(declination_deg=10., energy_pdf=epdf, norm_energy=norm_energy)
        #
        # get_nexp(txs_value_at_norm, declination_deg=10., energy_pdf=epdf, norm_energy=norm_energy,
        #          selection="alerts_v1")
        #
        # get_e2dnde(txs_value_100tev / (0.5 * u.year), 100 * u.TeV)


if __name__ == '__main__':
    unittest.main()