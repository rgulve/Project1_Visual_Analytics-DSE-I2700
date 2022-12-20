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

bubble_chart_text = 'The first chart displays the relationship between the number of total vaccinations by country. The colors of the bubbles indicate the country, with some countries sharing the same color, butseparated by a distance enough to distinguish them. The sizes of the bubbles indicate how large or small the total number of vaccinations are. The purpose of this graph is to offer more information than a two-dimensional graph of total vaccinations by country by considering the shapes and colors of the bubbles. This chart is also interactive in that it displays meta data about each bubble.'
bubble_chart_analysis_text = 'From the chart, we can easily tell the top 5 countries with the most vaccinations are (1) United States, (2) Japan, (3) Germany, (4) France, and (5) Italy, in order for Pfizer.The most Pfizer vaccinations administered in a country was around 370 million, while the smallest was around 700 thousand.'

tree_map_text = 'This interactive map displays all the countries that were administered by the selected vaccine in the dropdown bar. The map distinguishes each country by a unique color. Again, we have some countries that share the same color, but none are adjacent to each other, so it should be easy to tell the difference. What is also displayed is the total number of countries that were administered the vaccine to provide insight. Additionally, you can zoom in or out of the map for viewing purposes as well. The purpose of this mapis to help visualize the contrast between vaccines adminitered globally per vaccine, as well as the scale of such vaccines around the world.'
tree_map_analysis_text = 'From looking at all the vaccines in the dropdown bar, we see that CanSino has the lowest number of countries in which the vaccines were administered at just 2 countries, with the highest being Pfizer at 43 countries and two vaccines just shy away at 38 countries. The numberof countries vaccinated by each vaccine are also grouped by size to quickly show which vaccines were less used opposed to others.'

vaccine_breakout_text = 'This chart compares the vaccine breakout for each vaccine per country. This allows the reader to make easy comparisons between the vaccine break out. The purpose of this chart is to allow the reader to select betweeen countries and easily identify and compare vaccine breakouts for all vaccines administered in that country.'
vaccine_breakout_analysis_text = 'From looking at most countries, it is very clear that the Alpha Ancestral and Beta Gamma Delta infections have very close breakout values, as opposed to the Omicron which is much significantly higher for each country. What might this data infer about the vaccine efficacy? How might such consistency vary by country?'

vaccine_breakout_text2 = 'Similar to the previous graph, this side-by-side bar plot compares the vaccine efficacy for each vaccine type grouped by the infections. This makes it easy to determine which vaccine has performed the best amongst all three infections shown. The purpose of this chart is to provide comparison between vaccine efficacy for each vaccine type and infection for a given country, that can be selected from the dropdown menu. Then analysts could determine which countries need higher efficacy rates, and how to avoid large breakouts for infections.'
vaccine_breakout_analysis_text2 = ''

suggestions_text_header = 'Based on our analyses, we believe that there are a few recommendations that we can provide in order to improve some of the vaccine efficacy rates in terms of vaccine distribution.'


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
    html.H4('How Do Vaccinations Vary By Country?', style={'color': 'red'}),
    dcc.Markdown(bubble_chart_text, style={'color': 'white'}),
    dcc.Markdown(bubble_chart_analysis_text, style={'color': 'white'}),
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
        html.H4('How Popular Are Vaccine Types Globally?', style={'color': 'red'}),
        dcc.Markdown(tree_map_text, style={'color': 'white'}),
        dcc.Graph(
            id='graph2',
        ),
    html.H4('How Can Access to Different Vaccines Influence a Country\'s Efficacy Rate?', style={'color': 'red'}),
    dcc.Markdown(tree_map_analysis_text, style={'color': 'white'}),
    ]),

    html.Div([
        html.H1("Covid-19 Vaccine Breakout & Efficacy for different types of variants", style={
            'textAlign': 'center',
            'color': colors['text']}),
        html.H4('What Can Infection Rates Infer About Vaccine Types per Country?', style={'color': 'red'}),
        dcc.Markdown(vaccine_breakout_text, style={'color': 'white'}),
        dcc.Markdown(vaccine_breakout_analysis_text, style={'color': 'white'}),
        Country_dropdown,
        html.Div(style={'backgroundColor': colors['background']}, children=[
            dcc.Graph(id="graph5", style={'display': 'inline-block'}),
            dcc.Graph(id="graph4", style={'display': 'inline-block'}),
        html.H4('What Might the Popularity of a Vaccine Type Infer About its Efficacy Rates?', style={'color': 'red'}),
        dcc.Markdown(vaccine_breakout_text2, style={'color': 'white'}),
        ]),
    ]),

    html.Div([
        html.H1('Suggestions', style={
        'textAlign': 'center',
        'color': colors['text']}),
        dcc.Markdown(suggestions_text_header, style={'color': 'white'}),
        dcc.Markdown('''
        Encourage individuals who have been vaccinated to receive their second/third vaccination as required.
        *Suggestion #2
        ''', style={'color': 'white'}),
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
