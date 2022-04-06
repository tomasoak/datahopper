import unicodedata
from unidecode import unidecode
import pandas as pd


def normalize_string(text: str, case=None, clean=False):
    """Normalize string characters encoding to UTF-8.

    - Remove double-whitespace
    - Remove tab, newline, return, formfeed, etc.
    - Replace accented characters (e.g. ö becomes o)
    - Trim leading and trailing whitespace

    Case parameter makes your column string upper, lower or titlecase
    If clean:
        Removes special characters such as whitespace, ".", "-", "/", ",", '"'

    Example:
        df = pd.DataFrame(
            columns=["id",  "name"],
            data=[  [  1,   "john coltRanE-"],
                    [  2,   "eLLa _FiTzgeralD"],
                    [  3,   "MiLes DaviS"]])
        df = df["name"].apply(normalize_string, case="title", clean=True)
        `df = pd.DataFrame(
            columns=["id",  "name"],
            data=[  [  1,   "John Coltrane"],
            [  2,   "Ella Fitzgerald"],
            [  3,   "Miles Davis"]])`

    Args:
      text: string
      case: (Default value = None)
      clean: (Default value = False)

    Returns:
      text = string: cleaned string
    """

    text = (
        text
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

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

    if clean:
        text = (
            text.replace(".", "")
            .replace("-", "")
            .replace("/", "")
            .replace(",", "")
            .replace('"', "")
        )

    if case == "lower":
        text.lower()
    elif case == "upper":
        text.upper()
    elif case == "title":
        text.title()
    else:
        raise ValueError(
            "The chosen case must be 'lower', 'upper' or 'title'."
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
