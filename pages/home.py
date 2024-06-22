from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from data import df


layout = dbc.Container([
    html.H1("Фильтрация данных", className='text-center my-4'),

    # Селекторы в одну строку
    dbc.Row([
        dbc.Col([
            html.Label("Выберите диапазон дат:", className='d-block'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df['Purchase Date'].min(),
                end_date=df['Purchase Date'].max(),
                display_format='YYYY-MM-DD',
                className='d-block'
            ),
        ], width=4, className='me-3'),

        dbc.Col([
            html.Label("Выберите пол:", className='d-block'),
            dcc.Dropdown(
                id='gender-dropdown',
                options=[
                    {'label': 'Male', 'value': 'Male'},
                    {'label': 'Female', 'value': 'Female'}
                ],
                multi=False,
                placeholder="Select...",
                className='d-block'
            ),
        ], width=3, className='me-3'),

        dbc.Col([
            html.Label("Введите возраст:", className='d-block'),
            dcc.Input(
                id='age-input',
                type='number',
                placeholder='Введите возраст',
                className='d-block'
            ),
        ], width=4)
    ], className='mb-3 align-items-end g-0'),

    # Индикаторы
    dbc.Row([
        dbc.Col(dcc.Graph(id='total-customers'), width=4, className='p-0'),
        dbc.Col(dcc.Graph(id='total-revenue'), width=4, className='p-0'),
        dbc.Col(dcc.Graph(id='churn-rate'), width=4, className='p-0'),
    ], className='g-0'),
    
    # График выручки по дням
   dbc.Row([
        dbc.Col(dcc.Graph(id='revenue-by-date'), width=12, className='p-0')
    ], className='mt-3 g-0'),

    # Круговая диаграмма с процентом возвратов
    dbc.Row([
        dbc.Col(dcc.Graph(id='returns-pie-chart'), width=6, className='p-0')
    ], className='mt-3 g-0')
], fluid=True)

@callback(
    [Output('total-customers', 'figure'),
     Output('total-revenue', 'figure'),
     Output('churn-rate', 'figure'),
     Output('revenue-by-date', 'figure'),
     Output('returns-pie-chart', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('gender-dropdown', 'value'),
     Input('age-input', 'value')]
)
def update_indicators_and_graph(start_date, end_date, selected_gender, selected_age):
    # Фильтрация данных
    filtered_df = df[
        (df['Purchase Date'] >= start_date) &
        (df['Purchase Date'] <= end_date)
    ]
    
    if selected_gender:
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_age:
        filtered_df = filtered_df[filtered_df['Age'] == selected_age]
    
    # Общее количество клиентов
    total_customers = filtered_df['Customer ID'].nunique()
    total_customers_fig = go.Figure(go.Indicator(
        mode = "number",
        value = total_customers,
        title = {"text": "Кол-во клиентов"}
    ))

    # Выручка
    total_revenue = filtered_df['Total Purchase Amount'].sum()
    total_revenue_fig = go.Figure(go.Indicator(
        mode = "number",
        value = total_revenue,
        title = {"text": "Выручка"}
    ))

    # Отток клиентов
    churn_rate = (filtered_df['Churn'].sum() / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    churn_rate_fig = go.Figure(go.Indicator(
        mode = "number",
        value = churn_rate,
        title = {"text": "Отток клиентов (%)"}
    ))
    
    # График выручки по дням
    revenue_by_date_df = filtered_df.groupby('Purchase Date')['Total Purchase Amount'].sum().reset_index()
    revenue_by_date_fig = px.line(revenue_by_date_df, x='Purchase Date', y='Total Purchase Amount', title='Выручка по дням')
    
    # Круговая диаграмма с процентом возвратов
    returns_count = filtered_df['Returns'].value_counts().reset_index()
    returns_count.columns = ['Returns', 'Count']
    returns_count['Returns'] = returns_count['Returns'].map({0: 'No Return', 1: 'Return'})
    returns_pie_chart = px.pie(returns_count, names='Returns', values='Count', title='Процент возвратов', hole=0.3)
    
    return total_customers_fig, total_revenue_fig, churn_rate_fig, revenue_by_date_fig, returns_pie_chart