import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
df_languages = pd.read_csv("2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv")
df_languages_sorted = df_languages.sort_values(by=['Spanish'], ascending=False)

df_languages_sorted = df_languages_sorted.head(5)
print(df_languages_sorted)

print(df_languages_sorted["Spanish"])
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_languages_sorted['Spanish'],
    y=df_languages_sorted.head(5),
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
# ============================================================================================ #
# fig = px.bar(df, x="total_bill", y="day", orientation='h')
#fig.show()
#fig.show()
# ============================================================================================ #

barchart = px.bar(
            data_frame=df_languages_sorted,
            x=df_languages_sorted.Spanish[::-1],
            y=df_languages_sorted.Neighbourhood[::-1],
            opacity=0.9,
            #color="Assessed Value",
            orientation="h",
            #barmode='relative',

            #text='Assessed Value',
            #title="Average Home Value Assessment in Six Edmonton Neighbourhoods",
            #labels={'Assessed Value': 'Average Home Assessed Value', 'Neighbourhood': 'Edmonton Neighbourhoods'},
            width=1400,
            height=700,
        )

barchart.update_layout(
    xaxis=dict(
        title='Spanish Households',
        titlefont_size=16,
        tickfont_size=14,
    ),
    yaxis=dict(
        title='Neighbourhoods',
        titlefont_size=16,
        tickfont_size=14,
    )
)
barchart.update_traces(textposition='outside', width=[.5, .5, .5, .5, .5, .5, ])

pio.show(barchart)