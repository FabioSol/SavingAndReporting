from SavingAndReporting.Saving.controllers.historic_controller import HistoricController

#print(HistoricController.get_last_24hrs_historic_rows("15843602"))
import plotly.graph_objects as go

# Sample data
x = [1, 2, 3, 4, 5]
y1 = [1, 4, 9, 16, 25]
y2 = [1, 2, 3, 4, 5]

# Create traces
trace1 = go.Scatter(x=x, y=y1, mode='lines', name='Line')
trace2 = go.Scatter(x=x, y=y2, mode='lines', name='Line 2')

# Create layout
layout = go.Layout(title='Stock Chart', xaxis=dict(title='X-axis'), yaxis=dict(title='Y-axis'))

# Create figure
fig = go.Figure(data=[trace1, trace2], layout=layout)

# Display the figure
fig.show()
