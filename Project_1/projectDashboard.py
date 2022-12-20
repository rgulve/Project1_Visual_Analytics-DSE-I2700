from dash import Dash, html, dcc, Input, Output
import pandas as pd
import pycountry
import plotly.express as px
import plotly.graph_objects as go
import base64

data = pd.read_csv("VaccineBreakout_1.csv")
print(data.head())

app = Dash()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
Vaccine_dropdown = dcc.Dropdown(options=data['Vaccine_Manufacturer'].unique(),
                                value='Pfizer/BioNTech')

Country_dropdown = dcc.Dropdown(options=data['Country'].unique(),
                                value='Argentina')

# app.layout = html.Div(children=[
#     html.H1(children='Vaccine Administrated Globally'),
#     geo_dropdown,
#     dcc.Graph(id='graph1'),
#
# ])

app.layout = html.Div(style={'backgroundColor': colors['background']}, className='row', children=[
    html.H1("Covid-19 Vaccine Administrated Globally", style={
        'textAlign': 'center',
        'color': colors['text']}),
    Vaccine_dropdown,
    html.Div(children=[
        dcc.Graph(id="graph3", style={'display': 'inline-block'}),
        dcc.Graph(id="graph1", style={'display': 'inline-block'}),

    ]),

    # app.layout = html.Div(children=[
    #     html.Div([
    #         html.H1(children='Bubble Chart'),
    #         dcc.Graph(id="graph3"),
    #         #  dcc.Graph(id='graph3'),
    #
    #     ]),

    # html.Div([
    #     html.H1(children='Vaccine Administrated Globally'),
    #     Vaccine_dropdown,
    #     dcc.Graph(
    #         id='graph1',
    #     ),
    # ]),

    html.Div([
        dcc.Graph(
            id='graph2',
        ),
    ]),

    html.H1("Covid-19 Vaccine Breakout & Efficacy for different types of variants", style={
        'textAlign': 'center',
        'color': colors['text']}),
    Country_dropdown,
    html.Div(style={'backgroundColor': colors['background']}, children=[
        dcc.Graph(id="graph5", style={'display': 'inline-block'}),
        dcc.Graph(id="graph4", style={'display': 'inline-block'}),

    ]),

    # html.Div([
    #     html.H1(children='Covid-19 Vaccine breakout for different types of variants'),
    #     dcc.Graph(
    #         id='graph5',
    #     ),
    # ]),

    # html.Div([
    #     html.H1(children='Covid-19 Vaccine Efficacy for different types of Vaccines'),
    #     Country_dropdown,
    #     dcc.Graph(
    #         id='graph4',
    #     ),
    # ]),

])


@app.callback(
    [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure'), Output('graph4', 'figure'),
     Output('graph5', 'figure')],
    Input(component_id=Vaccine_dropdown, component_property='value'),
    Input(component_id=Country_dropdown, component_property='value')
)
def update_graph(selected_geography, selected_country):
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
                        hover_name="Vaccine_Manufacturer",
                        template='plotly_dark')
    fig.update_layout(
        title_text="Countries {}".format(country_cnt))

    vaccine_count = data.groupby("Vaccine_Manufacturer")["Country"].nunique()
    Vaccine_Manufacturer_count = pd.DataFrame(
        {'Vaccine_Manufacturer': vaccine_count.index, 'Count': vaccine_count.values})

    fig_1 = px.treemap(
        Vaccine_Manufacturer_count, path=["Vaccine_Manufacturer", "Count"], values="Count", template='plotly_dark'
    )
    # fig_1.update_traces(root_color="lightgrey")

    gk_1 = data.groupby('Vaccine_Manufacturer')
    Oxford = gk_1.get_group(selected_geography)
    fig_2 = px.scatter(Oxford, x='Country', y='Total_Vaccinations', size='Total_Vaccinations', color="Country",
                       hover_name="Vaccine_Manufacturer", size_max=70, template='plotly_dark')

    df = data[data["Country"] == selected_country]

    fig_3 = go.Figure()

    fig_3.add_trace(
        go.Bar(x=df['Vaccine_Manufacturer'], y=df['Omicron_Infection_Efficacy'], name='Omicorn_Infection_Efficacy'))

    fig_3.add_trace(go.Bar(x=df['Vaccine_Manufacturer'], y=df['Alpha_Ancestral_Infection_Efficacy'],
                           name='Alpha_Ancestral_Infection_Efficacy'))

    fig_3.add_trace(go.Bar(x=df['Vaccine_Manufacturer'], y=df['Beta_Gamma_Delta_Infection_Efficacy'],
                           name='Beta_Gamma_Delta_Infection_Efficacy'))

    fig_3.update_layout(title_text='Variant wise Vaccine Efficacy in {}'.format(selected_country),
                        template='plotly_dark')

    df.drop_duplicates(subset=['Country'], inplace=True)

    fig_4 = go.Figure()

    fig_4.add_trace(go.Bar(x=df['Country'], y=df['Susceptible_BreakOut_for_Omicron_Infection'],
                           name='Susceptible BreakOut for Omicron Infection'))

    fig_4.add_trace(go.Bar(x=df['Country'], y=df['Susceptible_BreakOut_for_Alpha_Ancestral_Infection'],
                           name='Susceptible BreakOut for Alpha Ancestral Infection'))

    fig_4.add_trace(go.Bar(x=df['Country'], y=df['Susceptible_BreakOut_for_Beta_Gamma_Delta_Infection'],
                           name='Susceptible BreakOut for Beta Gamma Delta Infection'))

    fig_4.update_layout(title_text='Susceptible BreakOut in {}'.format(selected_country), template='plotly_dark')

    return fig, fig_1, fig_2, fig_3, fig_4


if __name__ == '__main__':
    app.run_server(debug=True)
