import gpxpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#age = int(input("your age: "))
age = 22
#maxHR = 220 - age
maxHR = 190
print("your max HR is: ", maxHR)

gpx = gpxpy.parse(open('./ride.gpx'))

track = gpx.tracks[0]
segment = track.segments[0]

data = []
segment_length = segment.length_3d()
for point_idx, point in enumerate(segment.points):
    for ext in point.extensions:
        for extchild in list(ext):
            data.append([point.longitude, point.latitude,
                 point.elevation, point.time, segment.get_speed(point_idx),0, '{1}'.format(extchild.tag, extchild.text)])

columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed (m/s)', 'Speed (km/h)', 'Heart Rate']
df = pd.DataFrame(data, columns=columns)

df['Speed (km/h)'] = df['Speed (m/s)']*3.6

df['Filtered Speed'] = df['Speed (km/h)'].rolling(10).mean()

df['Heart Rate'] = pd.to_numeric(df['Heart Rate'])

conditions = [
    (df['Heart Rate'] <= 0.589*maxHR),
    (df['Heart Rate'] > 0.589*maxHR) & (df['Heart Rate'] <= 0.779*maxHR),
    (df['Heart Rate'] > 0.779*maxHR) & (df['Heart Rate'] <= 0.874*maxHR),
    (df['Heart Rate'] > 0.874*maxHR) & (df['Heart Rate'] <= 0.968*maxHR),
    (df['Heart Rate'] > 0.968*maxHR)
    ]

values = [1, 2, 3, 4, 5]

df['HR Zone'] = np.select(conditions, values)

df['Duration (s)'] = (df['Time'] - df['Time'][0]).dt.total_seconds()

df = df.dropna()

print("max heart rate = ",(np.max(df['Heart Rate'])))
print("avg heart rate = ",(int(np.mean(df['Heart Rate']))))

print("max speed = ",(np.max(df['Filtered Speed'])))
print("avg speed = ",(np.mean(df['Filtered Speed'])))

print(df)

fig = plt.subplots()
plt.plot(df['Longitude'], df['Latitude'],color='darkorange', linewidth=5, alpha=0.5)
plt.title('Route')

fig2, ax2 = plt.subplots()
ax2.plot(df['Duration (s)'], df['Altitude'], color='red')
ax2.tick_params(axis='y', labelcolor='red')

ax3 = ax2.twinx()
ax3.plot(df['Filtered Speed'], color='green')
ax3.tick_params(axis='y', labelcolor='green')

ax4 = ax2.twinx()
ax4.plot(df['Speed (km/h)'], color='blue')
ax4.tick_params(axis='y', labelcolor='blue')
plt.title('Analyze')

zones_count=[]
zones_count.append(sum(df['HR Zone'] == 1))
zones_count.append(sum(df['HR Zone'] == 2))
zones_count.append(sum(df['HR Zone'] == 3))
zones_count.append(sum(df['HR Zone'] == 4))
zones_count.append(sum(df['HR Zone'] == 5))

labels = ['Z1','Z2','Z3','Z4','Z5']

fig5, ax5 = plt.subplots()
ax5.pie(zones_count, labels=labels, autopct='%1.1f%%',startangle=90)
plt.title('HR Zones')

plt.show()
