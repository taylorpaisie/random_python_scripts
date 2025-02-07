import os
import folium
import json
import pandas as pd
import branca.colormap as cm

# Load the modified GeoJSON file
# with open('georiga_water_map.json') as f:
#     geojson_data = json.load(f)
water = json.load(open('georiga_water_map.geojson'))

# Define map attributes
attr = ('&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>')
tiles = 'https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png'

# Create the map
m = folium.Map(location=[33.473499, -82.010513], zoom_start=12, 
    tiles="OpenStreetMap", tile=tiles, attr=attr)

folium.GeoJson(water, style_function=lambda x:
  {'color' : '#58bbff', 'stroke' : '#58bbff', 'fill' : '#58bbff', 'strokeWidth' : '0.25', 
  'strokeOpacity': '0.75', 'fillColor' : '#58bbff', 'fillOpacity': '0.25'}
  ).add_to(m)


folium.Marker(
    location=[33.420696, -82.152374],
    popup="Fort Eisenhower",
    icon=folium.Icon(color="green", icon="flag"),
).add_to(m)

folium.Marker(
    location=[33.43761501031615, -82.03078216623695],
    popup="Hillcrest Memorial Park",
    icon=folium.Icon(color="blue", icon="heart"),
).add_to(m)


folium.Marker(
    location=[33.353140931803, -82.14176047439956],
    popup="Richmond County Solid Waste",
    icon=folium.Icon(color="red", icon="trash"),
).add_to(m)


folium.Marker(
    location=[33.38385047386637, -82.07783594154627],
    popup="Patient 1",
    icon=folium.Icon(color="gray", icon="home"),
).add_to(m)

folium.Marker(
    location=[33.437231342828994, -82.03516298056311],
    popup="Patient 2",
    icon=folium.Icon(color="purple", icon="home"),
).add_to(m)

folium.Marker(
    location=[33.37318610299889, -82.23698184151893],
    popup="Camp Crockett",
    icon=folium.Icon(color="black", icon="flag"),
).add_to(m)

# Create a custom legend with larger text
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 250px; height: 120px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; padding: 10px;">
    <b>Legend</b><br>
    <i class="fa fa-flag" style="color:green"></i> Fort Eisenhower<br>
    <i class="fa fa-heart" style="color:blue"></i> Hillcrest Memorial Park<br>
    <i class="fa fa-trash" style="color:red"></i> Richmond County Solid Waste<br>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Add scale bar
scale_bar_html = '''
<div style="position: fixed;
            bottom: 10px; left: 50px; width: 125px; height: 40px;
            background-color: white; border: 1px solid black; text-align: center;
            padding: 5px; font-size:10px; z-index: 9999;">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 3px;">
        <div style="width: 50px; height: 5px; background-color: black;"></div>
        <div style="width: 0.025px; height: 5px; background-color: black;"></div>
        <div style="width: 50px; height: 5px; background-color: black;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 12px;">
        <span>0 km</span><span>1 km</span><span>2 km</span>
    </div>
</div>
'''
m.get_root().html.add_child(folium.Element(scale_bar_html))


# Save the map
m.save('augusta_ga_map_with_legend_scale.html')

# m.save('index3.html')

# Load sample data
# sample_data = pd.read_csv("croatian_host_chrolopeth.csv")

# # Define threshold scale
# min_value = sample_data["Samples"].min()
# max_value = sample_data["Samples"].max()

# # Create a custom color map using branca
# colormap = cm.linear.BuPu_09.scale(min_value, max_value)

# # Create a new column in the DataFrame for colors
# sample_data['color'] = sample_data['Samples'].apply(lambda x: colormap(x))

# # Create a feature group
# choropleth = folium.FeatureGroup(name='Choropleth')

# # Add the GeoJson layer manually
# for feature in geojson_data['features']:
#     location = feature['properties']['id']
#     color = 'gray'  # Default color for NaN values

#     if location in sample_data['Location'].values:
#         color = sample_data[sample_data['Location'] == location]['color'].values[0]
    
#     folium.GeoJson(
#         feature,
#         style_function=lambda x, color=color: {
#             'fillColor': color,
#             'color': 'black',
#             'weight': 1,
#             'fillOpacity': 0.7,
#             'lineOpacity': 1
#         }
#     ).add_to(choropleth)

# # Add the feature group to the map
# choropleth.add_to(m)

# # Add the colormap to the map
# colormap.add_to(m)

# # Add markers
# locations = [
#     (45.397579, 16.892559, "Lipovljani", '#4169E1'),
#     (45.191872, 18.688511, "Cerna", '#30D5C8'),
#     (45.073372, 18.694830, "Zupanja", '#B57EDC'),
#     (45.372030, 16.921640, "Nova Subocka", '#FFC300'),
#     (45.652950, 16.534479, "Novoselec", '#8B0000'),
#     (45.898628, 16.842340, "Bjelovar", '#FF6F61'),
#     (46.44944, 16.43361, "Žiškovec", '#228B22')
# ]

# for lat, lon, name, color in locations:
#     folium.CircleMarker(
#         radius=10,
#         location=[lat, lon],
#         popup=name,
#         color=color,
#         fill=True,
#         fill_opacity=0.5,
#         opacity=1
#     ).add_to(m)

# Save the map
# m.save('index3.html')
