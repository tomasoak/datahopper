import pandas as pd


def summary(data, groupby_col, numeric_col):
    """ Summarizes dataframe based on numeric column
    Gives the percentage of each attribute in which it will be groupped
    and cumulative percentage contribution of given attribute.

    Args:
      data: pd.DataFrame:
      groupby_col: string
      numeric_col: string

    Example:
      summary(data, "COUNTRY", "VOLUME")

       COUNTRY         volume	       vol_pct	 vol_cpct
        SOUTH AFRICA  5.634480e+08	  5.22	   5.22
        ARGENTINA		  1.439596e+07	  0.13	   5.35
        BRAZIL	      4.991230e+09	  46.20	   51.55
        INDONESIA		  8.071003e+08	  7.47	   59.02

    Returns:
      df_summary: pd.Dataframe
    """

    df = (data.groupby(groupby_col)
              .agg({numeric_col: "sum"})
              .sort_values(numeric_col, ascending=False))
    total = df[numeric_col].sum()
    cum_sum = df[numeric_col].cumsum()

    df_summary = pd.DataFrame(
        {"volume": df[numeric_col],
         "percentage": (100 * df[numeric_col] / total),
         "percentage_cumulative": (100 * cum_sum / total)})

    return (df_summary[["volume", "percentage", "percentage_cumulative"]]
            .reset_index())


def check(df: pd.DataFrame):
    """Check missing data in a given pandas Dataframe

    Args:
      df: pd.DataFrame:

    Returns:
      df_check: pd.Dataframe
    """

    total_missing = df.isnull().sum().sum()
    missing_percentage = df.isnul().sum().sum() * 100 / df.shape[0]
    unique = df.nunique()
    not_null = df.notnull().sum()
    df_check = pd.DataFrame({"unique_values": unique,
                             "value_exist": not_null,
                             "total_missing": total_missing,
                             "missing_percentage": missing_percentage})
    print("Total Data Missing:", total_missing)
    print("Percentual Data Missing:", missing_percentage)

    return df_check


def row_difference(df: pd.DataFrame, vol: str):
    """Checks whether the previous values is equal to the current year,
    if so `CAP_DIFF` is False otherwise, True"""
    import numpy as np
    
    df = df.sort_values(["TRASE_ID", "YEAR"])

    previous_value = df[vol].shift(1)
    
    unique_trase_id = sorted(df["TRASE_ID"].unique())
    unique_years = sorted(df["YEAR"].unique())
    
    first_year = unique_years[0]
    not_first_year = df["YEAR"] != first_year
    
    bigger_previous = df[vol] > previous_value
    equal_previous = df[vol] == previous_value
    lower_previous = df[vol] < previous_value
    
    for i, j in zip(unique_trase_id, unique_years):
        df.loc[df["YEAR"] == first_year, "AREA_TREND"] = np.NaN
        df.loc[(not_first_year) & (bigger_previous), "AREA_TREND"] = "Increased"
        df.loc[(not_first_year) & (bigger_previous), "AREA_DIFF"] = df[vol] - previous_value
        df.loc[equal_previous, "AREA_TREND"] = "Equal"
        df.loc[(not_first_year) & (lower_previous), "AREA_TREND"] = "Decreased"
        df.loc[(not_first_year) & (lower_previous), "AREA_DIFF"] = df[vol] - previous_value
    
    return df