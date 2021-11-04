# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 00:47:33 2021

"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_csv("Wells Table.csv")

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[html.Div(
            children=[
                html.H1(
                    children="Wells Analytics",style={'textAlign': 'center'}, className="header-title"), #Header title
                html.H2(
                    children="Analyze the Wells records"
                    " by county in the Permian Basin"
                    " between 2018 and 2021",
                    className="header-description", style={'textAlign': 'center'},
                ),
            ],
            className="header",style={'backgroundColor':'#F5F5F5'},
        ),
        
        
        html.Div(
            children=[
                html.Div(children = 'Year', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'year-filter',
                    options = [
                        {'label': Year, 'value':Year}
                        for Year in sorted(df.Year.unique())
                    ], 
                    value ='2021',
                    multi=False,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'menu',
        ), 
        
        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'scatter',
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'bar',
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'bibar',
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'barPlay',
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
        ],
        className = 'double-graph',
        ), 
    ]
)

@app.callback(
    Output("scatter", "figure"),
    [Input("year-filter", "value")],
)
def update_chart1(Year):
    filtered_data = df.loc[df.Year == int(Year),:] 
    scatter = px.scatter(
        filtered_data,
        x="County",
        y="Operator Company Name",
        size="DI Lateral Length",
        color="DI Lateral Length",
        color_continuous_scale=px.colors.sequential.Plotly3,
        title="Total Lateral Length by County",
    )
    scatter.update_layout(
        xaxis_tickangle=30,
        title=dict(x=0.5),
        xaxis_tickfont=dict(size=9),
        yaxis_tickfont=dict(size=9),
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="#BDBDBD",
    )
    return scatter

@app.callback(Output("bar", "figure"),
    [Input("year-filter", "value")],
)
def update_chart2(Year):
    filtered_data = df[df.loc[:,"Year"] == int(Year)]
    bar = px.bar(
        filtered_data,
        x=filtered_data.groupby("Operator Company Name")["DI Lateral Length"].agg(sum),
        y=filtered_data["Operator Company Name"].unique(),
        color=filtered_data.groupby("Operator Company Name")["DI Lateral Length"].agg(sum),
        color_continuous_scale=px.colors.sequential.RdBu,
        text=filtered_data.groupby("Operator Company Name")["DI Lateral Length"].agg(sum),
        title="Drilled Lateral by Operator",
        orientation="h",
    )
    bar.update_layout(
        title=dict(x=0.5), margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="#BDBDBD"
    )
    bar.update_traces(texttemplate="%{text:.2s}")
    return bar

@app.callback(
    Output("bibar", "figure"),
    [Input("year-filter", "value")],
)
def update_chart3(Year): 
    filtered_s1 = df.loc[(df.loc[:,'Production Type']=='OIL')&(df.loc[:,'Year']==int(Year)),:]
    filtered_s2 = df.loc[(df.loc[:,'Production Type']=='GAS')&(df.loc[:,'Year']==int(Year)),:]
    trace1 = go.Bar(
        x=filtered_s1["County"].unique(),
        y=filtered_s1.groupby("County")["DI Lateral Length"].agg(sum),
        text=filtered_s1.groupby("County")["DI Lateral Length"].agg(sum),
        textposition="outside",
        marker_color=px.colors.qualitative.Dark24[0],
        name="Oil Wells",
    )
    trace2 = go.Bar(
        x=filtered_s2["County"].unique(),
        y=filtered_s2.groupby("County")["DI Lateral Length"].agg(sum),
        text=filtered_s2.groupby("County")["DI Lateral Length"].agg(sum),
        textposition="outside",
        marker_color=px.colors.qualitative.Dark24[1],
        name="Gas wells",
    )
    data = [trace1, trace2]
    layout = go.Layout(barmode="group", title="Oil Wells vs Gas wells")
    bibar = go.Figure(data=data, layout=layout)
    bibar.update_layout(
        title=dict(x=0.5),
        xaxis_title="County",
        yaxis_title="DI Lateral Length",
        paper_bgcolor="#BDBDBD",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    bibar.update_traces(texttemplate="%{text:.2s}")
    return bibar

@app.callback(
    Output("barPlay", "figure"),
    [Input("year-filter", "value")],
)
def update_chart4(Year):
    filtered_data = df[df["Year"] == int(Year)]
    barPlay = px.bar(
        filtered_data,
        x=filtered_data.groupby("DI Play")["DI Lateral Length"].agg(sum),
        y=filtered_data["DI Play"].unique(),
        labels={"x": "Total Recorded", "y": "DI Play"},
        color=filtered_data.groupby("DI Play")["DI Lateral Length"].agg(sum),
        color_continuous_scale=px.colors.sequential.Sunset,
        # color_discrete_sequence=['rgb(253,180,98)','rgb(190,186,218)'],
        text=filtered_data.groupby("DI Play")["DI Lateral Length"].agg(sum),
        title="Total Lateral by Basin",
        # ,barmode = 'group'
        orientation="h",
    )
    barPlay.update_layout(title=dict(x=0.5), paper_bgcolor="#BDBDBD")
    barPlay.update_traces(texttemplate="%{text:.2s}")
    return barPlay

app.run_server(debug=True)