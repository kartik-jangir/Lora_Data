from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pyperclip
import time
import sys
import os
import requests
from datetime import datetime as dt
from datetime import timedelta

import pandas as pd
import plotly.graph_objects as go
from dash import dcc

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : '/Users/kartikjangir/Desktop/Invest_Rough/SO_Bot'}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--headless")

def update_data():
    s = Service('/Users/kartikjangir/Desktop/Invest_Rough/PN_Whatsapp/Driver/chromedriver')
    browser = webdriver.Chrome( service = s, options=chrome_options)
    browser.maximize_window()

    browser.get('http://trac.suveechi.com/survey.php')
    username_input = WebDriverWait(browser, 500).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="div_refresh"]/table/tbody/tr[1]/th[1]'))
    )
    username_input = WebDriverWait(browser, 500).until(
        EC.presence_of_element_located((By.XPATH, '/html/body'))
    )
    time.sleep(1)
    username_input.send_keys(Keys.COMMAND, 'a')
    time.sleep(1)
    username_input.send_keys(Keys.COMMAND, 'c')
    time.sleep(1)
    df = pd.read_clipboard()

    df.to_csv('lora_data.csv', index = False)
    latest_time = dt.today().strftime('%d %b-%y %I:%M %p')
    print('Done', 'Last updated on {}'.format(latest_time))
    return None
    # return 'Last updated on {}'.format(latest_time)

def graph_maker(time_period):

    df = pd.read_csv('lora_data.csv')
    df['Time'] = df['Time'].apply(lambda x: dt.strptime(x, '%d-%m-%Y %H:%M:%S'))

    start_date=dt.today().replace(hour = 0, minute = 0, second = 0)+timedelta(days=1)
    if time_period == 1:
        minus_days=timedelta(days=1)
        df = df[df['Time'].between((start_date - minus_days), start_date)]
    elif time_period == 2:
        minus_days=timedelta(days=7)
        df = df[df['Time'].between((start_date - minus_days), start_date)]
    elif time_period == 3:
        df = df

    node_name_map = { 'LT2222_1' : 'pH (IN)', 'LT2222_3' : 'pH (OUT)', 'LT2222-3' : 'pH (OUT)',
                      'LT2222_16' : 'Flow (IN)', 'LT2222_11' : 'Filter Pressur (IN)' }

    df['Node Name'] = df['Node Name'].map(node_name_map)
    node_data_ph_in = df[df['Node Name'] == 'pH (IN)']
    node_data_ph_out = df[df['Node Name'] == 'pH (OUT)']
    node_data_flow_in = df[df['Node Name'] == 'Flow (IN)']
    node_data_pressure_in = df[df['Node Name'] == 'Filter Pressur (IN)']
    #ph
    data_phIn = go.Scatter(x = node_data_ph_in['Time'], y = node_data_ph_in['Current (4-20mA)'], name = 'ph(IN)', mode='lines+markers')
    data_phOut = go.Scatter(x = node_data_ph_out['Time'], y = node_data_ph_out['Current (4-20mA)'], name = 'ph(OUT)', mode='lines+markers')
    fig_ph = go.Figure(data = [data_phIn, data_phOut])
    fig_ph.update_layout(
         title_text='pH',
         # plot_bgcolor='#fff',
         font=dict(size=10),
         # showlegend=False,
         hovermode="x unified"
    )
    graph_ph = dcc.Graph( id= 'ph_graph', figure=fig_ph,style=dict(width='auto',height='auto'),
            config={"displayModeBar": False, "showTips": False}
            )
    #Flow
    data_flow_in = go.Scatter(x = node_data_flow_in['Time'], y = node_data_flow_in['Current (4-20mA)'], name = 'Flow(IN)', mode='lines+markers')
    fig_flow_in = go.Figure(data = [data_flow_in])
    fig_flow_in.update_layout(
         title_text='Flow(IN)',
         # plot_bgcolor='#fff',
         font=dict(size=10),
         # showlegend=False,
         hovermode="x unified"
    )
    graph_flow_in = dcc.Graph( id= 'flow_in_graph', figure=fig_flow_in,style=dict(width='auto',height='auto'),
            config={"displayModeBar": False, "showTips": False}
            )
    #Filter pressure
    data_pressure_in = go.Scatter(x = node_data_pressure_in['Time'],
                            y = node_data_pressure_in['Current (4-20mA)'],
                            name = 'Filter Pressure(IN)',
                            mode='lines+markers')
    fig_pressure_in = go.Figure(data = [data_pressure_in])
    fig_pressure_in.update_layout(
         title_text='Filter Pressure(IN)',
         # plot_bgcolor='#fff',
         font=dict(size=10),
         # showlegend=False,
         hovermode="x unified"
    )
    graph_pressure_in = dcc.Graph( id= 'pressure_in', figure=fig_pressure_in, style=dict(width='auto',height='auto'),
            config={"displayModeBar": False, "showTips": False}
            )
    return graph_ph, graph_flow_in, graph_pressure_in
