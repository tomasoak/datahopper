import unicodedata
from unidecode import unidecode
import pandas as pd


# TODO: UFT-8 string?
def normalize_column_string_encoding(
        df: pd.DataFrame, col: str):
    """
    Adjust column value characters encoding to UTF-8.

    Example:
        # TODO: Add an example that changes encoding!

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

    Returns:
      df = pd.DataFrame: utf-8 encoded column string
    """
    df[col] = (
        df[col]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    return df


def case_string(text: str, case=None):
    """
    Case string into upper, lower or title format

    Args:
     text: str
     case: (Default value None)

    Return:
    text: str

    """
    if case == "upper":
        text.upper()
    elif case == "lower":
        text.lower()
    elif case == "title":
        text.title()
    else:
        raise ValueError(
            "The chosen case must be 'lower', 'upper' or 'title'.")

    return text


def clean_string(text: str, special_char=False):
    """
    Take a string and clean it

    - Remove double-whitespace
    - Remove tab, newline, return, formfeed, etc.
    - Replace accented characters (e.g. ö becomes o)
    - Trim leading and trailing whitespace
    - If clean:
        Removes special characters such as whitespace, ".", "-", "/", ",", '"'

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

    if special_char is True:
        text = (
            text.replace(".", "")
            .replace("-", "")
            .replace("/", "")
            .replace(",", "")
            .replace('"', "")
        )

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
