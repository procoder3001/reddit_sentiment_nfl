import dash
from dash import dcc, html, dash_table, ctx
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from datetime import datetime
from pytz import timezone

import pandas as pd
import os

####### Utility Functions #####################

def get_date():
    tz = timezone('EST')
    d = datetime.now(tz)
    year = d.year
    month = d.strftime("%B")
    day = d.day

    if day in [1,21, 31]:
        suffix = "st"
    elif day in [2,22]:
        suffix = "nd"
    elif day in [3, 23]:
        suffix = "rd"
    else:
        suffix = "th"

    return f"{month} {day}{suffix}, {year}, EST"

def data_in():
    print("Loading in data from GCS...")
    stats_df_uri = "gs://gcf-sources-134756275535-us-central1/nfl_comments_agg_stats.csv"
    data_df = pd.read_csv(stats_df_uri)

    # return data_df
    return data_df.sort_values(by=["sentiment_summary"], ascending = False)

def get_nfl_team_card(position):


    if data_df.iloc[position-1,1] >= 0:
        color = "green"
    else:
        color = "red"

    team = data_df.iloc[position-1,0]
    

    card_icon = {
   
        "textAlign": "left",
        "justifyContent": "left",
        "margin": "auto",
        "max-width":"9em",
        "max-height":"9em",
        "font-size":"4vw"
    }

    card1 = dbc.CardGroup(
    [
        dbc.Card(
            # html.Div(className="col-5 fa fa-list", style=card_icon),
            html.Img(src=fr"assets/nfl_team_logos/{images_dict[team]}.png", style=card_icon, className="col-5 fa fa-list"),
           

        
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H1(f"# {position}", className="card-title",),
                    html.H3(f"{team}", style = {"font-size":"1.7vw"})
                ],
        
            ),
            style={"margin":"auto"}

        ),
  
        
    ],
    className="team mt-4 shadow",
    style={"width":"65%", "textAlign": "center","justifyContent":"center",
    "display": "flex", "margin":"auto", "color":color}
    )

    return card1

def app_layout():

    navbar = dbc.NavbarSimple(
        brand="NFL Reddit Sentiment",
        brand_style = {"font-family": "Lato, -apple-system, sans-serif" , "font-size": "2.8rem", "padding": "0.1rem 0.1rem"},
        brand_href="#",
        color="#87CEEB",
        dark=True,
        id="navbar",
        style={"height": "3rem"},
        expand = True
     
    )

    intro_md = f"""\
        **Today is {today}.**\n
        How do redditors feel about their teams? \n
        I grab around 25 top comments from each nfl team subreddit, perform sentiment analysis, \
        and aggregate scores to get a ranking of nfl teams by reddit sentiment, from relatively\
        most positive sentiment (#1) to least (#32). Data is updated every other day. [See code here.](https://github.com/procoder3001/nfl_reddit_sentiment "my github code")
    """,

    return html.Div([
        navbar,
        # body
        dbc.Container([
            dcc.Markdown(intro_md, 
            style = {"font-family": "Lato, -apple-system, sans-serif", "font-size": "1.5em", "margin-top": "2%", "margin-bottom": "2%"},
            ),
            dbc.Container([
                get_nfl_team_card(position = i) for i in range(1,33)
            ], style={})


        ])

    ])

###############################################

####### App ###################################

external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;1,100&display=swap',
    'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;1,100&family=Roboto+Mono&display=swap'
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])
app.title = "NFL Reddit Sentiment"
server = app.server

data_df = data_in()

today = get_date()

images_dict = {
"49ers":"san-francisco-49ers",
"azcardinals":"arizona-cardinals",
"bengals":"cincinnati-bengals",
"browns":"cleveland-browns",
"buccaneers":"tampa-bay-buccaneers",
"buffalobills":"buffalo-bills",
"chargers":"los-angeles-chargers",
"chibears":"chicago-bears",
"colts":"indianapolis-colts",
"commanders":"washington-commanders",
"cowboys":"dallas-cowboys",
"denverbroncos":"denver-broncos",
"detroitlions":"detroit-lions",
"eagles":"philadelphia-eagles",
"falcons":"atlanta-falcons",
"greenbaypackers":"green-bay-packers",
"jaguars":"jacksonville-jaguars",
"kansascitychiefs":"kansas-city-chiefs",
"losangelesrams":"los-angeles-rams",
"miamidolphins":"miami-dolphins",
"minnesotavikings":"minnesota-vikings",
"nygiants":"new-york-giants",
"nyjets":"new-york-jets",
"panthers":"carolina-panthers",
"patriots":"new-england-patriots",
"raiders":"las-vegas-raiders",
"ravens":"baltimore-ravens",
"saints":"new-orleans-saints",
"seahawks":"seattle-seahawks",
"steelers":"pittsburgh-steelers",
"tennesseetitans":"tennessee-titans",
"texans":"houston-texans",
}

app.layout = app_layout
###############################################

####### Callbacks #############################

###############################################

if __name__=='__main__':
    # app.run_server(debug=True, port=8005)
    # host = "0.0.0.0"
    app.run_server(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))