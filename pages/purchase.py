from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data import df

layout = dbc.Container([
    html.H1("Анализ продуктов и покупок", className='text-center my-4'),

    # Селекторы в одну строку
    dbc.Row([
        dbc.Col([
            html.Label("Выберите диапазон дат:", className='d-block'),
            dcc.DatePickerRange(
                id='date-picker-range-product',
                start_date=df['Purchase Date'].min(),
                end_date=df['Purchase Date'].max(),
                display_format='YYYY-MM-DD',
                className='d-block'
            ),
        ], width=4, className='me-3'), 

        dbc.Col([
            html.Label("Категория продукта:", className='d-block'),
            dcc.Dropdown(
                id='product-category-dropdown',
                options=[
                    {'label': 'Книги', 'value': 'Книги'},
                    {'label': 'Электроника', 'value': 'Электроника'},
                    {'label': 'Дом', 'value': 'Дом'},
                    {'label': 'Одежда', 'value': 'Одежда'}
                ],
                multi=True,
                placeholder="Select Category",
                className='d-block'
            ),
        ], width=4)
    ], className='mb-3 g-0'),  

    # Графики и таблица
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-bar-chart'), width=5, className='mr-3', ),
        dbc.Col(dcc.Graph(id='profit-bar-chart'), width=5, className='mr-3'),
        dbc.Col(dcc.Graph(id='payment-method-pie-chart'), width=5, className='mr-3'),
        dbc.Col(dcc.Graph(id='scatter-plot'), width=6, className='mr-3'),        
    ], className='mr-3 g-0')
], fluid=True) 

# Коллбэк для обновления круговой диаграммы на основе селекторов
@callback(
    Output('payment-method-pie-chart', 'figure'),
    [Input('date-picker-range-product', 'start_date'),
     Input('date-picker-range-product', 'end_date'),
     Input('product-category-dropdown', 'value')]
)
def update_pie_chart(start_date, end_date, selected_categories):
    # Фильтрация данных
    filtered_df = df[
        (df['Purchase Date'] >= start_date) &
        (df['Purchase Date'] <= end_date)
    ]
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Product Category'].isin(selected_categories)]

    # Круговая диаграмма анализа метода оплаты
    payment_method_count = filtered_df['Payment Method'].value_counts(normalize=True).reset_index()
    payment_method_count.columns = ['Payment Method', 'Percentage']
    payment_method_pie_chart = px.pie(payment_method_count, names='Payment Method', values='Percentage', title='Анализ метода оплаты (%)', hole=0.3)

    return payment_method_pie_chart

# Коллбэк для обновления столбчатых диаграмм и scatter plot на основе селекторов
@callback(
    [Output('sales-bar-chart', 'figure'),
     Output('profit-bar-chart', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('date-picker-range-product', 'start_date'),
     Input('date-picker-range-product', 'end_date'),
     Input('product-category-dropdown', 'value')]
)
def update_graphs_and_table(start_date, end_date, selected_categories):
    # Фильтрация данных
    filtered_df = df[
        (df['Purchase Date'] >= start_date) &
        (df['Purchase Date'] <= end_date)
    ]

    if selected_categories:
        filtered_df = filtered_df[filtered_df['Product Category'].isin(selected_categories)]

    # Столбчатая диаграмма продаж по категориям продуктов
    sales_by_category = filtered_df.groupby('Product Category').size().reset_index(name='Count')
    sales_bar_chart = px.bar(sales_by_category, x='Product Category',
    y='Count', 
    color='Product Category',
    labels={
    'Product Category': 'Категория продукта',
    'Count': 'Количество',
    }, 
    title='Количество продаж по категориям продуктов')

    # Столбчатая диаграмма прибыли по категориям продуктов
    profit_by_category = filtered_df.groupby('Product Category')['Total Purchase Amount'].sum().reset_index()
    profit_bar_chart = px.bar(profit_by_category, 
    x='Product Category', 
    y='Total Purchase Amount', 
    color='Product Category',
    labels={
    'Product Category': 'Категория продукта',
    'Total Purchase Amount': 'Прибыль',
    },  
    title='Прибыль по категориям продуктов')

    # График рассеивания средней стоимости покупок и количества покупок по категориям продуктов
    avg_purchase_amount = filtered_df.groupby('Product Category')['Total Purchase Amount'].mean().reset_index()
    purchase_count = filtered_df.groupby('Product Category').size().reset_index(name='Purchase Count')
    scatter_data = pd.merge(avg_purchase_amount, purchase_count, on='Product Category')
    scatter_plot = px.scatter(scatter_data, 
    x='Purchase Count', 
    y='Total Purchase Amount', 
    color='Product Category', 
    size='Purchase Count',
    labels={
    'Total Purchase Amount': 'Прибыль',
    'Purchase Count': 'Количество покупок',
    },   
    title='Соотношение средней стоимости и количества покупок')

    return sales_bar_chart, profit_bar_chart, scatter_plot
