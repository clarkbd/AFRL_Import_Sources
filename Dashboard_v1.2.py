import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly import graph_objects as go
import numpy as np
from dash import Dash, dcc, html, Input, Output
import json


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
        html.H4( # added this to display link to info about country relations
            id='hover_link',
            style={
                'color': '#9bb3ce',
                'fontFamily': 'Open Sans, arial',
                'textAlign': 'center',
                'marginTop': 0
            }
        ),
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
  
    # This implementation is needed in order to have more control
    # over the layout/format of the hoverdata
    # The Plotly Express choropleth does not seem to provide a hook
    # into the underlying hover template in the same way that the
    # low level Graph Objects API does

    # first create a plain Figure object
    choropleth = go.Figure()

    # loop over all categories and add a separate trace for each one
    for i, category in enumerate(dff['Category'].unique()):
        # filter dataset to only include data for current category
        dff_subset = dff[dff['Category'] == category]
        trace = go.Choropleth(
            locations=dff_subset['name'],
            locationmode='country names',
            z=[i,] * len(dff_subset), # meant to specify color, constant
            name=category, # name each trace by the category for reference
            colorscale=(
                (0.0, color_dictionary[category]),
                (1.0, color_dictionary[category])
            ), # strange colorscale construction, but just maps to the dict
            customdata=np.stack((
                dff_subset['Percentage'], 
                dff_subset['Category'],
                dff_subset['name'],
                dff_subset['URL']
            ), axis=-1), # custom data so we can customize the hover template
            showscale=False,
            hovertemplate='<br>'.join([
                '<b>%{customdata[2]}</b>',
                '%{customdata[1]}',
                'Percent of Imports: %{customdata[0]}%',
            ]) + '<extra></extra>' # specifies what data gets shown and how
        )

        # add the trace to the choropleth figure
        choropleth.add_trace(trace)

    # update the layout to set margins and title
    choropleth.update_layout(
        margin=dict(l=30, r=30, t=50, b=20), # adjust these to shrink/expand
        title=f'Countries of import for {metal_value}'
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


# updates the hover link component with link to URL
# of page containing info about Country relations
@app.callback(
    Output('hover_link', 'children'),
    [Input('the_graph', 'hoverData')]
)
def handle_choropleth_hover(hover_data):
    print(hover_data)
    if hover_data is None:
        return 'Hover over countries to learn more'
    else:
        country_name = hover_data['points'][0]['location']
        category = hover_data['points'][0]['customdata'][1]
        link = html.A(
            children=f'Learn More about U.S. relations with {country_name}',
            href=hover_data['points'][0]['customdata'][3],
            target='_blank', # open in a new tab
            style={
                'textDecoration': 'underline',
                'color': color_dictionary[category]
            }
        )
        return link



if __name__ == '__main__':
    app.run_server(debug=True)


###COMMENT