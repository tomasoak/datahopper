import pandas as pd
import numpy as np


def summary(data: pd.DataFrame, groupby_col: str, numeric_col: str):
    """ Summarizes dataframe based on numeric column
    Gives the percentage of each attribute in which it will be groupped
    and cumulative percentage contribution of given attribute.

    Args:
      data: pd.DataFrame
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
      df: pd.DataFrame

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

    return df_check


def row_difference(df: pd.DataFrame, id_col: str, temporal_col: str, num_col: str):
    """Checks whether the previous values is equal to the current year,
    if so `difference` is False otherwise, True

    Args:
      df: pd.DataFrame
      id_col: Column with the unique identifier code
      temporal_col: Column with the timestamp, might be year, month, day
      num_col: Numerical column with the value aimed to be look at

    Returns:
      df: pd.Dataframe
    """

    df = df.sort_values([id_col, temporal_col])

    previous_value = df[num_col].shift(1)

    unique_id = sorted(df[id_col].unique())
    unique_time = sorted(df[temporal_col].unique())

    first_year = unique_time[0]
    not_first_year = df[temporal_col] != first_year

    bigger_previous = df[num_col] > previous_value
    equal_previous = df[num_col] == previous_value
    lower_previous = df[num_col] < previous_value

    for i, j in zip(unique_id, unique_time):
        df.loc[df[temporal_col] == first_year, "trend"] = np.NaN
        df.loc[(not_first_year) & (bigger_previous), "trend"] = "Increased"
        df.loc[(not_first_year) & (bigger_previous), "difference"] = df[num_col] - previous_value
        df.loc[equal_previous, "trend"] = "Equal"
        df.loc[(not_first_year) & (lower_previous), "trend"] = "Decreased"
        df.loc[(not_first_year) & (lower_previous), "difference"] = df[num_col] - previous_value

    return df
