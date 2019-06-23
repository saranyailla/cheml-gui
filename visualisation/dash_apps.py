import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.graph_objs as go
import random

original_df=pd.DataFrame()

#parameter df from stats function
def lineplot():
    #uncomment the below 2lines
    # global original_df
    # df = original_df
    #comment out the below line
    df=pd.read_csv('https://raw.githubusercontent.com/saranyailla/Blockchain-Election/master/test.csv')
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    df = df.select_dtypes(include=numerics)
    lab=[]
    for i in list(df):
        labels=dict()
        labels["label"]=i
        labels["value"]=i
        lab.append(labels)
    df = df.dropna()
    app =DjangoDash("SimpleExample2")
    app.layout = html.Div([
                        html.Div([html.P('Choose axes to plot the linearity'),dcc.Dropdown(id="first-value",value=lab[0]['value'],
                                                options=lab,placeholder="Select X-Axis"),
                                dcc.Dropdown(id="second-value",value=lab[0]['value'],options=lab,placeholder="Select Y-Axis")],
                                    style={"display": "block", "width": "30%"}),
                        html.Div([dcc.Graph(id="my-graph")])], className="container",id="layout-content")


    @app.callback(
        Output('my-graph', 'figure'),
        [Input('first-value', 'value'),Input('second-value', 'value')])
    def update_figure(first, second):
        dff = df
        trace = []
        trace.append(go.Scatter(x=dff[first], y=dff[second], mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
        return {"data": trace,
                "layout": go.Layout(title=first+" over "+second, colorway=[random.choice(['#fdae61', '#abd9e9', '#2c7bb6'])],
                                    yaxis={"title": first}, xaxis={"title": second})}

#File upload and table
def fileUpload():
    app =DjangoDash("SimpleExample")
    app.layout = html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files',
                style={
                    "color": "#0a6892",
                    "font-weight": "700",
                    "cursor": "pointer"
                })
            ]),
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload'),
    ])


    def parse_contents(contents, filename):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
                global original_df
                original_df=df
               
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
                original_df=df
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        df=df.head(5)
        return html.Div([
            html.Div([html.A('Lets go',id='visualize',className='btn btn-primary',href='statistics'),
            html.Div(['Please note that the following are only the first 5 rows of your uploaded file: ',html.B(filename)])
            ]),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
        ],style={"overflow-x": "scroll"})


    @app.callback(Output('output-data-upload', 'children'),
                [Input('upload-data', 'contents')],
                [State('upload-data', 'filename'),
                ])
    def update_output(list_of_contents, list_of_names):
        if list_of_contents is not None:
            children = [
                parse_contents(c, n) for c, n in
                zip(list_of_contents, list_of_names)]
            return children


# Get the column wise column stats of only the numeric fields
def columnStats():
    global original_df
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    num_columns = original_df.select_dtypes(include=numerics)
    # uncomment the following line
    # lineplot(num_columns)
    b=dict()
    for i in num_columns:
        a=dict()
        a['Mean']=round(num_columns[i].mean(),2)
        a['Median']=round(num_columns[i].median(),2)
        a['Maximum']=round(num_columns[i].max(),2)
        a['Minimum']=round(num_columns[i].min(),2)
        a['Standard Deviation']=round(num_columns[i].std(),2)
        b[i]=a    
    return b


#Scatterplot
#pass df parameter from stats function,use global df
def scatterPlot():
    # global original_df
    df = pd.read_csv('https://raw.githubusercontent.com/saranyailla/Blockchain-Election/master/test.csv')
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    num_columns = df.select_dtypes(include=numerics) 
    app =DjangoDash("scatterPlot")
    cat_lab=[]
    num_lab=[]
    for i in list(df):
        labels=dict()
        labels["label"]=i
        labels["value"]=i
        if((len(df[i].unique())/len(df))<0.2):
            cat_lab.append(labels)
        else:
            if i in list(num_columns):
                num_lab.append(labels)
    app.layout =html.Div([
                        html.Div([html.P('Choose axes and category to plot the scatter plot'),
                        dcc.Dropdown(id="first-value",value=num_lab[1]['value'],options=num_lab,placeholder="Select X-Axis"),
                        dcc.Dropdown(id="second-value",value=num_lab[1]['value'],options=num_lab,placeholder="Select Y-Axis"),
                        dcc.Dropdown(id="category-value",value=cat_lab[0]['value'],options=cat_lab,placeholder="Select Category")],
                         style={"display": "block", "width": "30%"}),
                        html.Div([dcc.Graph(id='scatter-graph')])], className="container")

    @app.callback(
        Output('scatter-graph', 'figure'),
        [Input('first-value', 'value'),Input('second-value', 'value'),Input('category-value', 'value')])
    def update_figure(first,second,third):
        dff = df
        trace = []
        trace=[
                go.Scatter(
                    x=dff[dff[third] == i][first],
                    y=dff[dff[third] == i][second],                    
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=str(i)
                ) for i in dff[third].unique()
        ]
        return {"data": trace,
                "layout": go.Layout(
                xaxis={'type':'log','title': first},
                yaxis={'title': second},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )}
        


    

