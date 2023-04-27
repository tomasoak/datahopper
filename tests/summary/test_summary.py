import pandas as pd
from datahopper.summary.summary import (
    row_difference
    )


def test_row_difference():
    df = pd.DataFrame(
        columns=["id", "country_id", "country", "year", "gpd"],
        data=[
            [1, "01", "India", 2010, 100],
            [2, "01", "India", 2015, 100],
            [3, "01", "India", 2020, 1000],
            [4, "02", "Brazil", 2010, 200],
            [5, "02", "Brazil", 2015, 201],
            [6, "02", "Brazil", 2020, 2001],
            [7, "03", "South Africa", 2010, 1000],
            [8, "03", "South Africa", 2015, 1001],
            [9, "03", "South Africa", 2020, 1002],
        ]
    )

    df_row_difference = row_difference(df, "country_id", "year", "gpd")

    assert all(df_row_difference[(df_row_difference["country"] == "India")
                             & (df_row_difference["year"] == 2015)]["trend"] == "Equal")

    assert all(df_row_difference[(df_row_difference["country"] == "Brazil")
                             & (df_row_difference["year"] == 2015)]["difference"] == 1)
