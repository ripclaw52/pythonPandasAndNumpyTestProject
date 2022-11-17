import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

dataFrame = pd.read_csv("2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv")

#df = dataFrame[dataFrame['NeighbourhoodName']=='CRESTWOOD']
column_headers = list(dataFrame.columns.values)
print("The Column Header :", column_headers[4:15])

#print((dataFrame.loc[[0], "English Only"])[0])
# print(dataFrame.loc[[0], "No Response"])
# x = dataFrame.loc[[0], "No Response"]
# print(x[0])
# print(len(dataFrame))

english = 0
arabic = 0
cantonese = 0
french = 0
german = 0
mandarin = 0
indigenous = 0
punjabi = 0
spanish = 0
tagalog = 0
ukrainian = 0
other = 0

# dfRspnd = dataFrame.iloc[[0], 3]
# print(dfRspnd)

for row in range(len(dataFrame)):
    #english += (dataFrame.iloc[[row], 3])[row]
    arabic += (dataFrame.iloc[[row], 4])[row]
    cantonese += (dataFrame.iloc[[row], 5])[row]
    french += (dataFrame.iloc[[row], 6])[row]
    german += (dataFrame.iloc[[row], 7])[row]
    mandarin += (dataFrame.iloc[[row], 8])[row]
    indigenous += (dataFrame.iloc[[row], 9])[row]
    punjabi += (dataFrame.iloc[[row], 10])[row]
    spanish += (dataFrame.iloc[[row], 11])[row]
    tagalog += (dataFrame.iloc[[row], 12])[row]
    ukrainian += (dataFrame.iloc[[row], 13])[row]
    #other += (dataFrame.iloc[[row], 14])[row]


valueList = [arabic, cantonese, french, german, mandarin, indigenous, punjabi, spanish, tagalog, ukrainian]
#valueList.append(english)
#valueList.append(other)

colNames = [column_headers[9], column_headers[7], column_headers[13], column_headers[11], column_headers[4],
            column_headers[8], column_headers[10], column_headers[5], column_headers[12], column_headers[6]]

print(sorted(valueList))
fig = go.Figure()
fig.add_trace(go.Bar(
    x=sorted(valueList),
    y=colNames,
    marker_color='rgba(38, 24, 74, 0.8)',
    orientation="h",
     ))
# fig.add_trace(go.Bar(x=neighbourhood,
#                      y=noResponse,
#                      name='No Response',
#                      marker_color='rgb(26, 118, 255)'
#                      ))

fig.update_layout(
    title='Languages Spoken Other than English',
    xaxis_tickfont_size=14,
    xaxis=dict(
        title='Total Households',
        titlefont_size=16,
        tickfont_size=14,
    ),
    yaxis=dict(
        title='Languages',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinate.
)

fig.update_layout(
    title_font_color="purple",
    title_font_size=20,
)
#fig.update_xaxes(categoryorder='category ascending')
#fig.update_layout(xaxis={'categoryorder':'category descending'})
fig.show()
