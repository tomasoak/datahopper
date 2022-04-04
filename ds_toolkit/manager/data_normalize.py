import pandas as pd


def normalize_string(df: pd.DataFrame, col: str, case=None, clean=False):
    """Adjust column value characters encoding to UTF-8.
    Case parameter makes your column string upper, lower or titlecase
    If clean:
        Removes special characters such as whitespace, ".", "-", "/", ",", '"'

    Example:
        df = pd.DataFrame(
            columns=["id",  "name"],
            data=[  [  1,   "john coltRanE-"],
                    [  2,   "eLLa _FiTzgeralD"],
                    [  3,   "MiLes DaviS"]])
        df = normalize_string(df, name, case="title", clean=True)
        `df = pd.DataFrame(
            columns=["id",  "name"],
            data=[  [  1,   "John Coltrane"],
            [  2,   "Ella Fitzgerald"],
            [  3,   "Miles Davis"]])`

    Args:
      df: pd.DataFrame:
      col: str:
      case: (Default value = None)
      clean: (Default value = False)

    Returns:
      df = pd.DataFrame: cleaned string column values

    """
    df[col] = (
        df[col]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )
    if case is None:
        df[col] = df[col]
    elif case == "lower":
        df[col] = df[col].str.lower()
    elif case == "upper":
        df[col] = df[col].str.upper()
    elif case == "title":
        df[col] = df[col].str.title()
    else:
        raise ValueError("The chosen case must be 'lower', 'upper' or 'title'.")

    if clean is True:
        df[col] = (
            df[col]
            .str.replace(".", "")
            .str.replace("-", "")
            .str.replace("/", "")
            .str.replace(",", "")
            .str.replace('"', "")
        )
    else:
        df[col] = df[col]

    return df


def rename(df: pd.DataFrame, columns):
    """Rename columns

    Args:
      df: pandas.DataFrame:
      columns:

    Returns:
      df: pd.Dataframe: withe renamed columns
    """
    return df.rename(columns=columns, errors="raise")


def drop_rows_missing_values(df: pd.DataFrame, *columns):
    """Drop rows with missing values

    Args:
      data: pandas.DataFrame:
      *columns:

    Returns:
      data: pd.DataFrame: A .copy() of the input DataFrame

    """
    for column in columns:
        df = df[~df[column].isin(["", "NA", "nan"])]
    return df.copy()
