from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

cases_data = "https://raw.githubusercontent.com/iffaxoo/MCM7003/data/cases.csv"
patient_data = "https://raw.githubusercontent.com/iffaxoo/MCM7003/data/patient.csv"

dfCases = pd.read_csv(cases_data, encoding="latin")
dfCases.dropna(inplace=True)

dfPatient = pd.read_csv(patient_data, encoding="latin")
patient_data_clean = dfPatient.loc[:, ['gender', 'age', 'current_state']].dropna()

app = Dash(__name__, external_stylesheets=external_stylesheets)

def create_covid_cases_figure(selected_series):
    fig = px.line(dfCases, x=dfCases.index, y=selected_series,
                  labels={'value': 'Number of Cases', 'variable': 'Case Type'},
                  title="COVID-19 Cases in Indonesia")
    return fig

def create_age_distribution_figure():
    fig = px.histogram(patient_data_clean, x='age', nbins=20, title="Distribution of Covid-19 Patient in Indonesia by Age")
    return fig

def create_gender_pie_chart_figure():
    gender_counts = patient_data_clean['gender'].value_counts()

    fig = px.pie(
        values=gender_counts.values,
        names=gender_counts.index,
        title="Percentage of Covid-19 Patient in Indonesia by Gender",
        labels={'gender': 'Gender'},
    )
    
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(showlegend=True)

    return fig

def create_current_state_pie_chart():
    state_counts = patient_data_clean['current_state'].value_counts()

    fig = px.pie(
        values=state_counts,
        names=state_counts.index,
        title="Percentage of Current State of Covid-19 Patient in Indonesia"
    )

    return fig

def create_confirmed_patient_age_distribution_figure(selected_age_range):
    min_age, max_age = selected_age_range
    filtered_data = patient_data_clean[(patient_data_clean['age'] >= min_age) & (patient_data_clean['age'] <= max_age)]
    
    fig = px.scatter(filtered_data, x='age', title="Age Distribution of Confirmed Patients",
                     labels={'age': 'Age'},
                     size_max=20, opacity=0.7)
    fig.update_traces(marker=dict(size=8, opacity=0.7))
    return fig

image_url = "https://images.unsplash.com/photo-1639322537231-2f206e06af84?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1932&q=80"

background_style = {
    'background-image': f'url("{image_url}")',
    'background-size': 'cover',
    'background-position': 'center',
    'background-repeat': 'no-repeat',
    'position': 'fixed',
    'top': 65,
    'left': 0,
    'width': '100%',
    'height': '100%',
    'z-index': -2
}

onboarding_style = {
    'position': 'relative',
    'z-index': 1,  # Set a higher z-index
}

# Define the onboarding layout
onboarding_layout = html.Div([
    html.Div([
        html.H1("Welcome to COVID-19 Dashboard", className='display-4 text-center text-white'),
        html.Br(),
        html.P("This dashboard provides insights into COVID-19 cases and patient data in Indonesia.",
               className='lead text-center text-white'),
        html.P("Explore the tabs to visualize different aspects of the pandemic. ",
               className='text-center text-white'),
        html.Br(),
        html.P("by Iffa Nurlatifah 1221400166 ",
               className='text-center text-white'),
    ], className='container bg', style={
        'padding': '2rem',
        'color': 'white',
        'display': 'flex',
        'flex-direction': 'column',
        'justify-content': 'center',
        'height': '100%',  # Set the container to fill the height of the viewport
    }),
], style={**onboarding_style, **background_style})


custom_tabs_style = {
    'font-family': 'Arial, sans-serif',
    'background-color': '#152238',
    'border': 'none',
    'color': 'white',
}

custom_tab_content_style = {
    'padding': '20px',
}

custom_tab_content_container_style = {
    'background-color': 'black',
}

app.layout = html.Div([
dcc.Tabs(id='main-tabs', value='home', children=[
    dcc.Tab(label='Home', value='home', style=custom_tabs_style),  # Apply custom style here
    dcc.Tab(label='Cases', value='cases', style=custom_tabs_style),
    dcc.Tab(label='Patients', value='patients', style=custom_tabs_style),
    dcc.Tab(label='Confirmed Patient', value='confirmed_patient', style=custom_tabs_style)
    ]),
    html.Div(id='main-tabs-content', style={**custom_tab_content_style, **custom_tab_content_container_style})
], style={'background-color': '#152238'})



@app.callback(Output('main-tabs-content', 'children'), Input('main-tabs', 'value'))
def render_tab_content(tab_value):
    if tab_value == 'home':
        return onboarding_layout
    elif tab_value == 'cases':
        return html.Div([
            html.H1("COVID-19 Cases in Indonesia", className='display-4 mt-3 mb-4 text-center text-white'),
            dcc.Checklist(
                id='cases-checkbox',
                options=[
                    {'label': 'New Released', 'value': 'new_released'},
                    {'label': 'New Deceased', 'value': 'new_deceased'},
                    {'label': 'Accumulated Released', 'value': 'acc_released'},
                    {'label': 'Accumulated Deceased', 'value': 'acc_deceased'}
                ],
                value=['new_released', 'new_deceased', 'acc_released', 'acc_deceased'],
                labelStyle={'display': 'block'}
            ),
            html.Br(),
            dcc.Graph(id='covid_cases_fig')
        ], className='container bg', style={'padding': '2rem', 'color': 'white'})
    elif tab_value == 'patients':
        return html.Div([
            html.H1("COVID-19 Patients", className='display-4 mt-3 mb-4 text-center text-white'),
            dcc.RadioItems(
                id='graph_selector',
                options=[
                    {'label': 'Age Distribution', 'value': 'age'},
                    {'label': 'Gender Distribution', 'value': 'gender'},
                    {'label': 'Current State Distribution', 'value': 'current_state'},
                ],
                value='age',
                labelStyle={'display': 'block'},
            ),
            html.Br(),
            dcc.Graph(id='selected_patient_chart')
        ], className='container bg', style={'padding': '2rem', 'color': 'white'})
    elif tab_value == 'confirmed_patient':
        return html.Div([
            html.H1("Age distribution of Confirmed Patients", className='display-4 mt-3 mb-4 text-center text-white'),
            html.Br(),
            dcc.RangeSlider(
                id='age-range-slider',
                min=0,
                max=100,
                step=1,
                value=[0, 100],  # Default value for the entire age range
                marks={i: str(i) for i in range(0, 101, 10)},
            ),
            html.Br(),
            dcc.Graph(id='confirmed_patient_age_dist_fig')
        ], className='container bg', style={'padding': '2rem', 'color': 'white'})

@app.callback(
    Output('selected_patient_chart', 'figure'),
    Input('graph_selector', 'value')
)
def update_selected_patient_chart(selected_chart):
    return update_patient_chart(selected_chart)

@app.callback(
    Output('covid_cases_fig', 'figure'),
    Input('cases-checkbox', 'value')
)
def update_covid_cases_chart(selected_series):
    fig = create_covid_cases_figure(selected_series)
    return fig

@app.callback(
    Output('confirmed_patient_age_dist_fig', 'figure'),
    Input('age-range-slider', 'value')
)
def update_confirmed_patient_age_distribution_plot(selected_age_range):
    return create_confirmed_patient_age_distribution_figure(selected_age_range)

def update_patient_chart(selected_chart):
    if selected_chart == 'age':
        return create_age_distribution_figure()
    elif selected_chart == 'gender':
        return create_gender_pie_chart_figure()
    elif selected_chart == 'current_state':
        return create_current_state_pie_chart()
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True, port=8053)