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

LANG_CENSUS_DF = pd.read_csv("source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv")
#CRIME_OCCUR_DF = pd.read_csv("source-files/Occurrences_Last_90_Days.csv")
#PRPRT_ASSES_DF = pd.read_csv("source-files/Property_Assessment_Data_2022.csv")
PRPRT_ASSES_DF = pd.read_csv("source-files/Property_Assessment_Data__Current_Calendar_Year_.csv")

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
            avg_listings.append(lists)

    #print( len(avg_listings) )
    hlist = sorted(avg_listings, key=lambda x: x.median, reverse=True)
    llist = sorted(avg_listings, key=lambda x: x.median)
    print(f"High: {hlist[:5]}")
    print(f"Low: {llist[:5]}")
    #return avg_listings

HIGH = [{"name" : "WINDSOR PARK","mean" : 1136973.8175675676,"median" : 971500.0,"count" : 592},
        {"name" : "WESTBROOK ESTATES","mean" : 1178412.912912913,"median" : 963500.0,"count" : 333},
        {"name" : "RIVERVIEW AREA","mean" : 870414.8148148148,"median" : 812500.0,"count" : 135},
        {"name" : "GRANDVIEW HEIGHTS","mean" : 868951.4435695538,"median" : 809500.0,"count" : 381},
        {"name" : "HAYS RIDGE AREA","mean" : 721913.7931034482,"median" : 761500.0,"count" : 406}]

LOW = [{"name" : "RIVER VALLEY HERMITAGE","mean" : 75950.79365079365,"median" : 8000.0,"count" : 315},
       {"name" : "BARANOW","mean" : 97819.09885675857,"median" : 10000.0,"count" : 1487},
       {"name" : "MAPLE RIDGE","mean" : 48548.578199052135,"median" : 34500.0,"count" : 844},
       {"name" : "EVERGREEN","mean" : 41790.22556390977,"median" : 36000.0,"count" : 665},
       {"name" : "WESTVIEW VILLAGE","mean" : 49357.75047258979,"median" : 42500.0,"count" : 1058}]


def display_story_box():
    combined = []
    for lo in LOW:
        combined.append(lo.get("name"))
    for hi in HIGH:
        combined.append(hi.get("name"))
    df = PRPRT_ASSES_DF.query("`Assessment Class % 1`==100 &"
                              "`Assessment Class 1`=='RESIDENTIAL' &"
                              "`Neighbourhood`==@combined")
    fig = px.box(df,
                 y=df["Neighbourhood"],
                 x=df["Assessed Value"],
                 points=False,
                 )
    fig.show()

def display_story_histogram():
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

if __name__ == '__main__':
    library_version()
    #property_assessment_data_all_neighbourhoods()
    #get_median_of_each_neighbourhood()

    display_story_box()
    display_story_histogram()