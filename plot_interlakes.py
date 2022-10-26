import gpxpy
import pandas as pd
import numpy as np
import seawater as sw
import matplotlib.pyplot as plt

gpx = gpxpy.parse(open('./interlakes.gpx'))

track = gpx.tracks[0]
segment = track.segments[0]

data = []
segment_length = segment.length_3d()
for point_idx, point in enumerate(segment.points):
    data.append([point.longitude, point.latitude])

columns = ['Longitude', 'Latitude']
df = pd.DataFrame(data, columns=columns)

df = df.dropna()

print(df.head())

fig = plt.subplots()
plt.plot(df['Longitude'], df['Latitude'],
        color='darkorange', linewidth=5, alpha=0.5)

plt.title('Interlagos Circuit')
plt.plot(fig=fig, tiles='esri_aerial')

plt.show()