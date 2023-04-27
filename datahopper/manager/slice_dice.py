import pandas as pd


def rows_to_column(df: pd.DataFrame) -> pd.DataFrame:
    """ Melt table by combining two columns and bringing them into columns.

    Args:
      data: pd.DataFrame
      groupby_col: string
      numeric_col: string

    Example:
        From this:
        YEAR	DEPARTMENT	MUNICIPALITY	  GEOCODE	  INDICATOR	    VALUE
        2020	SANTA CRUZ	LAGUNILLAS	      070701	   PRODUCTION	1152.00
        2021	SANTA CRUZ	FERNANDEZ ALONSO  071004	   PRODUCTION	2.63

        To this:
        GEOCODE	   MUNICIPALITY	 DEPARTMENT	 PRODUCTION_2020	PRODUCTION_2021
        010401	PADILLA	     CHUQUISACA	       34.0	            35.0	
        010405	EL VILLAR	 CHUQUISACA	       15.0	            16.0
    
    Returns:
      df: pd.Dataframe
    """

    df_prod = pd.melt(
        df,
        id_vars=["GEOCODE", "MUNICIPALITY", "DEPARTMENT", "YEAR"],
        value_vars=["PRODUCTION"],
    )
    df_prod["VAR"] = df_prod["variable"] + "_" + df_prod["YEAR"]
    df_prod = df_prod[["GEOCODE", "MUNICIPALITY", "DEPARTMENT", "VAR", "value"]]
    df_prod = df_prod.astype({"value": "float"})

    df_prod = df_prod.pivot_table(
        values=["value"],
        index=["GEOCODE", "MUNICIPALITY", "DEPARTMENT"],
        columns=["VAR"],
    )

    df_prod.columns = [
        "PRODUCTION_2018",
        "PRODUCTION_2019",
        "PRODUCTION_2020",
        "PRODUCTION_2021",
    ]
    df_prod = df_prod.reset_index()
