from dash import Dash, html, dcc, Input, Output
import pandas as pd
import pycountry
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("merged_data.csv")
print(data.head())

app = Dash()

geo_dropdown = dcc.Dropdown(options=data['Vaccine_Manufacturer'].unique(),
                            value='Pfizer/BioNTech')

# app.layout = html.Div(children=[
#     html.H1(children='Vaccine Administrated Globally'),
#     geo_dropdown,
#     dcc.Graph(id='graph1'),
#
# ])


app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Treemap'),
        dcc.Graph(
            id='graph2',
        ),
    ]),
    # elements from the top of the page
    html.Div([
        html.H1(children='Vaccine Administrated Globally'),
        geo_dropdown,
        dcc.Graph(
            id='graph1',
        ),
    ]),
    # New Div for all elements in the new 'row' of the page

    html.Div([
        html.H1(children='Bubble Chart'),
        dcc.Graph(
            id='graph3',
        ),
    ]),
    html.Div([
        html.H1(children='Bar Chart'),
        dcc.Graph(
            id='graph4',
        ),
    ]),
])


@app.callback(
    [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure'), Output('graph4', 'figure')],
    Input(component_id=geo_dropdown, component_property='value')
)
def update_graph(selected_geography):
    df1_grouped = data.groupby('Vaccine_Manufacturer')
    vaccine_group = df1_grouped.get_group(selected_geography)
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

    total = data.groupby(['Country', 'Vaccine_Manufacturer'])["Total_Vaccinations"].sum().rename(
        "Total_sum").reset_index()
    df_1 = data.merge(total)
    gk_1 = df_1.groupby('Vaccine_Manufacturer')
    Oxford = gk_1.get_group(selected_geography)
    fig_2 = px.scatter(Oxford, x='Country', y='Total_sum', size='Total_sum', color="Country",
                       hover_name="Vaccine_Manufacturer", size_max=70)
    df = data.query("Country=='Argentina'")

    colors = ['lightslategray', ] * 5
    colors[1] = 'crimson'

    fig_3 = go.Figure()

    fig_3.add_trace(go.Bar(data_frame=df, x='Date', y='Susceptible_BreakOut_for_Omicorn_Infection',
                           name='Susceptible BreakOut for Omicorn Infection'))

    fig_3.add_trace(go.Bar(x='Date', y='Susceptible_BreakOut_for_Omicorn_Severe_Disease',
                           name='Susceptible BreakOut for Omicorn Severe Disease'))

    fig_3.add_trace(go.Bar(x='Date', y='Susceptible_BreakOut_for_Alpha_Ancestral_Severe_Disease',
                           name='Susceptible BreakOut for Alpha Ancestral Severe Disease'))

    fig_3.add_trace(go.Bar(x='Date', y='Susceptible_BreakOut_for_Alpha_Ancestral_Infection',
                           name='Susceptible BreakOut for Alpha Ancestral Infection'))

    fig_3.add_trace(go.Bar(x='Date', y='Susceptible_BreakOut_for_Beta_Gamma_Delta_Severe_Disease',
                           name='Susceptible BreakOut for Beta Gamma Delta Severe Disease'))

    fig_3.add_trace(go.Bar(x='Date', y='Susceptible_BreakOut_for_Beta_Gamma_Delta_Infection',
                           name='Susceptible BreakOut for Beta Gamma Delta Infection'))

    fig_3.update_layout(title_text='Susceptible BreakOut in Argentina')

    return fig, fig_1, fig_2, fig_3


if __name__ == '__main__':
    app.run_server(debug=True)
