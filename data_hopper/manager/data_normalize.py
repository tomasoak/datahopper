import unicodedata
from unidecode import unidecode
import pandas as pd


def clean_string(text: str, especial_char=False):
    """
    Take a string and clean it

    - Remove double-whitespace
    - Remove tab, newline, return, formfeed, etc.
    - Replace accented characters (e.g. ö becomes o)
    - Trim leading and trailing whitespace
    - If clean:
        Removes especial characters such as `.`  `-`  `/`  `,`  `"`

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

    if especial_char is True:
        text = (
            text.replace(".", "")
            .replace("-", "")
            .replace("/", "")
            .replace(",", "")
            .replace('"', "")
            .replace('*', "")
        )

    return text


def rename_column(df: pd.DataFrame, columns):
    """Rename columns

    Args:
      df: pandas.DataFrame:
      columns:

    Returns:
      df: pd.Dataframe: withe renamed columns
    """
    return df.rename(columns=columns, errors="raise")


def drop_rows_missing_values(df: pd.DataFrame, columns):
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
