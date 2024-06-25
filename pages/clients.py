from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import df


layout = dbc.Container([
    html.H1("Анализ клиентов", className='text-center my-4'),

    # Селекторы в одну строку с отступами
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
        ], id='left-align', width=4, className='me-3'),  

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
                className='d-block',
                style={'width': '150px'}  
            ),
        ], id='center-align', width='auto', className='me-3'),  

        dbc.Col([
            html.Label("Введите возраст:", className='d-block'),
            dcc.Input(
                id='age-input',
                type='number',
                placeholder='Введите возраст',
                className='d-block'
            ),
        ], id='right-align', width=4)
    ], className='mb-3 align-items-end g-0'),  

    # Столбчатая диаграмма по возрасту клиентов
    dbc.Row([
        dbc.Col(dcc.Graph(id='age-bar-chart'), width=12, className='p-0')
    ], className='mt-3 g-0'),


    dbc.Row([
        dbc.Col(dcc.Graph(id='gender-pie-chart'), width=4, className='p-0'),
        dbc.Col(dcc.Graph(id='churn-bar-chart'), width=8, className='p-0'),
    ], className='mt-3 g-0'), 

    dbc.Row([
        dbc.Col([
            html.H3("Топ-5 клиентов по выручке", className='text-center my-4'),
            dbc.Table(id='top-customers-table', bordered=True, striped=True, hover=True, responsive=True)
        ], width=4, className='mr-3'),
        dbc.Col([
            html.H3("Топ-5 клиентов по возвратам", className='text-center my-4'),
            dbc.Table(id='top-5-returns-table', striped=True, bordered=True, hover=True)
        ], width=4, className='mr-3')  
    ]), 
], fluid=True) 

# Коллбэк для обновления графиков на основе селекторов
@callback(
    [Output('age-bar-chart', 'figure'),
     Output('gender-pie-chart', 'figure'),
     Output('churn-bar-chart', 'figure'),
     Output('top-customers-table', 'children'),
     Output('top-5-returns-table', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('gender-dropdown', 'value'),
     Input('age-input', 'value')]
)
def update_graphs(start_date, end_date, selected_gender, selected_age):
    # Фильтрация данных
    filtered_df = df[
        (df['Purchase Date'] >= start_date) &
        (df['Purchase Date'] <= end_date)
    ]
    
    if selected_gender:
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    

    # Столбчатая диаграмма по возрасту клиентов
    age_gender_df = df.groupby(['Age', 'Gender']).size().reset_index(name='Count') 
    age_bar_chart = px.bar(
    age_gender_df,
    x='Age',
    y='Count',
    color='Gender',
    barmode='stack',
    title='Распределение клиентов по возрасту',
    labels={
        'Age': 'Возраст',
        'Count': 'Количество',
        'Gender': 'Пол',
    }
)

    # Круговая диаграмма с распределением клиентов по полу
    gender_count = df['Gender'].value_counts().reset_index()  
    gender_count.columns = ['Gender', 'Count']
    gender_pie_chart = px.pie(gender_count, 
    names='Gender', 
    values='Count', 
    title='Распределение клиентов по полу',
        labels={
        'Count': 'Количество',
        'Gender': 'Пол',
    }, 
    hole=0.3)

    # Фильтрация данных по возрасту для диаграммы по оттоку клиентов
    if selected_age:
        filtered_df = filtered_df[filtered_df['Age'] == selected_age]

    # Столбчатая диаграмма по оттоку клиентов
    churn_age_df = filtered_df[filtered_df['Churn'] == 1].groupby(['Age', 'Gender']).size().reset_index(name='Count')
    churn_bar_chart = px.bar(churn_age_df, x='Age',
    y='Count',
    color='Gender', 
    barmode='stack',
    labels={
        'Age': 'Возраст',
        'Count': 'Количество',
        'Gender': 'Пол',
    },
    title='Отток клиентов по возрасту')

    # Таблица топ-5 клиентов
    top_customers_df = filtered_df.groupby(['Customer ID', 'Customer Name'])['Total Purchase Amount'].sum().reset_index()
    top_customers_df = top_customers_df.sort_values(by='Total Purchase Amount', ascending=False).head(5)

    table_header_Purchase = [
        html.Thead(html.Tr([html.Th("Имя покупателя"), html.Th("Общая сумма покупок")]))
    ]
    table_body_Purchase = [
        html.Tbody([
            html.Tr([html.Td(row['Customer Name']), html.Td(f"{row['Total Purchase Amount']:.2f}")])
            for _, row in top_customers_df.iterrows()
        ])
    ]

    # Таблица с топ-5 клиентов по возвратам
    returns_by_customer = filtered_df.groupby('Customer ID')['Returns'].sum().reset_index()
    top_5_returns = returns_by_customer.sort_values(by='Returns', ascending=False).head(5)
    top_5_returns = pd.merge(top_5_returns, df[['Customer ID', 'Customer Name']].drop_duplicates(), on='Customer ID')

    table_header_Returns = [html.Thead(html.Tr([html.Th("Имя покупателя"), html.Th("Количество возвратов")]))]
    rows = [html.Tr([html.Td(row['Customer Name']), html.Td(row['Returns'])]) for index, row in top_5_returns.iterrows()]
    table_body_Returns = [html.Tbody(rows)]


    return age_bar_chart, gender_pie_chart, churn_bar_chart, table_header_Purchase + table_body_Purchase, table_header_Returns + table_body_Returns
