from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("О проекте", className='text-center my-4'),
    html.P([
        "Этот проект представляет собой приложение Dash, предназначенное для анализа данных клиентов электронной коммерции.",
        html.Br(),
        "Панель включает три основные страницы:",
        html.Ul([
            html.Li("Главная с общей информацией"),
            html.Li("Анализ клиентов"),
            html.Li("Анализ продуктов и покупок.")
        ]),
        "Каждая страница предоставляет интерактивные визуализации для лучшего понимания различных аспектов данных электронной коммерции."
    ], className='lead'),
    
    html.H3("Структура проекта", className='mt-4'),
    html.Ul([
        html.Li("data.py: Содержит датасет df, используемый в приложении."),
        html.Li("app.py: Основной файл приложения Dash."),
        html.Li("pages/: Каталог, содержащий файлы с определениями страниц (home.py, clients.py, purchase.py, about.py).")
    ]),
    
    html.H3("Описание каждой страницы", className='mt-4'),
    html.H4("Главная страница (home.py)"),
    html.P([
        "На этой странице представлена общая информация о клиентах, включающая следующие компоненты:"
    ]),
    html.Ul([
        html.Li("Селекторы:"),
        html.Ul([
            html.Li("Диапазон дат"),
            html.Li("Пол"),
            html.Li("Возраст")
        ]),
        html.Li("Индикаторы:"),
        html.Ul([
            html.Li("Общее количество клиентов"),
            html.Li("Выручка"),
            html.Li("Отток клиентов")
        ]),
        html.Li("Графики:"),
        html.Ul([
            html.Li("Линейный график выручки по дням"),
            html.Li("Круговая диаграмма процента возвратов")
        ])
    ]),
    
    html.H4("Анализ клиентов (clients.py)"),
    html.P([
        "На этой странице представлен анализ клиентов по различным параметрам:"
    ]),
    html.Ul([
        html.Li("Селекторы:"),
        html.Ul([
            html.Li("Диапазон дат"),
            html.Li("Пол"),
            html.Li("Возраст")
        ]),
        html.Li("Графики:"),
        html.Ul([
            html.Li("Столбчатая диаграмма распределения клиентов по возрасту"),
            html.Li("Круговая диаграмма распределения клиентов по полу"),
            html.Li("Столбчатая диаграмма оттока клиентов по возрасту")
        ]),
        html.Li("Таблицы:"),
        html.Ul([
            html.Li("Топ-5 клиентов по общему объёму покупок"),
            html.Li("Топ-5 клиентов по возвратам")
        ])
    ]),
    
    html.H4("Анализ продуктов и покупок (purchase.py)"),
    html.P([
        "На этой странице представлен анализ продуктов и покупок:"
    ]),
    html.Ul([
        html.Li("Селекторы:"),
        html.Ul([
            html.Li("Диапазон дат"),
            html.Li("Категория продукта")
        ]),
        html.Li("Графики:"),
        html.Ul([
            html.Li("Столбчатая диаграмма количества продаж по категориям продуктов"),
            html.Li("Столбчатая диаграмма прибыли по категориям продуктов"),
            html.Li("Круговая диаграмма анализа метода оплаты"),
            html.Li("График рассеивания соотношения средней стоимости и количества покупок по категориям продуктов")
        ])
    ]),
], fluid=True)
