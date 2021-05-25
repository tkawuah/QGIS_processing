import numpy as np

layer = iface.activeLayer() #click to highlight layer

fields = layer.fields()

field_idx = fields.indexFromName("rad") #change to match name of field

features = [f for f in layer.getFeatures()]

layer.startEditing()
for feat in layer.getFeatures():
    cent = feat.geometry().centroid()
    vert = [QgsGeometry.fromPointXY(QgsPointXY(v)) for v in feat.geometry().vertices()]
    rad = [cent.distance(v) for v in vert]
    rad = np.round(np.mean(rad), 3)
    print(rad)
    layer.changeAttributeValue(feat.id(), field_idx, float(rad))
layer.commitChanges()
