import sys
path = r"C:\Users\user\OneDrive\SpanishDragons\LineUp\venv\Lib\site-packages"
sys.path.append(path)
print(sys.path)

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

opt = []
for i in range(20):
    t_dict = {'label': str(i), 'value': str(i)}
    opt.append(t_dict)


app.layout = html.Div([
    html.H1(children="Dragon Boat Genetic Algorithm"),
    html.H2(children="By Ismael Sanz"),
    dcc.Checklist(
        id="dropdown",
        options=opt,
        labelStyle={"display": 'block'}),
    html.Div(id='my-div'),
    dcc.Input(id='my-id', value='input', type='text'),
    html.Div(id='my-div1'),
    dcc.Input(id='my-id2', value='input', type='text'),
    html.Div(id='my-div2'),
    html.Div(id='my-div3')
])


@app.callback(
    Output(component_id='my-div3', component_property='children'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_output_div(input_value):
    if input_value == None:
        return "none"
    else:
        texto = ""
        for x in input_value:
            texto = texto + " + " + x
        return texto


if __name__ == '__main__':
    app.run_server(debug=True)