import pandas as pd
import os
from qgis.core import QgsVectorLayer

# Read the CSV file
df = pd.read_csv('kml_files.csv')

# Download the KML files to a local directory
for index, row in df.iterrows():
    url = row['download_link']
    filename = os.path.join('kml_files', os.path.basename(url))
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Load the KML files into QGIS
for filename in os.listdir('kml_files'):
    full_path = os.path.join('kml_files', filename)
    layer = QgsVectorLayer(full_path, 'KML Layer', 'ogr')
    QgsProject.instance().addMapLayer(layer)
