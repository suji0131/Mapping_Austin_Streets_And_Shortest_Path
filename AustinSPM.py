'''@author: sujit, Date: 10/25/2016'''
import pandas as pd
from geoplotter import *
import networkx
import scipy as sp
import matplotlib
import matplotlib.pyplot
from scipy.spatial import distance

class networkAustin():
    def __init__(self):
        self.df = pd.read_csv('result.csv', header = 0) #using csv returned by running the mapAustin class
        self.node_dir = pd.read_csv('node.csv')
        self.startlon = self.df['start_lon'].tolist()
        self.startlat = self.df['start_lat'].tolist()
        self.endlon = self.df['end_lon'].tolist()
        self.endlat = self.df['end_lat'].tolist()
        
        self.df_address = pd.read_csv('addresses.csv')
        
        self.geo = GeoPlotter()
        
        self.createNetwork()
        self.initialPoints()
                   
    def stPoints(self):
        points = []
        for i in range(len(self.df)):
            start_pt = [self.startlon[i], self.startlat[i]]
            end_pt = [self.endlon[i], self.endlat[i]]
            line = [start_pt, end_pt]
            points.append(line)
        return points
        
    def drawMap(self, points):
        self.geo.setZoom(-97.8526, 30.2147, -97.626, 30.4323)
        self.geo.drawLines(points, color = 'b',linewidth = 0.3)
        #matplotlib.pyplot.show()
        
    def plotAddress(self, destination = None):
        self.drawMap(self.stPoints())
        for i in range(len(self.df_address)):
            Lat = self.df_address.Lat[i]
            Lon = self.df_address.Lon[i]
            if i == 15:
                self.geo.drawPoints(lat=Lat, lon=Lon, color='g')
            else:
                self.geo.drawPoints(lat=Lat, lon=Lon, color='r')
                
    def closest_node(self,node):
        node_set_array= sp.array([[self.node_dir.lon[i], self.node_dir.lat[i]]for i in range(len(self.node_dir))])
        closest_node = distance.cdist([node], node_set_array).argmin()
        return closest_node
        
    def initialPoints(self):
        etc_node = (self.df_address.Lon[15], self.df_address.Lat[15])
        self.etc = self.closest_node(etc_node)
        
        rudy_node = (self.df_address.Lon[3], self.df_address.Lat[3])
        self.rudy = self.closest_node(rudy_node)
        
        
    
    def createNetwork(self):
        self.network = networkx.DiGraph() 
        
        for i in range(len(self.df)):
            if self.df.ONE_WAY[i] == 'B':
                self.network.add_edge(self.df.strt_node[i], self.df.end_node[i], dict(time = self.df.SECONDS[i]))
                self.network.add_edge(self.df.end_node[i], self.df.strt_node[i], dict(time = self.df.SECONDS[i]))
                
            elif self.df.ONE_WAY[i] == 'FT':
                self.network.add_edge(self.df.strt_node[i], self.df.end_node[i], dict(time = self.df.SECONDS[i]))
            elif self.df.ONE_WAY[i] == 'TF':
                self.network.add_edge(self.df.end_node[i], self.df.strt_node[i], dict(time = self.df.SECONDS[i]))
                
    def spm(self, start_at = 1, destination = 2):
        
        self.soln = networkx.shortest_path(self.network, source = self.etc, target= self.rudy, weight = 'time')
        
    def drawPath(self):
        self.spm()
        self.plotAddress()
        
        self.points = [[[self.node_dir.lon[self.etc], self.node_dir.lat[self.etc]]]]
        for i in range(len(self.soln) - 1):
            start_pt = [self.node_dir.lon[self.soln[i]], self.node_dir.lat[self.soln[i]]]
            end_pt = [self.node_dir.lon[self.soln[i+1]], self.node_dir.lat[self.soln[i+1]]]
            line = [start_pt, end_pt]
            self.points.append(line)
        
            
        self.geo.setZoom(-97.8526, 30.2147, -97.6264, 30.4323)
        self.geo.drawLines(self.points, color = 'y',linewidth = 3.0)
        matplotlib.pyplot.show()

if __name__=='__main__':
    trail = networkAustin()
    trail.drawPath()
    #trail.plotAddress()
    #matplotlib.pyplot.show()