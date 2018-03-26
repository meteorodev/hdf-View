# _*_ coding: utf-8 *_*
# Autor: Darwin Rosero Vaca
# Descripción:

import pandas as pd
import numpy as np
from osgeo import gdal
import os
from glob import glob
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt


class LoadHdf():
    """"""

    def __init__(self, ):
        """Constructor for LoadHdf"""

    def hdfSubdatasetExtrac(hdf_file, dst_dir, subdataset):
        """unpack a single subdataset from a HDF5 container and write to GeoTiff"""
        # open the dataset
        hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)
        band_ds = gdal.Open(hdf_ds.GetSubDatasets()[subdataset][0], gdal.GA_ReadOnly)

        # read into numpy array
        band_array = band_ds.ReadAsArray().astype(np.int16)

        # convert no_data values
        band_array[band_array == -28672] = -32768

        # build output path
        band_path = os.path.join(dst_dir,
                                 os.path.basename(os.path.splitext(hdf_file)[0]) + "-sd" + str(subdataset + 1) + ".tif")

        # write raster
        out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                      band_ds.RasterXSize,
                                                      band_ds.RasterYSize,
                                                      1,  # Number of bands
                                                      gdal.GDT_Int16,
                                                      ['COMPRESS=LZW', 'TILED=YES'])
        out_ds.SetGeoTransform(band_ds.GetGeoTransform())
        out_ds.SetProjection(band_ds.GetProjection())
        out_ds.GetRasterBand(1).WriteArray(band_array)
        out_ds.GetRasterBand(1).SetNoDataValue(-32768)

        out_ds = None  # close dataset to write to disc

    def pdReadHdf(self,hdfPath):
        archivos = self.listFile(hdfPath, sufijo=".hdf")
        for arc in archivos:
            print(arc)
            dnvi = pd.read_hdf(arc,key=None,mode='r')

            dnvi.close()


    def listFile(self, filePath, prefijo="nada", sufijo="nada"):
        """Lee los archivos dado un directorio y un sufijo igual para todos los archivos"""
        # print("def listFile(self,filePath, prefijo=\"nada\", sufijo=\"nada\"):")
        # print(prefijo,"",sufijo)
        if prefijo == "nada":
            return glob(filePath + "*" + sufijo)
        else:
            return glob(filePath + "" + prefijo + "*")

    def hdfopen(self,hdfPath):

        archivos = self.listFile(hdfPath, sufijo=".hdf")
        for arc in archivos:
            print(arc)
            # Read H5 file
            f = h5.File(arc, "r")
            # obtienen la lista de los dataset
            datasetNames = [n for n in f.keys()]
            for n in datasetNames:
                print(n)

            # extract NDVI data from the HDF file
            ndvidata = f['NDVI']
            # extract one pixel from the data
            ndviSumData = ndvidata[:, 49, 392]
            ndviSumData = ndviSumData.astype(float)
            totData=totData+ndviSumData
            # Print the attributes (metadata):
            print("Data Description : ", ndvidata.attrs['Description'])
            print("Data dimensions : ", ndvidata.shape, ndvidata.attrs['DIMENSION_LABELS'])
            # print a list of attributes in the H5 file
            for n in ndvidata.attrs:
                print(n)
            # close the h5 file
            f.close()

            # Plot
            plt.plot( ndviSumData)
            plt.title("Vegetation index")
            plt.ylabel('time')
            plt.ylim((0, 1))
            plt.xlabel('Wavelength [$\mu m$]')
            plt.show()

            f.close()
        return totData

rutandvi="/media/drosero/Datos/modis/Modis/flyred/"
#rutandvi = "/media/drosero/Datos/modis"  # MOD13L2.A2016194.1556.006.2016194161014.hdf
hdf = LoadHdf()

hdf.pdReadHdf(rutandvi)
#dataset = hdf.hdfopen(rutandvi)
