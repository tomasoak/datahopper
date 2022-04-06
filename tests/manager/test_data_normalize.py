import pandas as pd
from ds_toolkit.manager.data_normalize import normalize_column_string


def test_normalize_column_string():
    df = pd.DataFrame(columns=["id", "name"],
                      data=[[1, "john coltRanE-"],
                            [2, "eLLa FiTzgeralD"],
                            [3, "MiLes DaviS"]])
    df_clean = pd.DataFrame(columns=["id", "name"],
                            data=[[1, "John Coltrane"],
                                  [2, "Ella Fitzgerald"],
                                  [3, "Miles Davis"]])

    df = normalize_column_string(df, "name", case="title", clean=True)

    assert all(df["name"] == df_clean["name"])
