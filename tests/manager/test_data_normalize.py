import pandas as pd
from datahopper.manager.data_normalize import (
    clean_string,
    rename_column,
    drop_rows_missing_values
)


def test_clean_string():
    string = "Älvkarleovägen"
    string_cleaned = "Alvkarleovagen"

    string_special = "Zimbäb*we"
    string_special_cleaned = "Zimbabwe"

    assert clean_string(string) == string_cleaned
    assert clean_string(
        string_special, especial_char=True) == string_special_cleaned


def test_rename_column():
    column_names = ["id", "municipality", "country", "continent"]

    df = pd.DataFrame(
        columns=["ID", "MUNCIPAL", "COUNTRI", "CONSTINENNT"])

    aimed_column_names = dict(zip(df.columns, column_names))

    df_renamed = pd.DataFrame(
        columns=["id", "municipality", "country", "continent"])

    assert all(rename_column(df, aimed_column_names) == df_renamed)


def test_drop_rows_missing_values():
    df = pd.DataFrame(columns=["id", "name", "age", "gender"],
                      data=[[1, "Alex", 32, "Non-Binary"],
                            [2, "", 28, "Male"],
                            [3, "Austin", 57, "Male"],
                            [4, "Palema", "NA", "NA"]])

    df_cleaned = pd.DataFrame(columns=["id", "name", "age", "gender"],
                              data=[[1, "Alex", 32, "Non-Binary"],
                                    [3, "Austin", 57, "Male"]])

    assert all(drop_rows_missing_values(
        df, df.columns).sort_index(inplace=True) == df_cleaned)
