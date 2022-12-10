import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pycountry

import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

data = pd.read_csv("vaccinations-by-manufacturer-up.csv")
print(data.head())


df1_grouped = data.groupby('Vaccine_Manufacturer')

selected_geography = dcc.Dropdown(options=data['Vaccine_Manufacturer'].unique(),
                                  value='Pfizer/BioNTech')

for group_name, df_group in df1_grouped:
    vaccine_group = df1_grouped.get_group(group_name)
    list_countries = vaccine_group['Country'].unique().tolist()
    country_cnt = len(vaccine_group['Country'].unique())
    d_country_code = {}

    for country in list_countries:
        try:
            country_data = pycountry.countries.search_fuzzy(country)
            country_code = country_data[0].alpha_3
            d_country_code.update({country: country_code})
        except:
            print('could not add ISO 3 code for ->', country)
            d_country_code.update({country: ' '})

    for k, v in d_country_code.items():
        vaccine_group.loc[(vaccine_group.Country == k), 'iso_alpha'] = v

    fig = px.choropleth(data_frame=vaccine_group,
                        locations="iso_alpha",
                        color="Country",
                        color_continuous_scale=px.colors.sequential.Inferno,
                        hover_name="Vaccine_Manufacturer")
    fig.update_layout(
        title_text="Countries {}".format(country_cnt))

vaccine_count = data.groupby("Vaccine_Manufacturer")["Country"].nunique()
Vaccine_Manufacturer_count = pd.DataFrame(
    {'Vaccine_Manufacturer': vaccine_count.index, 'Count': vaccine_count.values})

fig_1 = px.treemap(
    Vaccine_Manufacturer_count, path=["Vaccine_Manufacturer", "Count"], values="Count"

)
fig_1.update_traces(root_color="lightgrey")

app.layout = html.Div(children=[
    # elements from the top of the page
    html.Div([
        html.H1(children='Dash app1'),
        html.Div(children='''
      Dash: First graph.'''),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Dash app2'),
        html.Div(children='''
      Dash: Second graph. '''),

        dcc.Graph(
            id='graph2',
            figure=fig_1
        ),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
