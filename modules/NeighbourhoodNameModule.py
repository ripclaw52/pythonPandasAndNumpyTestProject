import plotly.graph_objects as go
import pandas as pd

def findLanguagesInNeighbourhood(filename, NEIGHBOURHOOD):
    dataFrame = pd.read_csv(filename)
    dataFrame = dataFrame[dataFrame['NeighbourhoodName'] == NEIGHBOURHOOD]

    column_headers = list(dataFrame.columns.values)
    print("The Column Header :", column_headers[4:15])

    english = (dataFrame.iloc[[0], 3])[214]
    arabic = (dataFrame.iloc[[0], 4])[214]
    cantonese = (dataFrame.iloc[[0], 5])[214]
    french = (dataFrame.iloc[[0], 6])[214]
    german = (dataFrame.iloc[[0], 7])[214]
    mandarin = (dataFrame.iloc[[0], 8])[214]
    indigenous = (dataFrame.iloc[[0], 9])[214]
    punjabi = (dataFrame.iloc[[0], 10])[214]
    spanish = (dataFrame.iloc[[0], 11])[214]
    tagalog = (dataFrame.iloc[[0], 12])[214]
    ukrainian = (dataFrame.iloc[[0], 13])[214]
    other = (dataFrame.iloc[[0], 14])[214]

    valueList = [arabic, cantonese, french, german, mandarin, indigenous, punjabi, spanish, tagalog, ukrainian]

    languages = [column_headers[10], column_headers[7], column_headers[9], column_headers[13], column_headers[8],
                 column_headers[11], column_headers[12], column_headers[4], column_headers[6], column_headers[5]]

    print(sorted(valueList))
    print(languages)

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
              'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
              'rgba(190, 192, 213, 1)', 'rgba(190, 192, 213, 1)',
              'rgba(190, 192, 213, 1)', 'rgba(190, 192, 213, 1)',
              'rgba(190, 192, 213, 1)', 'rgba(190, 192, 213, 1)']

    reversed_colors = colors[::-1]
    sorted_value = sorted(valueList);
    reversed_values = sorted_value[::-1]
    print(sorted_value)

    x_data = valueList
    y_data = languages

    fig = go.Figure()
    row = 0
    for xd, yd in zip(reversed_values, y_data):
        fig.add_trace(go.Bar(
            x=[yd], y=[xd],
            text=[xd],
            orientation='v',
            marker=dict(
                color='#0076B5',
                line=dict(color='rgb(248, 248, 249)', width=1)
            )
        ))
        row += 1

    fig.update_layout(
        title=f'Most Spoken Language in {NEIGHBOURHOOD}',
        xaxis_tickfont_size=14,
        xaxis=dict(
            title='Languages',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title='Total Households',
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
        font=dict(
            family="Courier New, monospace",
            size=18,  # Set the font size here
            color="RebeccaPurple"
        )
    )
    fig.update_layout(
        title_font_color="purple",
        title_font_size=24,
    )

    return fig