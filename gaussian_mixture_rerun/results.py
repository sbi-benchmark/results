from pathlib import Path

import pandas as pd  # noqa
from omegaconf import OmegaConf

from utils import apply_df, clean, compile_df, get_df

basepath_runs = Path(__file__).parent.absolute() / "runs/rq"
basepath = Path(__file__).parent.absolute() / "results"


def gaussian_mixture_rerun(row):
    """Gaussian Mixture rerun"""
    if row["algorithm"] == "REJ-ABC 100 KDE":
        row["algorithm"] = "REJ-ABC"

    if row["algorithm"] == "SMC-ABC (ours) .5 .2 KDE" and (
        row["num_simulations"] == "10³" or row["num_simulations"] == "10⁴"
    ):
        row["algorithm"] = "SMC-ABC"
    if (
        row["algorithm"] == "SMC-ABC (ours) .5 .2 KDE"
        and row["num_simulations"] == "10⁵"
    ):
        row["algorithm"] = "SMC-ABC"

    if row["algorithm"] == "NLE-MAF":
        row["algorithm"] = "NLE"

    if row["algorithm"] == "NPE-NSF":
        row["algorithm"] = "NPE"

    if row["algorithm"] == "NRE-RES":
        row["algorithm"] = "NRE"

    if row["algorithm"] == "SNLE-MAF":
        row["algorithm"] = "SNLE"

    if row["algorithm"] == "SNPE-NSF":
        row["algorithm"] = "SNPE"

    if row["algorithm"] == "SNRE-RES":
        row["algorithm"] = "SNRE"

    if row["algorithm"] not in [
        "REJ-ABC",
        "SMC-ABC",
        "NLE",
        "NPE",
        "NRE",
        "SNLE",
        "SNPE",
        "SNRE",
    ]:
        print(row["algorithm"])
        return None

    return row


if __name__ == "__main__":
    df = compile_df(basepath=f"{basepath_runs}")
    df.to_csv(f"{basepath}/df_raw.csv", index=False)
    print(len(df))
    df = apply_df(df=df, row_fn=clean)
    df.to_csv(f"{basepath}/df.csv", index=False)
    print(len(df))

    print(gaussian_mixture_rerun.__doc__)
    df = apply_df(
        df=get_df(path=f"{basepath}/df.csv"), row_fn=gaussian_mixture_rerun)
    df.to_csv(f"{basepath}/gaussian_mixture_rerun.csv", index=False)
    assert len(df) == 240
