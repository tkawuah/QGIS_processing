#import modules 
import gdal
import ogr
import numpy as np
import tempfile


#support functions
def rasterize(clip_raster, shp, attrib_name):
    raster_ds = gd.Open(clip_raster)
    # Fetch number of rows and columns
    ncol = raster_ds.RasterXSize
    nrow = raster_ds.RasterYSize
    
    # Fetch projection and extent
    proj = raster_ds.GetProjectionRef()
    ext = raster_ds.GetGeoTransform()
    raster_ds = None
    
    # Create the raster dataset
    temp_out = tempfile.NamedTemporaryFile(suffix='.tif').name
    memory_driver = gd.GetDriverByName('GTiff')
    out_raster_ds = memory_driver.Create(temp_out, ncol, nrow, 1, gd.GDT_Byte)
    
    # Set the ROI image's projection and extent to our input raster's projection and extent
    out_raster_ds.SetProjection(proj)
    out_raster_ds.SetGeoTransform(ext)
    
    mb_v = ogr.Open(shp)
    mb_l = mb_v.GetLayer()
    
    # Rasterize the shapefile layer to our new dataset
    
    status = gd.RasterizeLayer(out_raster_ds, [1], mb_l, options=["ATTRIBUTE="+attrib_name])  # put raster values according to the 'id' field values
    
    return temp_out
    

def img_to_array(input_file, dim_ordering="channels_last", dtype='float32'):
    file = gd.Open(input_file)
    bands = [file.GetRasterBand(i) for i in range(1, file.RasterCount + 1)]
    arr = np.array([gdn.BandReadAsArray(band) for band in bands]).astype(dtype)
    
    if dim_ordering=="channels_last":
        arr = np.transpose(arr, [1, 2, 0])  # Reorders dimensions, so that channels are last
    return arr
    
    
def array_to_tif(array, raster, dst_filename):
    src_raster = gd.Open(raster)
    x_pixels = src_raster.RasterXSize
    y_pixels = src_raster.RasterYSize
    bands= array.shape[2]
    driver = gd.GetDriverByName('GTiff')
    
    dtype = str(array.dtype)
    datatype_mapping = {'byte': gd.GDT_Byte, 'uint8': gd.GDT_Byte, 'uint16': gd.GDT_UInt16, 
                        'int8': gd.GDT_Byte, 'int16': gd.GDT_Int16, 'int32': gd.GDT_Int32,
                        'uint32': gd.GDT_UInt32, 'float32': gd.GDT_Float32}
                        
    out = driver.Create(dst_filename, x_pixels, y_pixels, bands, datatype_mapping[dtype])
    out.SetGeoTransform(src_raster.GetGeoTransform())
    out.SetProjection(src_raster.GetProjection())
    
    for i in range(bands):
        out.GetRasterBand(i+1).WriteArray(array[:, :, i])
        
    out.FlushCache()  # Write to disk.
    
    


#Get data 
inRaster = "/*.tif"
inVector = "/*.shp"


#Get vector layer attribute names 
lyr = ogr.Open(inVector)
lyr = lyr.GetLayer()

all_fields = [f.name for f in lyr.schema]


#select fied names to use 
field_names = [f for f in all_fields if f not in ['REGION_ID', 'FX_NUMHOLE', 'FX_HOLESOL']]


#Create multiband raster 
img_array_list = []
for i in band_info.columns:
    fx = rasterize(inRaster, inVector, i)
    fx_array = img_to_array(fx)
    mg_array_list.append(fx_array)

fx_multi = np.concatenate(img_array_list, axis=-1)
fx_multi.shape


# write raster
array_to_tif(fx_multi.astype(np.float32), inRaster, 'fx_multi.tif')
