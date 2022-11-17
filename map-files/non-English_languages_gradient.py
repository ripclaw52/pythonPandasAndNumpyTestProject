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

totalResponds = 0
totalNoResponds = 0

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

dfRspnd = dataFrame.iloc[[0], 3]
print(dfRspnd)


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

# long_dataFrame = px.data.medals_long()
# print(sorted(valueList))
# fig = px.bar(long_dataFrame, x=valueList, y=colNames, color='rgba(38, 24, 74, 0.8)', orientation='h',
#              #hover_data=["tip", "size"],
#              height=400,
#              title='Restaurant bills')
# fig.show()
#fig.show()

top_labels = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree',
              'Strongly<br>disagree']

colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
          'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
          'rgba(190, 192, 213, 1)', 'rgba(190, 192, 213, 1)',
          'rgba(190, 192, 213, 1)', 'rgba(190, 192, 213, 1)',
          'rgba(190, 192, 213, 1)', 'rgba(190, 192, 213, 1)']

reversed_colors = colors[::-1]

x_data = valueList
y_data = colNames

fig = go.Figure()
row = 0
for xd, yd in zip(sorted(valueList), y_data):
    fig.add_trace(go.Bar(
        x=[xd], y=[yd],
        orientation='h',
        text=[xd],
        marker=dict(
            color=reversed_colors[row],
            line=dict(color='rgb(248, 248, 249)', width=1)
        )
        )
    )
    row += 1

fig.update_layout(
    title='Most Spoken Language Other than English',
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
    bargroupgap=0.1,  # gap between bars of the same location coordinate.
    showlegend=False,
)

fig.update_layout(
    title_font_color="purple",
    title_font_size=20,
)
fig.show()
