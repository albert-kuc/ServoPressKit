import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import plotly.express as px

import pandas as pd
from helpers import LogFileToDf

# alternative layout
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUX]

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Br(),
    html.Div(id='output-data-upload'),
    html.Br(),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if 'log' in filename:
        log_file_object = LogFileToDf(io.StringIO(decoded.decode('utf-8')))
        summary_df = log_file_object.file_summary.reset_index()
        df = log_file_object.record_df
        if not log_file_object.press_data_empty:
            fig = px.line(df, x='[Position]', y='[Force]',
                          range_x=[int(min(df['[Position]'])), int(max(df['[Position]']) + 1)],
                          height=600,
                          line_group=df['[Record #]'],
                          color=df['[Record #]'])
        else:
            fig = {'layout': {'height': '600'}}
    else:
        return html.Div([
            'File with ".log" extension required.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(('File last modification date: ',
                 datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))),

        dash_table.DataTable(
            data=summary_df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in summary_df.columns[1:]]
        ),
        dcc.Graph(figure=fig),

        html.Hr(),

        # For debugging, display the raw content provided by the web browser
        html.Div('Raw content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output(component_id='output-data-upload', component_property='children'),
              Input(component_id='upload-data', component_property='contents'),
              State(component_id='upload-data', component_property='filename'),
              State(component_id='upload-data', component_property='last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def main():
    app.run_server(debug=True)


if __name__ == '__main__':
    main()
