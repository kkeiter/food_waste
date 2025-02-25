import os
import pandas as pd
from pyprojroot import has_dir, find_root

DATA_PATH = os.path.join(find_root(has_dir(".git")), "data")


def read_collections_data(dedup=True):
    # read in collection data
    coll_wk = pd.read_csv(os.path.join(DATA_PATH, "food-waste-pilot.csv"))

    # clean up column names and convert date
    coll_wk = clean_column_names(coll_wk)
    coll_wk["collection_date"] = pd.to_datetime(coll_wk["collection_date"])

    if dedup:
        # remove duplicate row for this particular location/date (discovered in EDA)
        coll_wk = coll_wk[
            ~(
                (coll_wk["stop_name"] == "Citizen's Convenience Center")
                & (coll_wk["collection_date"] == pd.to_datetime("2024-11-01"))
                & (coll_wk["estimated_earned_compost_created"] == 48)
            )
        ]

    return coll_wk


def clean_column_names(df):
    """
    Converts column names to lowercase and replaces spaces with underscores.

    Args:
      df: Pandas DataFrame.

    Returns:
      Pandas DataFrame with cleaned column names.
    """
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
    return df
