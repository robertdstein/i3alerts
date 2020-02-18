import logging
import numpy as np
import os
from pathlib import Path
import pandas as pd

base_dir = Path(__file__).parent.absolute()

def load_v1_aeff(declination):

    try:
        declination = float(declination)
    except ValueError as e:
        raise ValueError(f"Cannot convert declination '{declination}' to float") from e

    if declination < -5.:
        dec_dir = "dec_minus_90_minus_5"
        raise NotImplementedError("Effective Area File has not yet been added.")
    elif declination > 30.:
        dec_dir = "dec_30_90"
        raise NotImplementedError("Effective Area File has not yet been added.")
    else:
        dec_dir = "dec_minus_5_30"

    full_dir = os.path.join(base_dir, dec_dir)
    logging.debug(f"Loading effective areas from {full_dir}")

    aeffs = []

    for stream in ["ehe"]:
        filename = f"{full_dir}/Aeff_{stream}.csv"
        aeff = pd.read_csv(filename, names=["E_TeV", "A_eff"])
        aeffs.append(aeff)

    return aeffs