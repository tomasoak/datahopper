import pandas as pd


def summary(data, groupby_col, numeric_col):
    """ Summarizes dataframe based on numeric column
    Gives the percentage of each attribute in which it will be groupped
    and cumulative percentage contribution of given attribute.

    Args:
      data: pd.DataFrame:
      groupby_col:
      numeric_col:

    Returns:
      summary: pd.Dataframe
    """

    df = data.groupby(groupby_col).agg({numeric_col: "sum"})\
        .sort_values(numeric_col, ascending=False)
    total = df[numeric_col].sum()
    cum_sum = df[numeric_col].cumsum()

    df_summary = pd.DataFrame(
        {"volume": df[numeric_col],
         "percentage": (100 * df[numeric_col] / total),
         "percentage_cumulative": (100 * cum_sum / total)})

    return df_summary[["volume", "percentage", "percentage_cumulative"]]\
        .reset_index()


def check(df: pd.DataFrame):
    """Check missing data in a given pandas Dataframe

    Args:
      df: pd.DataFrame:

    Returns:
      df: pd.Dataframe
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
