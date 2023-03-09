import pandas as pd


def two_rows_to_column(df: pd.DataFrame) -> pd.DataFrame:
    df_area = pd.melt(
        df,
        id_vars=["TRASE_ID", "MUNICIPALITY", "DEPARTMENT", "YEAR"],
        value_vars=["AREA"],
    )
    df_area["VAR"] = df_area["variable"] + "_" + df_area["YEAR"]
    df_area = df_area[["TRASE_ID", "MUNICIPALITY", "DEPARTMENT", "VAR", "value"]]
    df_area = df_area.astype({"value": "float"})

    df_area = df_area.pivot_table(
        values=["value"],
        index=["TRASE_ID", "MUNICIPALITY", "DEPARTMENT"],
        columns=["VAR"],
    )

    df_area.columns = [
        "AREA_2013",
        "AREA_2014",
        "AREA_2015",
        "AREA_2016",
        "AREA_2017",
        "AREA_2018",
        "AREA_2019",
        "AREA_2020",
        "AREA_2021",
    ]
    df_area = df_area.reset_index()

    df_area = mun.merge(
        df_area, how="left", on=["TRASE_ID", "MUNICIPALITY", "DEPARTMENT"]
    )
    df_area = df_area.fillna(0)