import processing
#for alg in QgsApplication.processingRegistry().algorithms():
#    print(alg.id(), "->", alg.displayName())

# get layer names 
names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]

for name in names:
    # create main plot
    aa = processing.run("native:rectanglesovalsdiamonds", {
        'INPUT':name, 
        'SHAPE':0, 
        'WIDTH':50, 
        'HEIGHT':50, 
        'ROTATION':0,
        'SEGMENTS':1, 
        'OUTPUT':'memory:'})

    # create subplots
    bb = processing.run("native:creategrid", {
        'TYPE':2,
        'EXTENT': aa['OUTPUT'],
        'HSPACING':5,
        'VSPACING':5,
        'CRS':'EPSG:32748',
        'OUTPUT':'memory:'})

    ## create centroids
    cc = processing.run("native:centroids", {
        'INPUT':bb['OUTPUT'],
        'ALL_PARTS':True,
        'OUTPUT':'memory:'})
        
    # create vertices 
    dd = processing.run("native:extractvertices",{
        'INPUT':bb['OUTPUT'],
        'OUTPUT':'memory:'})
    #
    # open layer 
    QgsProject.instance().addMapLayer(aa['OUTPUT'])
    QgsProject.instance().addMapLayer(bb['OUTPUT'])
    QgsProject.instance().addMapLayer(cc['OUTPUT'])
    QgsProject.instance().addMapLayer(dd['OUTPUT'])