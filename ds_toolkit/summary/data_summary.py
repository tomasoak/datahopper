import pandas as pd


def summary(df: pandas.DataFrame, groupby_col, numeric_col) -> pandas.DataFrame:
    """Check missing data in a given pandas Dataframe
    
    Args:
      df: pd.DataFrame: 
      groupby_col: 
      numeric_col:

    Returns:
      summary: pd.Dataframe
    """

  df = df.groupby(groupby_col).agg({numeric_col: "sum"}).sort_values(numeric_col, ascending=False)
    
  total = df[numeric_col].sum()
  cum_sum = df[numeric_col].cumsum()

  summary = pd.DataFrame({"volume": df[numeric_col],
                                    "percentage": (100 * df[numeric_col] / total).round(1), 
                                    "percentage_cumulative": (100 * cum_sum / total).round(1)})
    
  return summary[["volume", "percentage", "percentage_cumulative"]].reset_index()


def check(data: pd.DataFrame):
    """Check missing data in a given pandas Dataframe
    
    Args:
      data: pd.DataFrame: 

    Returns:
      df: pd.Dataframe
    """
  total_missing = data.isnull().sum().sum()
  missing_percentage = data.isnul().sum().sum() * 100 / data.shape[0]
  unique = data.nunique()
  not_null = data.notnull().sum()
  df = pd.DataFrame({"unique_values": unique,
                    "value_exist": not_null,
                    "total_missing": total_missing,
                    "missing_percentage": missing_percentage})
  print("Total Data Missing:", total_missing)
  print("Percentual Data Missing:", missing_percentage)
  return df