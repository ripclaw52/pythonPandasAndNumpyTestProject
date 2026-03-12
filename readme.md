### How to use the Dashboard.
Run the file: `DashApp.py` within PyCharm or VSCode.

Go to the local host generated through Dash to view the dashboard.

http://127.0.0.1:8050/

### Libraries required currently to run this project.  
#### Basic python libraries
>`pip install pandas`  
> Documentation: [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html)

>`pip install numpy`  
> Documentation: [Numpy](https://numpy.org/doc/stable/user/index.html)

#### Libraries for graphing:
>`pip install plotly`  
> Documentation: [Plotly](https://plotly.com/python-api-reference/)

>`pip install dash`  
> Documentation: [Dash](https://dash.plotly.com/)

### Files used with dashboard
#### Source locations for dataset files:
> Geographical JSON:
> 
> `City of Edmonton - Neighbourhoods.geojson`
> 
> [City of Edmonton - Neighbourhoods GeoJson](https://data.edmonton.ca/City-Administration/City-of-Edmonton-Neighbourhoods-Map-View-/wps4-8auk)

> Languages dataset:
> 
> `2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv`
> 
> [2016 Census Dwelling Unity by Language](https://data.edmonton.ca/Census/2016-Census-Dwelling-Unit-by-Language-Neighbourhoo/jsc3-gmwb)

> Assessment dataset:
> 
> `Property_Assessment_Data_2022.csv`
> 
> [Property Assessment Data (Current Year)](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg)

> Crime dataset:
> 
> `Occurrences_Last_90_Days.csv`
> 
> [Edmonton Community Safety Map](https://experience.arcgis.com/experience/8e2c6c41933e48a79faa90048d9a459d/page/Table/) 

***

### The Attached Report
#### Our team:
 - Aaron A
 - Ryley G
 - Omar M
 - Vlad M

<br>

#### Abstract

Moving into a new city is a stressful endeavor. Understanding the price of the property, what the surrounding neighbourhood is like culturally, and how bad crime is are all deciding factors on whether a person should move into that neighbourhood. Most applications detailing neighbourhoods do not have this information readily available. The dashboard application aims to include this information to help users decide on what neighbourhood to move into.

<br>

#### Introduction

Information visualization has the important role in data analysis of displaying the data in an understandable way, and illuminating conclusions made about the data to people unfamiliar with the intricacies of the source material. Stock markets, and the measurement of individual stocks over time contain large amounts of hard data, and difficult to understand for people without any experience with stocks. Information visualization would take the data of an individual stocks change over time and create a line graph representing this. A graph would indicate the progression of time through its x-axis and the monetary value in its y-axis. When a stocks value increases, visually the line increases in slope. A dashboard informing the overview of all stocks at a stock market would group similar stocks by company type such as communication systems, and the physically viewed size of each item could correspond to the company’s net worth. Addition of colour, with green indicating a gain in the stock and red a loss would provide easily browsed information important to stockbrokers and interested sellers and buyers.

Moving into a new house is a stressful endeavor. Moving into a new city or country has even more stress attached to it. Moving into a new neighbourhood means entering into a new social dynamic with neighbours. The importance of neighbourhoods to a person’s social life in rural communities cannot be understated. Living in a neighbourhood means involvement in your surrounding community, interacting with neighbours, joining in community events, or starting a family. Information that would help people choose which neighbourhood to move to is sparse and difficult to understand.

This dashboard application is hoping to solve that problem by providing the information in an easily understandable way. The dashboard aims to inform its users about what each neighbourhood entails. Currently the dashboard shows city information about three differing topics: assessment values of properties, current crime data, and 6-year-old census data about the general distribution of languages for each neighbourhood. This information will help people decide on moving into the neighbourhood.

<br>

#### Background

We are using data about the city of Edmonton. Specific datasets include 2016 data about the distribution of spoken languages per neighbourhood, current years property assessment data, and reported crimes within the last 90 days in the city. An assessed property value can inform the base price of a particular property and viewing that average for the neighbourhood gives an overall sense of the neighbourhood’s value to the city. The census data taken for the languages spoken in each neighbourhood can be considered to still be valid for another 4 years, as moving is expensive and not done regularly. Crime statistics is taken from the publicly available reported day that covers the range of 90 days and is updated regularly.


One of the applications we took inspiration from was Darkhorse Analytics “Fight Covid” dashboard. They utilized a topology map showing the concentration of cases, with the option of filtering showing counties and the overall state. A search and multiple dropdown list with summarized data allowed extended interactivity by displaying the data on the map and in graphs. Selections available include vulnerability, race, and COVID-19 stats with multiple sub options. Graphs are shown below the topology map detailing a listed summary of the data.


The Google maps application was also an inspiration with the map, displaying the marked locations selected, with our dashboard focusing solely on the city of Edmonton, and data pertaining to languages, crime, and property value.

<br>

#### Design

The objective of our application is to help users find suitable neighbourhoods to live in without the hassle of going through multiple resources.


The primary colours chosen within the dashboard are based on the city of Edmonton’s brand guidelines. The blue background colour provides equal focus on the dashboard with the map and graphs, and margins surrounding text create a clear grouping. The text inside the boxes is styled in a serif font and coloured white for easier reading. The highlighted colours within the map are a transparent purple, which differentiates from the coloured map used being prominent in greens and light grays. The selection outline for the neighbourhood is a transparent yellow, indicated through colour theory as the complementary to purple. The transparent green colour from a selection by the dropdown list stands out in the purple and is different from yellow. With the map being so colourful, the remaining graphs on the page use whitespace to reduce any noise created and maintain focus on the map.


Main features implemented into the application include a map outlining the residential neighbourhoods within an assessed value range selected by the user. Included on the map is the location and type of each reported crime grouping. The map chart was used to provide an overview of the city and connect the neighbourhood data to its geographical location. Selection of a specific neighbourhood within the assessed value range through a search bar or directly on the map distinctly outlines the neighbourhood.

![The Assessment Map]("The Assessment Map")

Separate from the map a counted listing of the reported crime groups, and selectable sub-groups is displayed with summarized values in two graphs. A radio button selection populates the subgroup selected and displays the statistics of the reported crime group as its subgroups. From that a selection is offered for its subgroups to show its subtype in the populated radio button. A subsequent graph is created displaying the subtypes and listing their numerical count.

![Greater Edmonton Crime Filter]("Greater Edmonton Crime Filter")

Beside the crime data is a dropdown selection using the reported languages per household excluding English, non-responses, and what has been defined as other. It displays the data as a horizontal bar graph of the top 5 neighbourhoods, with the number of homes in the neighbourhood listed.

![Non-English Languages per Household in Neighbourhoods]("Non-English Languages per Household in Neighbourhoods")

On a separate page is a neighbourhood comparison selection detailing the average assessed value of the neighbourhood and its distribution of languages. This page provides 3 dropdowns listing the neighbourhoods with search functionality and maintains the selected neighbourhood while on the other page.

![Neighbourhoods Average Housing Value and Proportion of Languages]("Neighbourhoods Average Housing Value and Proportion of Languages")

<br>

#### Implementation

We implemented the project mainly through the python coding language. We used the pandas python library for the creation of dataframes, importing the data stored within the CSV files into a usable format. Graphs were created through the plotly library utilizing the specific imports such as graph_objects and express which supported usage of the pandas library. Displaying the dashboard onto the web browser was used with the Dash library that supported HTML contents such as divs and dropdown objects. Four datasets were used in the project; 3 are in CSV format containing tabled information about the current years property assessment, 2016 languages census for neighbourhood, and previous 90 days of reported crime data. The fourth dataset contains a geographical marker outlining each neighbourhood on a map as geojson coordinates. The fourth dataset was used with the map to outline the neighbourhoods within the city.


Limitations of the project were primarily based on the lack of time to continue work on it. Property assessment data used within the dashboard focused mainly on residential housing, and an expansion to include farmland and commercial properties would provide additional information towards them. Utilizing the full information of the property assessment would detail each residence in each neighbourhood and provide information such as garage status, house number, account number, does it have a street address and does it have a suite value. Within the map, being able to view and filter these specific results per property would provide an influx of information to the user. And additional feature that could be included in the map-based selection would be to display that information and provide a connection to Google Maps service to show the state of the property currently.


Future planning involving the map would have it include information about the language distribution per neighbourhood, and a weighted display for each crime statistic. Weighted would refer to as the crime statistics are displayed currently as single dots at the recorded geographical location, it would change to count the amount of crime groups within a neighbourhood and increase the size of the dot.


Within the comparison section of the dashboard, mapping the crime statistics to the neighbourhood would allow for its inclusion in the comparison as it was previously intended. As the current crime data only included the geographical location and no neighbourhood section, mapping the crime data would be a more complicated process.


Moving our datasets to using dynamic API’s instead of static CSV files would be a step for future work, but due to lack of experience with using more complicated web-based technologies in a python language this was not implemented.
Further refinement of the stylistic UI of the dashboard, as well as the UI flow would be expanded on, and limited by time constraints.

<br>

#### Evaluation Methods

Referring to the Chapter four lecture discussing validation, initial focus would be placed on user testing. User tests would be performed with the application to see how UI flow and interactivity can be improved upon, and any questions or suggestions for additional data test users have would be considered during further refinement. Usage of design principles, mainly colour, size of objects within the graph and surrounding white space would have questions asked about these characteristics during the test cases and analyzed for optimization of the UI. After these factors are answered, algorithms would be simplified where possible, and the loading time of graphs would be optimized.

<br>

#### Conclusion

This dashboard aims to help users decide on which neighbourhood within the city of Edmonton best suits them. Information included pertains to what distinct cultural communities might have emerged in each neighbourhood, the safety in reported crime occurrences the neighbourhood receives, and the general property value of the homes in the neighbourhood to inform them of the expected cost. With an additional three months, future work would be spent on moving the python coding into JavaScript and utilizing software such as the react framework and MUI5Core UI library for components. Inclusion of a CSS theme would lower additional time spent on UI modifications within the dashboard.
