import dash
#import dash_html_components as html
from dash import html 
from dash import dcc 
#import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

engine = create_engine('sqlite:///info/Heathcare.db', echo=False)
session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
Heathcare_cost = Base.classes.Heathcare_cost
Total_heathcost = Base.classes.Total_heathcost
Healthcost = Base.classes.Healthcost

stmt = session.query(Heathcare_cost).statement
df= pd.read_sql_query(stmt, session.bind)
rank = df[['Country','ranking']].sort_values(by='ranking')

st = session.query(Total_heathcost).statement
data = pd.read_sql_query(st, session.bind)
data2 = data.sort_values(by='Health_spending_per_capita', ascending=0)
df2 = data2.head(15)

# stm = session.query(Healthcost).statement
# df2= pd.read_sql_query(stm, session.bind)

NAVBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#003366",
    # "color": "#ffffff",
}

CONTENT_STYLE = {
    "top":0,
    "marginTop":'2rem',
    "marginLeft": "18rem",
    "marginRight": "2rem",
    # "backgroundColor": "#000000",
    # "color": "#33cc00",
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


def nav_bar():
    
    """
    Creates Navigation bar
    """
    navbar = html.Div(
    [
        html.H4("Heathcare vs Life span Dashboard",  className="display-10",style={'textAlign':'center', }),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Portfolio", href="https://sonyamg80.github.io/",  external_link=True, target='_blank'),
                dbc.NavLink("Linkten", href="https://www.linkedin.com/in/sonyagreen", target='_blank', external_link=True)
            ],
            pills=True,
            vertical=True
        ),
    ],
    style=NAVBAR_STYLE,
    )  

    return navbar


app.layout = html.Div([
    dcc.Location(id='url', refresh=False), #this locates this structure to the url
    nav_bar(),
    html.Div(id='page-content',style=CONTENT_STYLE) #we'll use a callback to change the layout of this section 
])

### Layout 1
layout1 = html.Div([
    html.H2("Cost of Health Care vs Life Span"),
    html.Hr(),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                            html.H4('This Dashboard shows Lifespan from birth vs Cost of healthcare per capita'),
                            
                            #create tabs
                            dbc.Tabs(
                                [
                                    #graphs will go here eventually using callbacks
                                    dbc.Tab(label='Lifespan',tab_id='graph1'),
                                    dbc.Tab(label='HealthCare Ranking',tab_id='graph2'),
                                    dbc.Tab(label='HealthCare Cost',tab_id='graph3')
                                ],
                                id="tabs",
                                active_tab='graph1',
                                ),
                            html.Div(id="tab-content",className="p-4")
                            ]
                        ),
                    ],
                    width=11 
                ),
                
                dbc.Col(
                    [
                        html.H4('References '),
                        html.P(dbc.NavLink("Life Expectancy", active=True, href="https://data.oecd.org/healthstat/life-expectancy-at-birth.htm",target='_blank' )),
                        html.P(dbc.NavLink("Spending", active=True, href="https://data.oecd.org/healthres/health-spending.htm",target='_blank' )),
                        html.P(dbc.NavLink("Performance", active=True, href="https://www.who.int/healthinfo/paper30.pdf",target='_blank'))
                    ],
                    width=1
                    
                )
                
            ],
        ), 
    ]),
])

#graph 1
example_graph1 = px.scatter(df, x="average_age", y="Avg_Healthcare_cost", color = "Country" , size = "Avg_Healthcare_cost")

#graph 2
example_graph2 = go.Figure(data=[go.Table(
    header=dict(values=list(rank.columns),
               fill_color='paleturquoise',
               align='left'),
    cells=dict(values= rank.transpose().values.tolist(),
              fill_color='lavender',
              align='left'))
])

example_graph3 = px.scatter(df2, x='Health_spending_per_capita', y='GDP_per_capita', color = 'Country', size='Total_five_year_healthcost_15_19')


@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    
)




def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, and 
    renders the associated graph with the tab name on page 1.
    """
    if active_tab is not None:
        if active_tab == "graph1":
            return dcc.Graph(figure=example_graph1, id='graph')
        elif active_tab == "graph2":
            return dcc.Graph(figure=example_graph2, id='graph')
        elif active_tab == "graph3":
            return dcc.Graph(figure=example_graph3, id='graph')
    return "No tab selected"





@app.callback(Output('page-content', 'children'), #this changes the content
              [Input('url', 'pathname')]) #this listens for the url in use
def display_page(pathname):
    if pathname == '/':
        return layout1
    

    
#Runs the server at http://127.0.0.1:5000/      
if __name__ == '__main__':
     app.run_server(port=8080, dev_tools_ui=True, host= '127.0.0.1',debug=False)

