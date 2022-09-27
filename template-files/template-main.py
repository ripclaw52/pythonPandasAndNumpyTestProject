import numpy as np
import pandas as pd
import plotly as po
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Display version for imported libraries
def library_version():
    print(f"numpy version: {np.__version__}\n"
          f"pandas version: {pd.__version__}\n"
          f"plotly version: {po.__version__}")

# TEMPERATURE_CHANGE data csv file as dataframe
clm_dataframe = pd.read_csv("../source-files/CLIMATEDATA.csv")
# GREENHOUSE-GAS data csv file as dataframe
ghg_dataframe = pd.read_csv("../source-files/GREENHOUSEGASDATA.csv")

# climate data base lists
df_country_list = clm_dataframe['country'].unique() # 247 unique countries
df_year_list = clm_dataframe['year'].unique() # 60 unique years
df_months_list = clm_dataframe['months'].unique() # 17 unique months (12 standard, 4 seasons, 1 meteorological year)

# climate data; limited to meteorological month with random country as line graph
def climate_data_random_single_country_in_metereological_month_over_year_as_line():
    random_country = np.random.randint((len(df_country_list) - 1), size=1)[0]
    np_country_select = df_country_list[random_country]
    df = clm_dataframe.query("`country` == @np_country_select and `months_code` == 7020")
    fig = px.line(df, x="year", y="value", title=f"Temperature change over time in {np_country_select}")
    fig.show()

# climate data; limited to meteorological month with random country as bar graph
def climate_data_random_single_country_in_metereological_month_over_year_as_bar():
    random_country = np.random.randint((len(df_country_list) - 1), size=1)[0]
    np_country_select = df_country_list[random_country]
    df = clm_dataframe.query("`country` == @np_country_select and `months_code` == 7020")
    fig = px.bar(df, x="year", y="value", title=f"Temperature change over time in {np_country_select}")
    fig.show()

# climate data; all months with random country as box graph
def climate_data_random_single_country_in_month_over_year_as_box():
    random_country = np.random.randint((len(df_country_list) - 1), size=1)[0]
    np_country_select = df_country_list[random_country]
    df = clm_dataframe.query("`country` == @np_country_select")
    fig = px.box(df, x="year", y="value", title=f"Temperature change over time in {np_country_select}")
    fig.show()

def climate_and_ghg_single_country():
    clm1 = pd.DataFrame(clm_dataframe)
    ghg1 = pd.DataFrame(ghg_dataframe)

def read_climate_data_csv():
    #print("Reading climate data")
    df = pd.read_csv("../source-files/CLIMATEDATA.csv")
    df_area_list = df['Area'].unique() # 247 unique areas
    df_year_list = df['Year'].unique() # 60 unique years
    df_months_list = df['Months'].unique() # 17 unique months (12 standard, 4 seasons, 1 meteorological year)
    df_values_list = df['Value'].unique()
    #print("Maximum: {max(df_values_list)}")
    # Months Code = 7020
    random_area = np.random.randint((len(df_area_list) - 1), size=1)[0]
    #print(random_area)
    np_area_select = df_area_list[random_area]
    #print(np_area_select)

    df.query("`Area` == @np_area_select and `Months Code` == 7020", inplace=True)
    #df.query("`Months Code` == 7020", inplace=True)
    #df.query("`Area` == @np_area_select", inplace=True)
    #df.query("`Area` == @np_area_select and `Months Code` <= 7012", inplace=True)

    #fig = px.line(df, x="Year", y="Value", color="Months", title=f"Temperature change over time in {np_area_select}")
    #fig = px.box(df, x="Year", y="Value", title=f"Temperature change over time in {np_area_select}")
    #fig = px.strip(df, x="Year", y="Value", title=f"Temperature change over time in {np_area_select}")
    #fig = px.line(df, x="Year", y="Value", color="Area", title=None)
    #fig = px.histogram(df, x="Year", y="Value", color="Area", title="Temperature change for each country grouped by year.", barmode="group", height=1000)
    #fig = px.bar(df, x="Months", y="Value", color="Area", title="Temperature change for each country grouped by month.", barmode="group")
    #fig = px.bar(df, x="Months", y="Value", facet_row="Area", facet_col="Year")
    fig = px.box(df, x="Year", y="Value", color="Area", title=f"Temperature  change for {np_area_select} over time", range_y=[-9.5, 12.5])
    fig.show()

def read_greenhouse_gas_data_csv():
    #print("Reading greenhouse gas data")
    df = pd.read_csv("../source-files/GREENHOUSEGASDATA.csv")
    df_country_list = df['country'].unique()
    random_country_number = np.random.randint((len(df_country_list) - 1), size=1)[0]
    random_country = df_country_list[random_country_number]
    df.query("`country` == @random_country", inplace=True)

    first_line = go.Scatter(y=df["co2"],x=df["year"],name="co2")
    second_line = go.Scatter(y=df["methane"],x=df["year"],name="methane")
    third_line =  go.Scatter(y=df["nitrous_oxide"],x=df["year"],name="nitrous_oxide")

    fig = make_subplots(rows=1, cols=3, shared_yaxes=True)
    fig.add_trace(first_line, row=1, col=1)
    fig.add_trace(second_line, row=1, col=2)
    fig.add_trace(third_line, row=1, col=3)
    fig.show()

    #(co2, methane, nitrous_oxide)
    #fig1 = px.line(df, x='year', y='co2', title=f"CO2 output per year in {random_country}.")
    #fig1.show()
    #fig2 = px.line(df, x='year', y='methane', title=f"Methane output per year in {random_country}.")
    #fig2.show()
    #fig3 = px.line(df, x='year', y='nitrous_oxide', title=f"Nitrous Oxide output per year in {random_country}.")
    #fig3.show()


if __name__ == '__main__':
    library_version()
    #read_climate_data_csv()
    #read_greenhouse_gas_data_csv()

    climate_data_random_single_country_in_metereological_month_over_year_as_line()
    #climate_data_random_single_country_in_metereological_month_over_year_as_bar()
    #climate_data_random_single_country_in_month_over_year_as_box()
    #climate_and_ghg_single_country()