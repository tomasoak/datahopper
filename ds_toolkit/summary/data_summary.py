import pandas as pd

def check(data: pd.DataFrame):
  total_missing = data.isnull().sum().sum()
  missing_percentage = data.isnul().sum().sum() * 100 / data.shape[0]
  unique = data.nunique()
  not_null = data.notnull().sum()
  df = pd.DataFrame({"unique_values": unique,
                    "value_exist": not_null,
                    "total_missing": total_missing,
                    "missing_percentage": missing_percentage})
  print("Total Data Missing:", total_missing)
  return df