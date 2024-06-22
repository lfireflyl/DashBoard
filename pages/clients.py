from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
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
        ], id='left-align', width=4, className='me-3'),  # Добавлен отступ справа

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
                className='d-block',
                style={'width': '150px'}  # Установлена фиксированная ширина
            ),
        ], id='center-align', width='auto', className='me-3'),  # Добавлен отступ справа и авто ширина

        dbc.Col([
            html.Label("Введите возраст:", className='d-block'),
            dcc.Input(
                id='age-input',
                type='number',
                placeholder='Введите возраст',
                className='d-block'
            ),
        ], id='right-align', width=4)
    ], className='mb-3 align-items-end g-0'),  # выравнивание колонок по нижнему краю

    # Столбчатая диаграмма по возрасту клиентов
    dbc.Row([
        dbc.Col(dcc.Graph(id='age-bar-chart'), width=12, className='p-0')
    ], className='mt-3 g-0'),

    # Круговая диаграмма с распределением клиентов по полу и столбчатая диаграмма по оттоку клиента
    dbc.Row([
        dbc.Col(dcc.Graph(id='gender-pie-chart'), width=6, className='p-0'),
        dbc.Col(dcc.Graph(id='churn-bar-chart'), width=6, className='p-0')
    ], className='mt-3 g-0')
], fluid=True)  # установлено полную ширину контейнера

# Коллбэк для обновления графиков на основе селекторов
@callback(
    [Output('age-bar-chart', 'figure'),
     Output('gender-pie-chart', 'figure'),
     Output('churn-bar-chart', 'figure')],
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
    age_gender_df = df.groupby(['Age', 'Gender']).size().reset_index(name='Count')  # Используем неотфильтрованные данные для диаграммы по возрасту
    age_bar_chart = px.bar(age_gender_df, x='Age', y='Count', color='Gender', barmode='stack', title='Распределение клиентов по возрасту')

    # Круговая диаграмма с распределением клиентов по полу
    gender_count = df['Gender'].value_counts().reset_index()  # Используем неотфильтрованные данные для круговой диаграммы
    gender_count.columns = ['Gender', 'Count']
    gender_pie_chart = px.pie(gender_count, names='Gender', values='Count', title='Распределение клиентов по полу', hole=0.3)

    # Фильтрация данных по возрасту для диаграммы по оттоку клиентов
    if selected_age:
        filtered_df = filtered_df[filtered_df['Age'] == selected_age]

    # Столбчатая диаграмма по оттоку клиентов
    churn_age_df = filtered_df[filtered_df['Churn'] == 1].groupby(['Age', 'Gender']).size().reset_index(name='Count')
    churn_bar_chart = px.bar(churn_age_df, x='Age', y='Count', color='Gender', barmode='stack', title='Отток клиентов по возрасту')

    return age_bar_chart, gender_pie_chart, churn_bar_chart