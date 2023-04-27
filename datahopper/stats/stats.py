import pandas as pd

class Regression:
    def __init__(self, df):
        self.df = df

    def quantile_normalization(self, col_one, col_two):
        """Implements a quantile normalization
        https://en.wikipedia.org/wiki/Quantile_normalization """
        import numpy as np
        import pandas as pd

        df = self.df.copy()
        df = df[[col_one, col_two]]

        # compute mean rank
        dic = {}
        for col in df:
            dic.update({col: sorted(df[col])})
        sorted_df = pd.DataFrame(dic)
        rank = sorted_df.mean(axis=1).tolist()

        # sort
        for col in df:
            t = np.searchsorted(np.sort(df[col]), df[col])
            df[col] = [rank[i] for i in t]

        return df

    def plot_regression(self, col_one, col_two, title, label_xaxis, label_yaxis):
        import plotly.express as px
        
        both = Regression.quantile_normalization(self, col_one, col_two)

        fig = px.scatter(
            y=both[col_one],
            x=both[col_two],
            trendline="ols",
            title=title,
            labels={"y": label_yaxis, "x": label_xaxis},
            height=540,
            width=800,
        )

        fig.update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
        )

        return fig.show()
    

def mun_diff_capacity(df: pd.DataFrame, vol: str) -> pd.DataFrame:
    """Checks whether the previous values is equal to the current year,
    if so `CAP_DIFF` is False otherwise, True"""
    import numpy as np
    
    df = df.sort_values(["TRASE_ID", "YEAR"])

    previous_value = df[vol].shift(1)

    unique_trase_id = sorted(df["TRASE_ID"].unique())
    unique_years = sorted(df["YEAR"].unique())

    first_year = unique_years[0]
    not_first_year = df["YEAR"] != first_year

    bigger_previous = df[vol] > previous_value
    equal_previous = df[vol] == previous_value
    lower_previous = df[vol] < previous_value

    for i, j in zip(unique_trase_id, unique_years):
        df.loc[df["YEAR"] == first_year, "AREA_TREND"] = np.NaN
        df.loc[not_first_year & bigger_previous, "AREA_TREND"] = "Increased"
        df.loc[not_first_year & bigger_previous, "AREA_DIFF"] = df[vol] - previous_value
        df.loc[equal_previous, "AREA_TREND"] = "Equal"
        df.loc[not_first_year & lower_previous, "AREA_TREND"] = "Decreased"
        df.loc[not_first_year & lower_previous, "AREA_DIFF"] = df[vol] - previous_value

    return df    