import pandas as pd
import plotly.express as px


class Chart:
    def __init__(self, df, agg_col):
        self.df = df
        self.agg_col = agg_col
        
    def histogram(self, title: str, label: str, yaxis_title: str):
        fig = px.histogram(self.df[self.df[self.agg_col]>0], x=self.agg_col,
                           marginal="box",
                           title=f"{title}", labels={self.agg_col: label},
                           height=400, width=900)
        fig.update_layout(
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            yaxis_title = yaxis_title
        )
        
        return fig

    def bar_year(self, title: str, label: str):
        """Vertical bar chart"""
        df_year = self.df.groupby("YEAR", as_index=False).agg({self.agg_col: "sum"}).sort_values(self.agg_col, ascending=False)
        df_year['category'] = [str(i) for i in df_year.index]
        colors = ["rgb(189,189,189)"] * df_year["YEAR"].nunique()
        colors[0] = "rgb(255,106,95)"
        colors[1] = "rgb(120,120,120)"

        fig = px.bar(df_year, x="YEAR", y=self.agg_col, color='category', 
                     hover_name="YEAR", hover_data={"category": False, "YEAR":False},
                     labels={self.agg_col: label, "YEAR": ""},
                     color_discrete_sequence=colors, title=f"{title}",
                     height=500, width=800)
        fig.update_layout(
            showlegend=False,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            xaxis = dict(tickmode = 'linear', tick0 = 1),
        )

        return fig

    def bar_year_uf(self, title: str, label: str):
        """Vertical bar chart"""
        df_per_year_uf = self.df[self.df["YEAR"]>=2013].groupby(["YEAR", "SIGLA_UF"], as_index=False).agg({self.agg_col: "sum"})
        df_per_year_uf = df_per_year_uf.assign(UF_YEAR=lambda x: x["SIGLA_UF"] + " - " + x["YEAR"].astype(str))

        fig = px.bar(df_per_year_uf, x="YEAR", y=self.agg_col, color="SIGLA_UF", 
                     barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel,
                     hover_name="UF_YEAR", hover_data={"YEAR":False, "SIGLA_UF":False},
                     height=500, width=900, labels={"YEAR": "", self.agg_col: label, "SIGLA_UF": "State"})

        fig.update_layout(
                plot_bgcolor = 'rgba(0, 0, 0, 0)',
                paper_bgcolor = 'rgba(0, 0, 0, 0)',
                xaxis = dict(tickmode = 'linear', tick0 = 1)
            )

        return fig
    
    def bar_mun_year(self, title: str, label: str):
        """Horizontal bar chart"""
        apb_mun_sorted = self.df[self.df["YEAR"]>=2013].sort_values(self.agg_col, ascending=False).head(20)

        fig = px.bar(apb_mun_sorted, x=self.agg_col, y="MUN_UF", color="YEAR",
                     color_continuous_scale="Viridis", title=f"{title}", 
                    height=500, width=800, hover_name="MUN_UF", hover_data={"MUN_UF": False},
                     labels={self.agg_col: label, "MUN_UF": "Municipalities", "YEAR": "Year"})
        fig.update_layout(
                plot_bgcolor = 'rgba(0, 0, 0, 0)',
                paper_bgcolor = 'rgba(0, 0, 0, 0)'
        )
        return fig
    
    
    def bar_mun_uf_total(self, agg_method: str, title: str, label: str):
        df_mun_group = (self.df[self.df["YEAR"]>=2013]
                         .groupby(["TRASE_ID", "MUN_UF"], as_index=False)
                         .agg({self.agg_col: agg_method})
                         .sort_values(self.agg_col, ascending=False)
                         .head(20)
                    )
        
        df_mun_group['category'] = [str(i) for i in df_mun_group.index]
        colors = ["rgb(189,189,189)"] * df_mun_group["TRASE_ID"].nunique()
        colors[0] = "rgb(255,106,95)"
        colors[1] = "rgb(120,120,120)"

        fig = px.bar(df_mun_group, x=self.agg_col, y="MUN_UF", 
                    color='category', color_discrete_sequence=colors, title=f"{title}",
                     hover_name="MUN_UF", hover_data={'category':False, "MUN_UF": False},
                    height=600, width=800, 
                     labels={self.agg_col: label, "MUN_UF": "Municipalities"})
        fig.update_layout(
            showlegend=False,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            yaxis={'categoryorder':'total ascending'}
        )
        return fig
    
    def subplot_hist(self, title: str):
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        fig = make_subplots(rows=2, cols=4)
        
        df = self.df[self.df[self.agg_col]>0]

        trace0 = go.Histogram(x=df[df["YEAR"]==2020][self.agg_col], autobinx=True, name="2020", marker_color="rgb(255,106,95)")
        trace1 = go.Histogram(x=df[df["YEAR"]==2019][self.agg_col], autobinx=True, name="2019", marker_color="rgb(120,120,120)")
        trace2 = go.Histogram(x=df[df["YEAR"]==2018][self.agg_col], autobinx=True, name="2018", marker_color="rgb(189,189,189)")
        trace3 = go.Histogram(x=df[df["YEAR"]==2017][self.agg_col], autobinx=True, name="2017", marker_color="#EE7A68")
        trace4 = go.Histogram(x=df[df["YEAR"]==2016][self.agg_col], autobinx=True, name="2016", marker_color="#604693")
        trace5 = go.Histogram(x=df[df["YEAR"]==2015][self.agg_col], autobinx=True, name="2015", marker_color="rgb(189,189,189)")
        trace6 = go.Histogram(x=df[df["YEAR"]==2014][self.agg_col], autobinx=True, name="2014", marker_color='#330C73')
        trace7 = go.Histogram(x=df[df["YEAR"]==2013][self.agg_col], autobinx=True, name="2013", marker_color='#EB89B5')

        fig.append_trace(trace0, 1, 1)            
        fig.append_trace(trace1, 1, 2)
        fig.append_trace(trace2, 1, 3)
        fig.append_trace(trace3, 1, 4)
        fig.append_trace(trace4, 2, 1)
        fig.append_trace(trace5, 2, 2)
        fig.append_trace(trace6, 2, 3)
        fig.append_trace(trace7, 2, 4)

        fig.update_layout(
            autosize=False,
            height=500,
            width=900,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
        )

        fig.update_xaxes(title=f"{title}")
        fig.update_yaxes(title="Num. Municipalities")

        return fig.show()