import copy
import numpy as np
import pandas as pd
import plotly as po
import plotly.express as px
import dash
import requests
import sodapy
from sodapy import Socrata
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Display version for imported libraries
def library_version():
    print(f"numpy version: {np.__version__}\n"
          f"pandas version: {pd.__version__}\n"
          f"plotly version: {po.__version__}\n"
          f"dash version: {dash.__version__}\n"
          f"request version: {requests.__version__}\n"
          f"sodapy version: {sodapy.__version__}")

#JSON API data https://data.edmonton.ca/resource/q7d6-ambg.json

#LANG_CENSUS_DF = pd.read_csv("source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv")
#CRIME_OCCUR_DF = pd.read_csv("source-files/Occurrences_Last_90_Days.csv")
#PRPRT_ASSES_DF = pd.read_csv("source-files/Property_Assessment_Data__Current_Calendar_Year_.csv")

WARDS_2021 = {
     1: "Nakota Isga Ward",
     2: "Anirniq Ward",
     3: "tastawiyiniwak Ward",
     4: "Dene Ward",
     5: "sipiwiyiniwak Ward",
     6: "O-day'min Ward",
     7: "Métis Ward",
     8: "Ipiihkoohkanipiaohtsi Ward",
     9: "pihêsiwin Ward",
    10: "papastew Ward",
    11: "Karhiio Ward",
    12: "Sspomitapi Ward"
}

NEIGHBOURHOOD_WARD_1  = ['GLENWOOD',
                     'WINTERBURN INDUSTRIAL AREA WEST',
                     'LA PERLE',
                     'WEST JASPER PLACE',
                     'WINTERBURN INDUSTRIAL AREA EAST',
                     'BRITANNIA YOUNGSTOWN',
                     'ALDERGROVE',
                     'SECORD',
                     'HAWIN PARK ESTATE INDUSTRIAL',
                     'STONE INDUSTRIAL',
                     'KINOKAMAU PLAINS AREA',
                         'GLENORA',
                         'CANORA',
                         'EDMISTON INDUSTRIAL',
                         'HAWKS RIDGE',
                         'LEWIS FARMS INDUSTRIAL',
                         'KINGLET GARDENS',
                         'SUDER GREENS',
                         'ROSENTHAL',
                         'MORIN INDUSTRIAL',
                         'GROVENOR',
                         'WILSON INDUSTRIAL',
                         'YOUNGSTOWN INDUSTRIAL',
                         'ANTHONY HENDAY',
                         'MCNAMARA INDUSTRIAL',
                         'ALBERTA PARK INDUSTRIAL',
                         'STARLING',
                         'ANTHONY HENDAY BIG LAKE',
                         'PLACE LARUE',
                         'PINTAIL LANDING',
                         'RIVER VALLEY GLENORA',
                         'WEBBER GREENS',
                         'TRUMPETER AREA',
                         'WEST SHEFFIELD INDUSTRIAL',
                         'WHITE INDUSTRIAL',
                         'ARMSTRONG INDUSTRIAL',
                         'SHEFFIELD INDUSTRIAL',
                         'SUNWAPTA INDUSTRIAL',
                         'STEWART GREENS',
                         'POTTER GREENS',
                         'WESTVIEW VILLAGE',
                         'MCQUEEN',
                         'BELMEAD',
                         'MAYFIELD',
                         'HIGH PARK',
                         'CRESTWOOD',
                         'NORTH GLENORA',
                         'CARLETON SQUARE INDUSTRIAL',
                         'NORWESTER INDUSTRIAL',
                         'TERRA LOSA',
                         'BRECKENRIDGE GREENS',
                         'POUNDMAKER INDUSTRIAL', ]
NEIGHBOURHOOD_WARD_2  = ['MISTATIM INDUSTRIAL',
                     'DUNLUCE',
                     'CARLTON',
                     'PRINCE CHARLES',
                     'MITCHELL INDUSTRIAL',
                     'CARLISLE',
                     'ANTHONY HENDAY MISTATIM',
                     'INGLEWOOD',
                     'RAMPART INDUSTRIAL',
                     'PEMBINA',
                     'GAGNON ESTATE INDUSTRIAL',
                         'HIGH PARK INDUSTRIAL',
                         'CALDER',
                         'DOVERCOURT',
                         'CANOSSA',
                         'CUMBERLAND',
                         'LAUDERDALE',
                         'ANTHONY HENDAY RAMPART',
                         'KENSINGTON',
                         'RAPPERSWILL',
                         'ATHLONE',
                         'HUFF BREMNER ESTATE INDUSTRIAL',
                         'HAGMANN ESTATE INDUSTRIAL',
                         'BROWN INDUSTRIAL',
                         'ROSSLYN',
                         'GOODRIDGE CORNERS',
                         'BARANOW',
                         'YELLOWHEAD CORRIDOR WEST',
                         'BONAVENTURE INDUSTRIAL',
                         'GARSIDE INDUSTRIAL',
                         'WOODCROFT',
                         'SHERBROOKE',
                         'DOMINION INDUSTRIAL',
                         'WELLINGTON',
                         'MCARTHUR INDUSTRIAL',
                         'OXFORD',
                         'CAERNARVON',
                         'ALBANY',
                         'GRIESBACH',
                         'HUDSON', ]
NEIGHBOURHOOD_WARD_3  = ['BELLE RIVE',
                     'LAGO LINDO',
                     'KILKENNY',
                     'BEAUMARIS',
                     'BALWIN',
                     'EVANSDALE',
                     'MAYLIEWAN',
                     'KILLARNEY',
                     'BATURYN',
                     'OZERNA',
                     'EAUX CLAIRES',
                         'ANTHONY HENDAY CASTLEDOWNS',
                         'KILDARE',
                         'LORELEI',
                         'ELSINORE',
                         'NORTHMOUNT',
                         'GLENGARRY',
                         'KLARVATTEN',
                         'ANTHONY HENDAY LAKE DISTRICT',
                         'CRYSTALLINA NERA EAST',
                         'DELWOOD',
                         'CRYSTALLINA NERA WEST',
                         'CHAMBERY',
                         'SCHONSEE', ]
NEIGHBOURHOOD_WARD_4  = ['MATT BERRY',
                     'FRASER',
                     'RURAL NORTH EAST HORSE HILL',
                     'HAIRSINE',
                     'CASSELMAN',
                     'CLOVER BAR AREA',
                     'KIRKNESS',
                     'EDMONTON ENERGY AND TECHNOLOGY PARK',
                     'RURAL NORTH EAST SOUTH STURGEON',
                     'MARQUIS',
                     'BELVEDERE',
                         'BANNERMAN',
                         'HOMESTEADER',
                         'KENNEDALE INDUSTRIAL',
                         'EBBERS',
                         'GORMAN',
                         'BRINTNELL',
                         'MCLEOD',
                         'EVERGREEN',
                         'YORK',
                         'ANTHONY HENDAY ENERGY PARK',
                         'ANTHONY HENDAY HORSE HILL',
                         'HOLLICK-KENYON',
                         'ANTHONY HENDAY CLAREVIEW',
                         'MCCONACHIE',
                         'OVERLANDERS',
                         'CY BECKER',
                         'CLAREVIEW TOWN CENTRE',
                         'KERNOHAN',
                         'RIVER VALLEY HERMITAGE',
                         'BELMONT',
                         'CANON RIDGE',
                         'SIFTON PARK',
                         'MILLER', ]
NEIGHBOURHOOD_WARD_5  = ['RIO TERRACE',
                     'JASPER PARK',
                     'WEST MEADOWLARK PARK',
                     'RIVER VALLEY OLESKIW',
                     'ELMWOOD',
                     'SHERWOOD',
                     'CALLINGWOOD SOUTH',
                     'MEADOWLARK PARK',
                     'LYMBURN',
                     'WESTRIDGE','RIVERVIEW AREA',
                     'THE UPLANDS',
                         'JAMIESON PLACE',
                         'LYNNWOOD',
                         'OLESKIW',
                         'PATRICIA HEIGHTS',
                         'ORMSBY PLACE',
                         'EDGEMONT',
                         'LAURIER HEIGHTS',
                         'SUMMERLEA',
                         'PARKVIEW',
                         'RIVER VALLEY LESSARD NORTH',
                         "RIVER'S EDGE",
                         'WEDGEWOOD HEIGHTS',
                         'GLASTONBURY',
                         'RIVER VALLEY CAMERON',
                         'DECHENE',
                         'RIVER VALLEY LAURIER',
                         'STILLWATER',
                         'GARIEPY',
                         'CAMERON HEIGHTS',
                         'DONSDALE',
                         'ANTHONY HENDAY SOUTH WEST',
                         'GRANVILLE',
                         'THE HAMPTONS',
                         'QUESNELL HEIGHTS',
                         'THORNCLIFF',
                         'CALLINGWOOD NORTH',
                         'RIVER VALLEY CAPITOL HILL', ]
NEIGHBOURHOOD_WARD_6  = ['OLIVER',
                     'RIVERDALE',
                     'CENTRAL MCDOUGALL',
                     'QUEEN MARY PARK',
                     'SPRUCE AVENUE',
                     'DOWNTOWN',
                     'BOYLE STREET',
                     'RIVER VALLEY VICTORIA',
                     'BLATCHFORD AREA',
                     'MCCAULEY',
                     'WESTMOUNT',
                         'WESTWOOD',
                         'ROSSDALE',
                         'PRINCE RUPERT',
                         'RIVER VALLEY WALTERDALE', ]
NEIGHBOURHOOD_WARD_7  = ['CROMDALE',
                        'EASTGATE BUSINESS PARK',
                        'WEIR INDUSTRIAL',
                        'MONTROSE',
                        'TERRACE HEIGHTS',
                        'EASTWOOD',
                        'ELMWOOD PARK',
                        'INDUSTRIAL HEIGHTS',
                        'RUNDLE HEIGHTS',
                        'KING EDWARD PARK',
                        'KENILWORTH',
                        'MORRIS INDUSTRIAL',
                        'RIVER VALLEY HIGHLANDS',
                        'DAVIES INDUSTRIAL WEST',
                        'NEWTON',
                        'ALBERTA AVENUE',
                        'HIGHLANDS',
                        'FOREST HEIGHTS',
                        'BONNIE DOON',
                        'IDYLWYLDE',
                        'OTTEWELL',
                        'DAVIES INDUSTRIAL EAST',
                        'BEVERLY HEIGHTS',
                        'AVONMORE',
                        'GOLD BAR',
                        'CLOVERDALE',
                        'RIVER VALLEY GOLD BAR',
                        'STRATHEARN',
                        'BEACON HEIGHTS',
                        'BERGMAN',
                        'RIVER VALLEY RIVERSIDE',
                        'RIVER VALLEY KINNAIRD',
                        'YELLOWHEAD CORRIDOR EAST',
                        'DELTON',
                        'CAPILANO',
                        'BELLEVUE',
                        'GIRARD INDUSTRIAL',
                        'PARKDALE',
                        'VIRGINIA PARK',
                        'GAINER INDUSTRIAL',
                        'FULTON PLACE',
                        'EDMONTON NORTHLANDS',
                        'HOLYROOD',
                        'LAMBTON INDUSTRIAL',
                        'ABBOTTSFIELD',
                        'RIVER VALLEY RUNDLE', ]
NEIGHBOURHOOD_WARD_8  = ['BEARSPAW',
                        'KEHEEWIN',
                        'SWEET GRASS',
                        'SKYRATTLER',
                        'BLUE QUILL',
                        'RICHFORD',
                        'ERMINESKIN',
                        'BLACKBURNE',
                        'GLENRIDDING RAVINE',
                        'HERITAGE VALLEY TOWN CENTRE AREA',
                        'CASHMAN',
                        'CHAPPELLE AREA',
                        'STEINHAUER',
                        'HAYS RIDGE AREA',
                        'TWIN BROOKS',
                        'ANTHONY HENDAY SOUTH BLACKBURNE',
                        'HERITAGE VALLEY AREA',
                        'CAVANAGH',
                        'DESROCHERS AREA',
                        'GRAYDON HILL',
                        'ALLARD',
                        'BLUE QUILL ESTATES',
                        'BLACKMUD CREEK RAVINE',
                        'MACEWAN',
                        'ANTHONY HENDAY SOUTH',
                        'RUTHERFORD',
                        'BLACKMUD CREEK',
                        'CALLAGHAN',
                        'PAISLEY',
                        'EDMONTON SOUTH CENTRAL', ]
NEIGHBOURHOOD_WARD_9  = ['RAMSAY HEIGHTS',
                        'HENDERSON ESTATES',
                        'RHATIGAN RIDGE',
                        'WINDERMERE',
                        'WINDERMERE AREA',
                        'KESWICK',
                        'RIVER VALLEY TERWILLEGAR',
                        'RIVER VALLEY WINDERMERE',
                        'SOUTH TERWILLEGAR',
                        'HADDOW',
                        'CARTER CREST',
                        'WHITEMUD CREEK RAVINE TWIN BROOKS',
                        'GLENRIDDING HEIGHTS',
                        'AMBLESIDE',
                        'ANTHONY HENDAY TERWILLEGAR',
                        'OGILVIE RIDGE',
                        'BULYEA HEIGHTS',
                        'BRANDER GARDENS',
                        'FALCONER HEIGHTS',
                        'MACTAGGART',
                        'RIVER VALLEY FORT EDMONTON',
                        'LEGER',
                        'TERWILLEGAR TOWNE',
                        'HODGSON',
                        'MAGRATH HEIGHTS',
                        'EDMONTON SOUTH WEST', ]
NEIGHBOURHOOD_WARD_10 = ['STRATHCONA',
                        'GARNEAU',
                        'EMPIRE PARK',
                        'QUEEN ALEXANDRA',
                        'RITCHIE',
                        'STRATHCONA JUNCTION',
                        'GRANDVIEW HEIGHTS',
                        'CORONET INDUSTRIAL',
                        'LANSDOWNE',
                        'GREENFIELD',
                        'MILL CREEK RAVINE NORTH',
                        'ALLENDALE',
                        'WINDSOR PARK',
                        'CPR IRVINE',
                        'HAZELDEAN',
                        'UNIVERSITY OF ALBERTA',
                        'MALMO PLAINS',
                        'DUGGAN',
                        'RIDEAU PARK',
                        'PLEASANTVIEW',
                        'ASPEN GARDENS',
                        'ROYAL GARDENS',
                        'CALGARY TRAIL NORTH',
                        'BELGRAVIA',
                        'MCKERNAN',
                        'PARKALLEN',
                        'CORONET ADDITION INDUSTRIAL',
                        'WHITEMUD CREEK RAVINE SOUTH',
                        'UNIVERSITY OF ALBERTA FARM',
                        'MILL CREEK RAVINE SOUTH',
                        'ROSEDALE INDUSTRIAL',
                        'RIVER VALLEY WHITEMUD',
                        'BROOKSIDE',
                        'LENDRUM PLACE',
                        'WESTBROOK ESTATES',
                        'RIVER VALLEY MAYFAIR',
                        'WHITEMUD CREEK RAVINE NORTH',
                        'ARGYLL', ]
NEIGHBOURHOOD_WARD_11 = ['STRATHCONA INDUSTRIAL PARK',
                        'SAKAW',
                        'ELLERSLIE',
                        'MEYONOHK',
                        'MEYOKUMIN',
                        'HILLVIEW',
                        'KAMEYOSEK',
                        'ROPER INDUSTRIAL',
                        'TIPASKAN',
                        'PAPASCHASE INDUSTRIAL',
                        'ELLERSLIE INDUSTRIAL',
                        'PARSONS INDUSTRIAL',
                        'MCINTYRE INDUSTRIAL',
                        'MATTSON',
                        'ANTHONY HENDAY SOUTH EAST',
                        'EDMONTON RESEARCH AND DEVELOPMENT PARK',
                        'TAWA',
                        'THE ORCHARDS AT ELLERSLIE',
                        'MENISA',
                        'SOUTH EDMONTON COMMON',
                        'CHARLESWORTH',
                        'GREENVIEW',
                        'MILL WOODS PARK',
                        'RICHFIELD',
                        'CALGARY TRAIL SOUTH',
                        'EKOTA',
                        'MICHAELS PARK',
                        'MILL WOODS TOWN CENTRE',
                        'TWEDDLE PLACE',
                        'SATOO',
                        'LEE RIDGE',
                        'SUMMERSIDE',
                        'WALKER',
                        'EDMONTON SOUTH CENTRAL EAST', ]
NEIGHBOURHOOD_WARD_12 = ['SOUTHEAST INDUSTRIAL',
                        'POLLARD MEADOWS',
                        'KINISKI GARDENS',
                        'DALY GROVE',
                        'CRAWFORD PLAINS',
                        'WEINLOS',
                        'MINCHAU',
                        'BISSET',
                        'DECOTEAU',
                        'LARKSPUR',
                        'SILVER BERRY',
                        'MAPLE RIDGE INDUSTRIAL',
                        'ASTER',
                        'DECOTEAU NORTH',
                        'MAPLE',
                        'TAMARACK',
                        'MELTWATER',
                        'LAUREL',
                        'MAPLE RIDGE',
                        'PYLYPOW INDUSTRIAL',
                        'JACKSON HEIGHTS',
                        'WILD ROSE',
                        'EDMONTON SOUTH EAST', ]

def new_ward_neighbourhood_list(var_input):
    try:
        ward_num = int(var_input)
        if type(ward_num) is int:
            if ward_num == 1:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_1)
                return neighbourhood_list
            elif ward_num == 2:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_2)
                return neighbourhood_list
            elif ward_num == 3:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_3)
                return neighbourhood_list
            elif ward_num == 4:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_4)
                return neighbourhood_list
            elif ward_num == 5:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_5)
                return neighbourhood_list
            elif ward_num == 6:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_6)
                return neighbourhood_list
            elif ward_num == 7:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_7)
                return neighbourhood_list
            elif ward_num == 8:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_8)
                return neighbourhood_list
            elif ward_num == 9:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_9)
                return neighbourhood_list
            elif ward_num == 10:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_10)
                return neighbourhood_list
            elif ward_num == 11:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_11)
                return neighbourhood_list
            elif ward_num == 12:
                neighbourhood_list = copy.deepcopy(NEIGHBOURHOOD_WARD_12)
                return neighbourhood_list
            else:
                print("\n")
                #print(f"{ward_num} must be between (1-12)")
    except ValueError:
        print("\n")
        #print(f"{var_input} is of {type(var_input)}\n{type(int)} is required.")

'''Map chart with all the locations of the crime occurrences plotted'''
def read_crime_occurances_mapbox():
        df = pd.read_csv("source-files/Occurrences_Last_90_Days.csv")
        fig = px.scatter_mapbox(df,
                                lon=df['X'],
                                lat=df['Y'],
                                zoom=10,
                                color=df['Occurrence_Category'],
                                width=1200,
                                height=900,
                                title="Crime Occurences - Last 90 Days",
                                center=dict(
                                    lat=53.537667,
                                    lon=-113.496135),
                                labels={'Occurrence_Category': 'Category of Occurrence'},
                                )

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(title_x=0.5)

        fig.show()
def read_property_assessment_box(input):
    ward_num = int(input)
    df = PRPRT_ASSES_DF.query("`Ward`==@WARDS_2021.get(@ward_num)")
    fig = px.box(df,
                 x=df["Neighbourhood"],
                 y=df["Assessed Value"],
                 color=df["Assessment Class 1"],
                 title=f"Assessed value in {WARDS_2021.get(ward_num)}."
                 )
    fig.show()
def read_property_assessment_bar(input):
    ward_num = int(input)
    df = PRPRT_ASSES_DF.query("`Ward`==@WARDS_2021.get(@ward_num)")
    fig = px.bar(
        df,
        x=df["Neighbourhood"],
        y=df["Assessed Value"],
        color=df["Assessment Class 1"],
        barmode="relative",
        height=700,
        title=f"Assessed value in {WARDS_2021.get(ward_num)}.",
    )
    fig.show()
def read_property_assessment_mapbox(input):
    ward_num = int(input)
    df = PRPRT_ASSES_DF.query("`Ward`==@WARDS_2021.get(@ward_num)")
    fig = px.scatter_mapbox(df,
                            lon=df['Longitude'],
                            lat=df['Latitude'],
                            zoom=11,
                            color=df['Assessment Class 1'],
                            width=1200,
                            height=900,
                            title=f"Assessment Classes in {WARDS_2021.get(ward_num)}",
                            center=dict(
                                lat=53.537667,
                                lon=-113.496135,),
                            )
    fig.update_layout(
        mapbox_style="open-street-map",
        title_x=0.5,
    )
    fig.show()

def property_assessment_data_all_neighbourhoods():
    residential = "RESIDENTIAL"
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 & `Assessment Class 1`==@residential")
    fig = px.box(df,
                 x=df['Neighbourhood'],
                 y=df['Assessed Value'],
                 color=df["Ward"],
                 points=False,
                 title="Assessed values of residential properties in the city of Edmonton.",
                 )
    fig.show()

'''
FIVE Neighbourhoods with highest valued outliers
FIVE Neighbourhoods with highest valued medians
'''
class HoodStats:
    def __init__(self, hood, mean, median, count):
        self.hood = hood
        self.mean = mean
        self.median = median
        self.count = count
    def __repr__(self):
        return '{' + self.hood + ', ' + str(self.mean) + ', ' + str(self.median) + ', ' + str(self.count) + '}'

def get_median_of_each_neighbourhood():
    residential = "RESIDENTIAL"
    normal_neighbourhood = PRPRT_ASSES_DF["Neighbourhood"].unique()
    #print( len(normal_neighbourhood) )
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 & `Assessment Class 1`==@residential")[['Neighbourhood','Assessed Value']]
    unique_neighbourhood = df["Neighbourhood"].unique()
    #print(len(normal_neighbourhood)) #402
    #print(len(unique_neighbourhood)) #345
    '''
    test_hood = df.query("Neighbourhood == @unique_neighbourhood[0]")
    count = test_hood["Assessed Value"]
    median = np.median(test_hood["Assessed Value"])
    mean = np.mean(test_hood["Assessed Value"])
    print(f"{unique_neighbourhood[0]} ==> count:{count}\t\tmedian:{median}\t\tmean:{mean}")
    '''
    hood_list = []
    for hood in unique_neighbourhood:
        temp_df = df.query("Neighbourhood == @hood")
        value_list = temp_df["Assessed Value"]
        mean = np.mean(value_list)
        median = np.median(value_list)
        count = len(value_list)
        hood_list.append( HoodStats(hood, mean, median, count) )

    avg_listings = []
    for lists in hood_list:
        if lists.count >= 50:
            avg_listings.append( lists )

    #print( len(avg_listings) ) #280
    #hlist = sorted(avg_listings, key=lambda x: x.median, reverse=True)
    #llist = sorted(avg_listings, key=lambda x: x.median)
    #print(f"High: {hlist[:5]}")
    #print(f"Low: {llist[:5]}")
    return avg_listings

HIGH = [{"name" : "WINDSOR PARK","mean" : 1136973.8175675676,"median" : 971500.0,"count" : 592},
        {"name" : "WESTBROOK ESTATES","mean" : 1178412.912912913,"median" : 963500.0,"count" : 333},
        {"name" : "RIVERVIEW AREA","mean" : 870414.8148148148,"median" : 812500.0,"count" : 135},]
        #{"name" : "GRANDVIEW HEIGHTS","mean" : 868951.4435695538,"median" : 809500.0,"count" : 381},
        #{"name" : "HAYS RIDGE AREA","mean" : 721913.7931034482,"median" : 761500.0,"count" : 406}]
LOW = [{"name" : "RIVER VALLEY HERMITAGE","mean" : 75950.79365079365,"median" : 8000.0,"count" : 315},
       {"name" : "BARANOW","mean" : 97819.09885675857,"median" : 10000.0,"count" : 1487},
       {"name" : "MAPLE RIDGE","mean" : 48548.578199052135,"median" : 34500.0,"count" : 844},]
       #{"name" : "EVERGREEN","mean" : 41790.22556390977,"median" : 36000.0,"count" : 665},
       #{"name" : "WESTVIEW VILLAGE","mean" : 49357.75047258979,"median" : 42500.0,"count" : 1058}]


def display_story_hood_amount_(list):
    colors1 = '#5A8AA2'
    colors2 = '#C8C7C7'
    #colors = ['#C8C7C7',]*8
    #colors[2] = '#31566F'

    intervals = ["Less than 200K", "200K - 300K", "300K - 400K", "400K - 500K",
                 "500K - 600K", "600K - 700K", "700K - 800K", "More than 800K"]
    median = [0, 0, 0, 0,
             0, 0, 0, 0]
    mean = [0, 0, 0, 0,
              0, 0, 0, 0]
    for key in list:
        if (key.median < 200000):
            median[0] += 1
        elif (300000 > key.median >= 200000):
            median[1] += 1
        elif (400000 > key.median >= 300000):
            median[2] += 1
        elif (500000 > key.median >= 400000):
            median[3] += 1
        elif (600000 > key.median >= 500000):
            median[4] += 1
        elif (700000 > key.median >= 600000):
            median[5] += 1
        elif (800000 > key.median >= 700000):
            median[6] += 1
        else:
            median[7] += 1
    for key in list:
        if (key.mean < 200000):
            mean[0] += 1
        elif (300000 > key.mean >= 200000):
            mean[1] += 1
        elif (400000 > key.mean >= 300000):
            mean[2] += 1
        elif (500000 > key.mean >= 400000):
            mean[3] += 1
        elif (600000 > key.mean >= 500000):
            mean[4] += 1
        elif (700000 > key.mean >= 600000):
            mean[5] += 1
        elif (800000 > key.mean >= 700000):
            mean[6] += 1
        else:
            mean[7] += 1

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=median,
        x=intervals,
        text=median,
        name="Median",
        marker_color = colors1,
    ))
    fig.add_trace(go.Bar(
        y=mean,
        x=intervals,
        text=mean,
        name="Mean",
        marker_color = colors2,
    ))
    fig.update_traces(
        textfont_size=24,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_layout(
        hoverdistance=-1,
        hovermode="x unified",
        title="Distribution of Average Assessed Values per Neighbourhood in the City of Edmonton",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=0.85,
            traceorder="normal",
            font=dict(
                size=16,
                family="sans-serif",
                color=colors1,
            ),
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
        ),
        barmode='group',
    )
    fig.show()

def display_story_hood_amount_per_median_pie(list):
    #color_of_unselected = 'rgba(200, 200, 200)'
    #color_of_selected = '#5A8AA2'

    #colors=['#0d0887', '#46039f', '#7201a8', '#9c179e','#bd3786', '#d8576b','#ed7953', '#fb9f3a']
    #colors=['#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921']
    #colors=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921']

    colors = ['#C8C7C7', ] * 8
    colors[2] = '#31566F'

    #colors=['#5a8aa2','#507c93','#466f84','#3d6175','#335566','#2a4858',]
    intervals = ["Less than 200K", "200K - 300K", "300K - 400K", "400K - 500K",
                 "500K - 600K", "600K - 700K", "700K - 800K", "More than 800K"]
    count = [0, 0, 0, 0,
             0, 0, 0, 0]
    for key in list:
        if (key.median < 200000):
            count[0] += 1
        elif (300000 > key.median >= 200000):
            count[1] += 1
        elif (400000 > key.median >= 300000):
            count[2] += 1
        elif (500000 > key.median >= 400000):
            count[3] += 1
        elif (600000 > key.median >= 500000):
            count[4] += 1
        elif (700000 > key.median >= 600000):
            count[5] += 1
        elif (800000 > key.median >= 700000):
            count[6] += 1
        else:
            count[7] += 1

    fig = go.Figure(go.Pie(
        labels=intervals,
        values=count,
        hole=0.5,
        pull=[0.2,0.1,0.6,0.3,
              0.1,0.2,0.1,0.5,]
    ))
    fig.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textposition='inside',
        marker=dict(
            colors=colors
        ),
    )
    fig.update_layout(
        template='plotly_white',
        legend=dict(
            x=1,
            y=1,
        ),
        margin=dict(t=50,b=50,l=25,r=25),
        uniformtext_minsize=12,
        #uniformtext_mode='hide',
    )
    fig.show()


def display_story_histogram_plots():
    colors_high = '#5A8AA2'
    colors_low = '#DB463D'
    #colors_low = '#C8C7C7'
    combined = []
    for lo in LOW:
        combined.append(lo.get("name"))
    for hi in HIGH:
        combined.append(hi.get("name"))

    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@combined")

    df_0l = df.query("`Neighbourhood`==@LOW[0].get('name')")
    df_1l = df.query("`Neighbourhood`==@LOW[1].get('name')")
    df_2l = df.query("`Neighbourhood`==@LOW[2].get('name')")
    df_0h = df.query("`Neighbourhood`==@HIGH[0].get('name')")
    df_1h = df.query("`Neighbourhood`==@HIGH[1].get('name')")
    df_2h = df.query("`Neighbourhood`==@HIGH[2].get('name')")

    fig = make_subplots(rows=3, cols=2)

    trace0l = go.Histogram(x=df_0l["Assessed Value"],name=LOW[0].get('name'),marker_color=colors_low,)
    trace1l = go.Histogram(x=df_1l["Assessed Value"],name=LOW[1].get('name'),marker_color=colors_low,)
    trace2l = go.Histogram(x=df_2l["Assessed Value"],name=LOW[2].get('name'),marker_color=colors_low,)
    trace0h = go.Histogram(x=df_0h["Assessed Value"],name=HIGH[0].get('name'),marker_color=colors_high,)
    trace1h = go.Histogram(x=df_1h["Assessed Value"],name=HIGH[1].get('name'),marker_color=colors_high,)
    trace2h = go.Histogram(x=df_2h["Assessed Value"],name=HIGH[2].get('name'),marker_color=colors_high,)

    fig.append_trace(trace0l, 1, 1)
    fig.append_trace(trace0h, 1, 2)
    fig.append_trace(trace1l, 2, 1)
    fig.append_trace(trace1h, 2, 2)
    fig.append_trace(trace2l, 3, 1)
    fig.append_trace(trace2h, 3, 2)
    fig.show()

def display_story_histogram_overlay():
    colors_high = '#5A8AA2'
    colors_low = '#DB463D'
    #colors_low = '#C8C7C7'
    combined = []
    for lo in LOW:
        combined.append(lo.get("name"))
    for hi in HIGH:
        combined.append(hi.get("name"))

    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@combined")

    df_0l = df.query("`Neighbourhood`==@LOW[0].get('name')")
    df_1l = df.query("`Neighbourhood`==@LOW[1].get('name')")
    df_2l = df.query("`Neighbourhood`==@LOW[2].get('name')")
    df_0h = df.query("`Neighbourhood`==@HIGH[0].get('name')")
    df_1h = df.query("`Neighbourhood`==@HIGH[1].get('name')")
    df_2h = df.query("`Neighbourhood`==@HIGH[2].get('name')")

    fig = go.Figure()
    fig.add_trace( go.Histogram(x=df_0l["Assessed Value"],name=LOW[0].get('name'),marker_color=colors_low,) )
    fig.add_trace( go.Histogram(x=df_1l["Assessed Value"],name=LOW[1].get('name'),marker_color=colors_low,) )
    fig.add_trace( go.Histogram(x=df_2l["Assessed Value"],name=LOW[2].get('name'),marker_color=colors_low,) )
    fig.add_trace( go.Histogram(x=df_0h["Assessed Value"],name=HIGH[0].get('name'),marker_color=colors_high,) )
    fig.add_trace( go.Histogram(x=df_1h["Assessed Value"],name=HIGH[1].get('name'),marker_color=colors_high,) )
    fig.add_trace( go.Histogram(x=df_2h["Assessed Value"],name=HIGH[2].get('name'),marker_color=colors_high,) )

    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)

    fig.show()

def display_story_histogram():
    colors1 = ['#5A8AA2',] *5
    colors2 = ['#C8C7C7',] *5
    colors = colors1 + colors2
    combined = []
    for lo in LOW:
        combined.append(lo.get("name"))
    for hi in HIGH:
        combined.append(hi.get("name"))
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@combined")
    fig = px.histogram(df,
                       y=df["Neighbourhood"],
                       x=df["Assessed Value"],
                       barmode='group',
                       histfunc='avg',
                 )
    fig.show()

def display_story_bar():
    color_high = '#5082C2'
    color_middle = '#986FAF'
    color_low = '#DB463D'
    combined = []
    low = []
    high = []
    for lo in LOW:
        low.append(lo.get("name"))
        combined.append(lo.get("name"))
    for hi in HIGH:
        high.append(hi.get("name"))
        combined.append(hi.get("name"))
    df_l = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@low")
    df_h = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@high")
    lymburn = display_lymburn()
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        y=df_l["Assessed Value"],
        x=df_l["Neighbourhood"],
        histfunc='avg',
        marker_color=color_low,
        texttemplate="%{y:.3s}",
        #texttemplate="%{x}",
        name="Lowest valued Neighbourhoods",
    ))
    fig.add_trace(go.Histogram(
        y=lymburn["Assessed Value"],
        x=lymburn["Neighbourhood"],
        histfunc='avg',
        marker_color=color_middle,
        texttemplate="%{y:.3s}",
        name="My Neighbourhood",
    ))
    fig.add_trace(go.Histogram(
        y=df_h["Assessed Value"],
        x=df_h["Neighbourhood"],
        histfunc='avg',
        marker_color=color_high,
        texttemplate="%{y:.3s}",
        #texttemplate="%{x}",
        name="Highest valued Neighbourhoods",
    ))
    fig.update_traces(
        hovertemplate=None,
        textfont_size=24,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_layout(
        template="plotly_white",
        title="Three of the Most and Least Expensive Neighbourhoods based on the Assessment Value",
        legend=dict(
            yanchor="top",
            y=1.02,
            xanchor="left",
            x=0.01,
            traceorder="normal",
            font=dict(
                size=18,
                family="sans-serif",
            ),
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
        ),
    )
    fig.show()

def display_story_box():
    color_high = '#5082C2'
    color_middle = '#986FAF'
    color_low = '#DB463D'
    combined = []
    low = []
    high = []
    for lo in LOW:
        low.append(lo.get("name"))
        combined.append(lo.get("name"))
    for hi in HIGH:
        high.append(hi.get("name"))
        combined.append(hi.get("name"))
    df_l = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@low")
    df_h = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@high")
    lymburn = display_lymburn()
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df_l["Assessed Value"],
        x=df_l["Neighbourhood"],
        marker_color=color_low,
        name="Lowest valued Neighbourhoods",
    ))
    fig.add_trace(go.Box(
        y=lymburn["Assessed Value"],
        x=lymburn["Neighbourhood"],
        marker_color=color_middle,
        name="My Neighbourhood",
    ))
    fig.add_trace(go.Box(
        y=df_h["Assessed Value"],
        x=df_h["Neighbourhood"],
        marker_color=color_high,
        name="Highest valued Neighbourhoods",
    ))
    fig.update_traces(
        hovertemplate=None,
    )
    fig.update_layout(
        title="Three of the Most and Least Expensive Neighbourhoods based on the Assessment Value",
        template="plotly_white",
        legend=dict(
            yanchor="top",
            y=1.02,
            xanchor="left",
            x=0.01,
            traceorder="normal",
            font=dict(
                size=18,
                family="sans-serif",
            ),
        ),
    )
    fig.show()

def display_multiple_property_class():
    multiple_property_class = PRPRT_ASSES_DF.query("`Assessment Class % 1`<100")
    print(f"\nMultiple Property Class: {len(multiple_property_class)}")

    not_residential = PRPRT_ASSES_DF.query("`Assessment Class 1`!='RESIDENTIAL'")
    print( not_residential["Assessment Class 1"].unique() )
    print(f"None Residential: {len(not_residential)}")

    other_residential = PRPRT_ASSES_DF.query("`Assessment Class 1`=='OTHER RESIDENTIAL'")
    commercial = PRPRT_ASSES_DF.query("`Assessment Class 1`=='COMMERCIAL'")
    farmland = PRPRT_ASSES_DF.query("`Assessment Class 1`=='FARMLAND'")
    print(f"Other Residential: {len(other_residential)}")
    print(f"Commercial: {len(commercial)}")
    print(f"Farmland: {len(farmland)}")

def display_residential_by_ward():
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL'")
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        y=df["Assessed Value"],
        x=df["Ward"],
        histfunc='avg',
    ))
    fig.show()

def display_residential_by_ward_by_neighbourhood():
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL'")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["Assessed Value"],
        x=df["Ward"],
    ))
    fig.show()

def display_lymburn_map():
    #lymburn_id = 4270
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`=='LYMBURN'")
    fig = go.Figure()
    fig.add_trace()
    fig.show()

def display_ranges_map():
    #https://data.edmonton.ca/City-Administration/City-of-Edmonton-Neighbourhoods/65fr-66s6
    print(f"{4+2}")

def display_lymburn():
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                         "`Assessment Class 1`=='RESIDENTIAL' &"
                         "`Neighbourhood`=='LYMBURN'")
    return df

def display_crime_occurences():
    df = CRIME_OCCUR_DF
    #occurrence_category = df['Occurrence_Category'].unique()
    occurrence_category_unique = ['Disorder','Non-Violent','Violent','Traffic','Weapons','Drugs','Other',]
    #print(occurrence_category)

    # display occurrence group & type group per category
    file = open("crime_occurrence_sorting.txt", "w")
    for item in occurrence_category_unique:
        df_oc = df.query("`Occurrence_Category`==@item")
        list_og = df_oc['Occurrence_Group'].unique()
        file.write(f"{'='*30}\n{item}:\n")
        for second_item in list_og:
            df_og = df_oc.query("`Occurrence_Group`==@second_item")
            list_otg = df_og['Occurrence_Type_Group'].unique()
            file.write(f" -> {second_item}:\n\t{list_otg}\n\n")
        file.write("\n")
    file.close()
    print("file closed.")

    #occurrence_group = df['Occurrence_Group'].unique()
    # occurrence_group_unique = ['Mischief/Graffiti','Property','Disputes/Disturbances','Personal Violence','General Disorder','Provincial Statute Violations','Abandoned/Recovered/Seized Vehicles','Criminal Flights/Impaired Operation/Escape Lawful ','Weapons Violations','Drug Violations','Sexual Violations','Counterfeiting/Gaming and Betting','Explosives/Dangerous Goods','Workplace/Labour Violations',]
    #print(occurrence_group)

    #occurrence_type_group = df['Occurrence_Type_Group'].unique()
    # occurrence_type_group_unique = ['Mischief - Property','Break and Enter Commercial','Theft Under $5000','Disturbance','Assault','Trouble with Person','Dispute','Theft Over $5000','Internet Fraud','Intoxicated Person','Recovered Motor Vehicle','Suspicious Person','Break and Enter Residential','Impaired Driving','Trespassing','Weapons Complaint','Fraud - Financial','Theft of Motor Vehicle','Criminal Flight Event','Possession Stolen Property','Weapons Complaint Firearm','Fraud General','Robbery Personal','Suspicious Vehicle','Drugs','Fraud Personal','Indecent Act','Public Mischief','Fire Arson','Property Damage','Abandoned Vehicle','Robbery Commercial','Graffiti','Liquor Act','Homicide','Counterfeit Money','Technology/Internet Crime','Dangerous Condition','Bomb Threat','Workplace Accident',]
    #print(occurrence_type_group)


if __name__ == '__main__':
    # https://colordesigner.io/gradient-generator
    # https://www.edmonton.ca/sites/default/files/public-files/assets/PDF/VIS_Book_1.pdf
    library_version()
    #property_assessment_data_all_neighbourhoods()
    #list_1 = copy.deepcopy( get_median_of_each_neighbourhood() )

    #display_story_hood_amount_per_median_pie(list_1)
    #display_story_histogram_overlay()

    #display_story_hood_amount_(list_1)
    #display_story_bar()
    #display_story_box()

    #display_story_histogram_plots()
    #display_story_histogram()

    #display_multiple_property_class()
    #display_residential_by_ward()
    #display_residential_by_ward_by_neighbourhood()
    #display_lymburn_map()

    display_crime_occurences()