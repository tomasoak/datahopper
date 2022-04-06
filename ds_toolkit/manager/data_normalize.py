import unicodedata
from unidecode import unidecode
import pandas as pd


def normalize_column_string(
        df: pd.DataFrame, col: str, case=None, clean=False):
    """
    Adjust column value characters encoding to UTF-8.
    Case parameter makes your column string upper, lower or titlecase
    If clean:
        Removes special characters such as whitespace, ".", "-", "/", ",", '"'
    Example:
        df = pd.DataFrame(columns=["id", "name"],
                      data=[[1, "john coltRanE-"],
                            [2, "eLLa FiTzgeralD"],
                            [3, "MiLes DaviS"]])
        df = normalize_string(df, name, case="title", clean=True)

        `df = pd.DataFrame(columns=["id",  "name"],
                        data=[[1,   "John Coltrane"],
                              [2, "Ella Fitzgerald"],
                              [3, "Miles Davis"]])`
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
        raise ValueError(
            "The chosen case must be 'lower', 'upper' or 'title'.")

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


def clean_string(text: str):
    """ 
    Take a string and clean it!

    - Remove double-whitespace
    - Remove tab, newline, return, formfeed, etc.
    - Replace accented characters (e.g. ö becomes o)
    - Trim leading and trailing whitespace
    - Convert to upper-case
    """

    def keep(character):
        category = unicodedata.category(character)
        return (
            category[0] != "C"  # ignore control characters
            and category != "Zl"  # ignore line separator
            and category != "Zp"  # ignore paragraph separator
        )

    text = "".join(c for c in text if keep(c))
    text = " ".join(text.split())
    text = unidecode(text)
    return text


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
