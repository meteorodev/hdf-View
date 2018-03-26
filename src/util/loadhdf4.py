# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:


import os
import matplotlib as mpl
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import numpy as np

from glob import glob

from pyhdf.SD import SD, SDC

class LoadHdf4():
    """"""

    def __init__(self,):
        """Constructor for LoadHdf4"""

    def listFile(self, filePath, prefijo="nada", sufijo="nada"):
        """Lee los archivos dado un directorio y un sufijo igual para todos los archivos"""
        # print("def listFile(self,filePath, prefijo=\"nada\", sufijo=\"nada\"):")
        # print(prefijo,"",sufijo)
        if prefijo == "nada":
            return glob(filePath + "*" + sufijo)
        else:
            return glob(filePath + "" + prefijo + "*")

    def hdfopen(self,hdfPath,var='NDVI'):
        archivos = self.listFile(hdfPath,sufijo="hdf")
        print(archivos)
        expData=[]
        for arc in archivos:
            print(arc)
            # Read Hdffile file
            hdf = SD(arc,SDC.READ)
            #Print Variables
            print(hdf.datasets())
            #read Dataset
            dataVar=hdf.select(var)
            print("metadata from var")
            print(dataVar.dimensions())
            print(dataVar.attributes())
            dataMat=dataVar[:,:]
            print(dataMat)
            print(type(dataMat))
            expData.append(dataMat)
            print("Datavar #####")
            ##geolocation Var names
            # Read geolocation dataset.

            print("geolocation vars ················")
            lat = hdf.select('Latitude')
            latitude = lat[:,:]
            print(latitude)
            lon = hdf.select('Longitude')
            longitude = lon[:,:]
            print(longitude)
            hdf.end()
        self.plotMap(dataMat,longitude,latitude)
        return dataMat

    def findCoor(self, latnc, lonnc, latp, lonp):
        """Retorna un serie de tiempo desde el netcdf dada un latitud y longitug"""

        # print(latp," metodo findCoor ", lonp)
        ncmx = np.where(latnc >= latp)
        mx = len(ncmx[0])
        latncb = [latnc[mx - 1], latnc[mx]]
        # print("latitudes ", latncb)
        a = abs(latncb[0]) - abs(latp)
        b = abs(latp) - abs(latncb[1])
        corfin = []
        pos = []
        if a > b:
            corfin.append(latncb[1])
            pos.append(mx)
        else:
            corfin.append(latncb[0])
            pos.append(mx - 1)
        # print("********************************")
        # print(lonnc)
        ncmx = np.where(lonnc <= lonp)
        # print(lonnc[ncmx])
        mx = len(ncmx[0])
        lonncb = [lonnc[mx - 1], lonnc[mx]]
        a = abs(lonncb[0]) - abs(lonp)
        b = abs(lonp) - abs(lonncb[1])
        if a > b:
            corfin.append(lonncb[1])
            pos.append(mx)
        else:
            corfin.append(lonncb[0])
            pos.append(mx - 1)
        # print("longitudes ",lonncb)
        # print("############################################")
        return {"coor": corfin, "pos": pos}

    def plotMap(self,data,longitude, latitude):
        m = Basemap(projection='mercator', resolution='l', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
        m.drawcoastlines(linewidth=0.5)
        m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
        m.drawmeridians(np.arange(-180., 181., 45.), labels=[0, 0, 0, 1])
        x, y = m(longitude, latitude)
        m.pcolormesh(x, y, data)


hdf=LoadHdf4()

ruta= rutandvi="/media/drosero/Datos/modis/Modis/flyred/"

ndvida=hdf.hdfopen(ruta)
