import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import Dash, dcc, html, Input, Output

pio.renderers.default = 'browser'
app = Dash(__name__)


Import_Source = pd.read_csv("Import_Source_Pct.csv", header=0)

df = Import_Source

metals_subcategories = df[['Metal','Subcategory']].drop_duplicates()
metal_list = metals_subcategories['Metal'].unique().tolist()


app.layout = html.Div([
    dcc.Dropdown(
        metal_list,
        'Aluminum',
        id='metals_dropdown',
    ),

    html.Hr(),

    dcc.Dropdown(id='subcategories-dropdown'),

    html.Hr(),

    html.Div(id='display-selected-values'),

    html.Div([
        dcc.Graph(id='the_graph'),
        dcc.Graph(id='the_graph2')
    ]),
])

color_dictionary = {"NATO Member": "#3498DB", "Major Non-NATO Ally": "#5DADE2", "Strategic Partner": "#AED6F1",
                    "Strong Partner": "#27AE60",
                    "Limited Partner": "#58D68D", "Partner": "#ABEBC6", "Very Limited Partner": "#F9E79F",
                    "Potential Adversary": "#FAD7A0",
                    "Strategic Competitor": "#EC7063", "Other": "#D1E2E7"}


# ---------------------------------------------------------------

@app.callback(
    Output('subcategories-dropdown', 'options'),
    Output('subcategories-dropdown', 'value'),
    Input('metals_dropdown', 'value'))
def set_metal_options(selected_metal):
    subcategories = metals_subcategories[metals_subcategories['Metal'] == selected_metal]
    return subcategories['Subcategory'], subcategories['Subcategory'].iloc[0]


@app.callback(
    Output('the_graph', 'figure'),
    Output('the_graph2', 'figure'),
    Input('metals_dropdown', 'value'),
    Input('subcategories-dropdown', 'value'),
)
def update_graph(metal_value, subcategory):
    dff = df[df['Metal'] == metal_value]
    choropleth = px.choropleth(
        locations=dff['name'],
        locationmode="country names",
        color=dff['Category'],
        color_discrete_map=color_dictionary,
        hover_name=dff["Percentage"],
        title='Import Source Countries',
        scope="world"
    )


    dff2 = df.loc[
        (df["Metal"] == metal_value) & (df["Subcategory"] == subcategory)]
    piechart = px.pie(
        data_frame=dff2,
        values='Percentage', names='Country', title='Import Source Percentage - ' + subcategory, labels='Country',
        color=dff2['Category'],
        color_discrete_map=color_dictionary,
        hole=.3)

    return choropleth, piechart


if __name__ == '__main__':
    app.run_server(debug=True)