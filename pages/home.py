from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import df

gender_map = {'Male': 'Мужчина', 'Female': 'Женщина'}
df['Gender'] = df['Gender'].map(gender_map)

category_map = {'Books': 'Книги', 'Clothing': 'Одежда', 'Home': 'Дом', 'Electronics': 'Электроника'}
df['Product Category'] = df['Product Category'].map(category_map)

layout = dbc.Container([
    html.H1("Главная", className='text-center my-4'),

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
                    {'label': 'Мужчина', 'value': 'Мужчина'},
                    {'label': 'Женщина', 'value': 'Женщина'}
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

    html.H1("Общая информация", className='text-center'),
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
        dbc.Col(dcc.Graph(id='returns-pie-chart'), width=6, className='p-0', style={'margin': '0 auto', 'textAlign': 'center'})
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
    
    revenue_by_date_df = filtered_df.groupby(pd.to_datetime(filtered_df['Purchase Date']).dt.date)['Total Purchase Amount'].sum().reset_index()
    revenue_by_date_fig = go.Figure(
        data=go.Scatter(x=revenue_by_date_df['Purchase Date'], y=revenue_by_date_df['Total Purchase Amount'], mode='lines+markers'),
        layout=go.Layout(
            title='Выручка по дням',
            xaxis_title='Дата покупки',
            yaxis_title='Общая сумма покупки',
            autosize=True
        )
    )

    # Круговая диаграмма с процентом возвратов
    returns_count = filtered_df['Returns'].value_counts().reset_index()
    returns_count.columns = ['Returns', 'Count']
    returns_count['Returns'] = returns_count['Returns'].map({0: 'Не возвращен', 1: 'Возвращен'})
    returns_pie_chart = px.pie(returns_count, names='Returns', values='Count', title='Процент возвратов', hole=0.3)
    
    return total_customers_fig, total_revenue_fig, churn_rate_fig, revenue_by_date_fig, returns_pie_chart