# coding=utf-8

import numpy as np
import math
import os, sys
import time
import copy
import matplotlib.pyplot as plt

class USRBIN():
    """
    Class for reconstructing and handling ASCII formatted Fluka USRBIN outputs
    
    Python version 3.8
    
    Developed by Daniel Björkman 2016-2021 at CERN, dabjor@kth.ch, daniel.bjorkman@cern.ch
    
    call:
    from USRBIN import USRBIN
    instance = USRBIN(filename, path, normfactor)
    instance.plot()
    
    """
    def __init__(self, filename, path = os.getcwd(), normfactor = 1):
        self.filename = filename
        self.path = path
        sys.path.insert(0, self.path)
        self.cube = []
        self.cubeErrors = []
        self.info = []
        self.starts = []
        self.stops = []
        self.depthdeposition = []
        self.horizontal = []
        self.vertical = []
        self.maxY = []
        self.widthY = []
        self.maxX = []
        self.widthX = []
        self.X = []
        self.Y = []
        self.vmax = []
        self.vmin = []
        self.normfactor = normfactor
        self.binningtype = []
        self.below = [] 
        self.side = []
        self.xcoodinates = []
        self.zcut = []
        self.maxalongz = []
        self.TIDP1meter = []
        self.feetdose = []
        self.pipe = []
        self.centre = []
        self.Xs = []
        self.Ys = []
        self.contourfilename = []
        self.contourpath = []
        self.title = []
        self.Xreal = []
        self.Yreal = []
        
        self.read()
        self.calc()
        
    def readRaw(self, start, stop):

        

#        data = np.genfromtxt(filename, skip_header= start -1, skip_footer= stop -9)
            

        data = np.genfromtxt(self.filename, skip_header= start -1, skip_footer= len(self.file) - stop -2)
        
        data = np.reshape(data ,(data.size,1))
    
        return data;        
    
    def constructCube(self, data):
        

        
        info = self.info

        
        #Cube reconstruction from list
        print("Reconstructing 3D cube...")
        if self.binningtype == 'RPZ':
            cube = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
            phiBinAngle = int(360 / info['pbin'][0])
            checkedVal = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
            x0 = int(info['rbin'][0]) - 0.5
            y0 = int(info['rbin'][0]) - 0.5
            stepConverter = 100
    
            #Reconstructs the R-Phi-Z binning into cartesian coordinate system
            Rvector = np.zeros((int(info['rbin'][0]),1))
            tracker = 0
            for z in range(0, int(info['zbin'][0])):
                for phi in range(0,int(info['pbin'][0])):     
                    Rvector = data[range(0 +tracker*int(info['rbin'][0]),(tracker +1)*int(info['rbin'][0])),0]   
                    tracker = tracker +1        
                   # Rvector = list[0:int(info['rbin'][0])]
                   # del list[:int(info['rbin'][0])]
                    for r in range(0,int(info['rbin'][0])):
                        val = Rvector[r]
                        steps = int(math.ceil(math.pi * (r + 1) * float(phiBinAngle) / 180))
                        for p in range(0,int(stepConverter * phiBinAngle), int(stepConverter * phiBinAngle / steps)):
                            angle = p * math.pi / (180 * stepConverter) + phi * phiBinAngle * math.pi / 180
                            x = int(round(x0 + (r + 0.5) * math.cos(angle)))
                            y = int(round(y0 + (r + 0.5) * math.sin(angle)))
                            if checkedVal[x,y,z] == 0:
                                cube[x, y,z] = val
                                checkedVal[x,y,z] = 1
    
            #Interpolating missing values
            print("Interpolating missing values...")
            for z in range(0,cube.shape[2]-1):
                for x in range(0,cube.shape[0] -1):
                    for y in range(0,cube.shape[1] -1):
                        if not checkedVal[x,y,z] and math.sqrt(math.pow(x-x0,2) + math.pow(y-y0,2)) < info['rbin'][0]:
                            sum = 0
                            sumCh = 0
                            for i in range(-1,2):
                                for ii in range(-1,2):
                                    sum = sum + cube[x+i,y+ii,z]
                                    sumCh = sumCh + checkedVal[x+i,y+ii,z]
                            cube[x,y,z] = sum/sumCh
                            checkedVal[x,y,z] = 1
            print("Missing values interpolated")
            cube = np.rot90(cube)
            cube = np.fliplr(cube)
    
        elif self.binningtype == 'RZ':
            cube = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
            phiBinAngle = int(360 / 4)
            checkedVal = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
            x0 = int(info['rbin'][0]) - 0.5
            y0 = int(info['rbin'][0]) - 0.5
            stepConverter = 100      
    
            #Reconstructs a quarter of the R-Z binning into cartesian coordinate system
            Rvector = np.zeros((int(info['rbin'][0]),1))
            tracker = 0
            for z in range(0, int(info['zbin'][0])):
                    Rvector = data[range(0 +tracker*int(info['rbin'][0]),(tracker +1)*int(info['rbin'][0])),0]   
                    tracker = tracker +1 
                    for r in range(0,int(info['rbin'][0])):
                        val = Rvector[r]
                        steps = int(math.ceil(math.pi * (r + 1) * float(phiBinAngle) / 180)*3) #number of steps
                        for p in range(0,stepConverter * phiBinAngle, stepConverter * phiBinAngle / steps):
                            angle = p * math.pi / (180 * stepConverter)
                            x = int(round(x0 + (r + 0.5) * math.cos(angle)))
                            y = int(round(y0 + (r + 0.5) * math.sin(angle)))
                            if checkedVal[x,y,z] == 0:
                                cube[x, y,z] = val
                                checkedVal[x,y,z] = 1
    
            #Interpolating missing values
            print("Interpolating missing values...")
            for z in range(0,cube.shape[2]-1):
                for x in range(int(cube.shape[0]/2),cube.shape[0] -1):
                    for y in range(int(cube.shape[1]/2),cube.shape[1] -1):
                        if not checkedVal[x,y,z] and math.sqrt(math.pow(x-x0,2) + math.pow(y-y0,2)) < info['rbin'][0]:
                            sum = 0
                            sumCh = 0
                            for i in range(-1,2):
                                for ii in range(-1,2):
                                    sum = sum + cube[x+i,y+ii,z]
                                    sumCh = sumCh + checkedVal[x+i,y+ii,z]
                            cube[x,y,z] = sum/sumCh
                            checkedVal[x,y,z] = 1
            print("Missing values interpolated")
    
            #Mirror the constructed quarter to fill the rest of the cube
            tmpCube = np.fliplr(cube)
            cube = cube + tmpCube
            tmpCube = np.flipud(cube)
            cube = cube + tmpCube
    
        else:
            cube = np.reshape(data, (int(info['xbin'][0]),int(info['ybin'][0]),int(info['zbin'][0])),order='F')
        
        return cube;
    
    
    
    def read(self):

    
        directory = self.path
        print("Loading " + self.filename)
        
        startTime = time.time()
        
        
    
        #Binning type
        RPZ = 0
        RZ = 0
        CAR = 0
        
        os.chdir(directory)
        file = open(self.filename).readlines()
    
        #Predefine meta info
        for i in range(1,len(file)):
            line_content = file[i].split()
            if len(line_content) > 5:
                if line_content[5] == 'A(ir,ip,iz),':
                    self.info = {'rbin':[],'zbin':[],'pbin':[], 'rmin':[],'rmax':[], 'zmin':[],'zmax':[], 'rwidth':[], 'zwidth':[],'prad':[]}
                    RPZ = 1
                    self.binningtype = 'RPZ'
                    print('R-Phi-Z binning detected')
                if line_content[5] == 'A(ix,iy,iz),':
                    self.info = {'xbin':[], 'ybin':[],'zbin':[], 'xmin':[],'xmax':[], 'ymin':[],'ymax':[], 'zmin':[],'zmax':[], 'xwidth':[], 'ywidth':[], 'zwidth':[]}
                    CAR = 1
                    self.binningtype = 'CAR'
                    print('Cartesian binning detected')
                if line_content[5] == 'A(ir,iz),':
                    self.info = {'rbin':[],'zbin':[],'pbin':[], 'rmin':[],'rmax':[], 'zmin':[],'zmax':[], 'rwidth':[], 'zwidth':[],'prad':[]}
                    self.info['pbin'].append(float(1))
                    RZ = 1
                    self.binningtype = 'RZ'
                    print('R-Z binning detected')
                try:
                    a = float(line_content[0])
                    if isinstance(a, float) and len(line_content) > 1:
                        break
                except Exception:
                        pass
    
        #Return if file is of wrong format
        if not (RPZ or RZ or CAR):
            print("Unable to read file")
            return
    
        #Extract dimensional information
        if RPZ or RZ:
                for line in file:
                    line_content = line.split()
                    if line.lstrip(' ').partition(' ')[0] == 'R':
                        if line_content[1] != '-':
                            self.info['rbin'].append(float(line_content[7]))
                            self.info['rmin'].append(float(line_content[3]))
                            self.info['rmax'].append(float(line_content[5]))
                            self.info['rwidth'].append(float(line_content[10]))
                    if line.lstrip(' ').partition(' ')[0] == 'Z':
                        self.info['zbin'].append(float(line_content[7]))
                        self.info['zmin'].append(float(line_content[3]))
                        self.info['zmax'].append(float(line_content[5]))
                        self.info['zwidth'].append(float(line_content[10]))
                    if line.lstrip(' ').partition(' ')[0] == 'P':
                        self.info['pbin'].append(float(line_content[7]))
                        self.info['prad'].append(float(line_content[10]))
        elif CAR:
                for line in file:
                     line_content = line.split()
                     if line.lstrip(' ').partition(' ')[0] == 'X':
                         self.info['xbin'].append(float(line_content[7]))
                         self.info['xmin'].append(float(line_content[3]))
                         self.info['xmax'].append(float(line_content[5]))
                         self.info['xwidth'].append(float(line_content[10]))
                     if line.lstrip(' ').partition(' ')[0] == 'Y':
                         self.info['ybin'].append(float(line_content[7]))
                         self.info['ymin'].append(float(line_content[3]))
                         self.info['ymax'].append(float(line_content[5]))
                         self.info['ywidth'].append(float(line_content[10]))
                     if line.lstrip(' ').partition(' ')[0] == 'Z':
                         self.info['zbin'].append(float(line_content[7]))
                         self.info['zmin'].append(float(line_content[3]))
                         self.info['zmax'].append(float(line_content[5]))
                         self.info['zwidth'].append(float(line_content[10]))
        #self.info = info
    
        if (RZ or RPZ) and not self.info['rmin'][0] == 0 :
            print("Function currently not defined for minimum rbins other than 0")
            return;
 

        
        if CAR:
            
            minX = self.info['xmin'][0]
            maxX = self.info['xmax'][0]
            widthX = self.info['xwidth'][0]
            minY = self.info['ymin'][0]
            maxY = self.info['ymax'][0]
            widthY = self.info['ywidth'][0] 
            minZ = self.info['zmin'][0]
            maxZ = self.info['zmax'][0]
            widthZ = self.info['zwidth'][0]*1.0001
            
            #for horizontal image, ie Z as x-axis and X as y-axis
            self.X, self.Y = np.meshgrid(np.arange(minZ,maxZ, widthZ),np.arange(minX + widthX,maxX + widthX, widthX))

            self.Yreal, self.Xreal = np.meshgrid(np.arange(minY,maxY, widthY), np.arange(minX,maxX, widthX))
        elif (RZ or RPZ):
            #For ATLAS fluka model
            maxY = int(self.info['rmax'][0])
            widthY = int(self.info['rwidth'][0])
            maxX = int(self.info['zmax'][0])
            widthX = int(self.info['zwidth'][0])
            self.X, self.Y = np.meshgrid(range(0,maxX, widthX),range(-maxY,maxY, widthY))            

            
        
        
        #Find start and stop for reading      
        for i in range(1,len(file)):
    
            isPrevString = False
            try:
                float(file[i -1].split()[0])
                
            except:
                isPrevString = True;
            
            try:        
                firstCurr = float(file[i].split()[0])
                if isinstance(firstCurr, float) and isPrevString and len(file[i].split()) == 10:      
                    self.starts.append(i +1)
            except:
                pass
            
            try:
                if (len(file[i].split()) == 10 and file[i+1][0] == "\n"):
                    self.stops.append(i+1)
            except:
                pass
        self.file = file
        
        
        # print("starts", self.starts)
        # print("stops", self.stops)
        
        # print("Note HACK" )
        # if self.filename == "T1_1w.ascii":
        #     self.starts[0] -= 1
        # # self.stops[0] -= 1
        # print("first row", self.file[self.starts[0]])
        # print("last row", self.file[self.stops[0]])
        # print((self.stops[0] - self.starts[0])*10, 58*45*260) 
            
        if len(self.stops) == 1:
            self.stops.append(self.starts[1] + self.stops[0] - self.starts[0]  )        

    
        
        data = self.readRaw(  self.starts[0], self.stops[0])
        cube = self.constructCube(data)
    
                
        end = time.time()
        print("Cube reconstructed in " + str(round(end - startTime,2)) + " seconds")
        print(' ')    
        self.cube = cube * self.normfactor
        self.max = np.amax(cube)
        self.min = np.amin(cube)


    def readError(self):

        
        data = self.readRaw(  self.starts[1], self.stops[1])
        cube = self.constructCube(data)
        
        print('Error values reconstructed')
        
        self.cubeErrors = cube;


    
    def loadGeometryFile(self, filename, path_drawings, firstIndex = 2, lastIndex = 4):
    
#    	""" 
#        Reads in a geometry file from FLUKA 
#    	x Axis -> Index 2
#    	y Axis -> Index 3
#    	z Axis -> Index 4
#    	Default: x and z Axis
#    	""" 

        os.chdir(path_drawings)

       	X = []	
       	Y = []
       	Xs = []	
       	Ys = []
       	for line in open(filename,"r+").readlines():
       		if line[0] == "#":
       			continue
       		if line.strip() == "":
       			if X:
       				Xs.append(copy.copy(X))
       				Ys.append(copy.copy(Y))				
       
       				X = []	
       				Y = []
       		else:
       			splitted = list(map(float, line.split()))               
       			X.append(splitted[firstIndex])
       			Y.append(splitted[lastIndex])
       
   
        if X:
             Xs.append(copy.copy(X))
             Ys.append(copy.copy(Y))				
             X = []	
             Y = []
    
        self.Xs = Xs
        self.Ys = Ys

    def drawGeo(self,ax , linewidth = 0.5, alpha = 1):
        
        for j in range(len(self.Xs)):
            plt.plot(self.Ys[j], self.Xs[j], 'k-',  linewidth=linewidth, alpha = alpha)
        return ax;
    
    
    def plot(self):
        
        cube = self.cube
        
        import math
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.colors import LogNorm
        import matplotlib.gridspec as gridspec
        import matplotlib.ticker as ticker

        #Determines the indecies of maxiumum value in cube
        i,j,k = np.unravel_index(cube.argmax(), cube.shape)

        #Conditional color scaling     
        vmax = cube.max()
        vmin = np.min(cube[np.nonzero(cube)])
        self.vmin = vmin
        self.vmax = vmax
        
        if int(math.log10(vmax)) - int(math.log10(vmin)) > 14 :
            vmin = vmax * math.pow(10,-14)

        fig = plt.figure()
        
        gs0 = gridspec.GridSpec(1, 3)
        gs00 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs0[0])
        ax = plt.subplot(gs0[1:])
        image = cube[0:,0:,k]
        image = np.rot90(image,3)
        if self.binningtype == 'CAR':
            def y_fmt(x, y):
                return cube.shape[0] - x
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(y_fmt))
        plt.pcolor(image, norm=LogNorm(vmin=vmin, vmax=vmax), cmap='jet')
        cbar = plt.colorbar()
        cbar.set_label('Intensity')
        plt.title('Z plane')
        plt.xlabel('X- axis')
        plt.ylabel('Y- axis')
        

        plt.subplot(gs00[0])
        image = cube[i,0:,0:]
        plt.pcolor(image, norm=LogNorm(vmin=vmin, vmax=vmax), cmap='jet')
        plt.title('X plane')
        plt.xlabel('Z- axis')
        plt.ylabel('Y- axis')


        plt.subplot(gs00[1])
        image = cube[0:,j,0:]
        plt.pcolor(image, norm=LogNorm(vmin=vmin, vmax=vmax), cmap='jet')
        plt.title('Y plane')
        plt.xlabel('Z- axis')
        plt.ylabel('X- axis')


        plt.subplot(gs00[2])
        vector = np.zeros((cube.shape[2]))
        for r in range(0,cube.shape[2]):
            vector[r] = np.sum(cube[0:,0:,r])
        plt.plot(range(0,cube.shape[2]),vector)
        plt.title('Integrated depth deposition')
        plt.xlabel('Z- axis')
        plt.ylabel('Integrated intensity')
        plt.grid()

        plt.show()

    def calc(self):
        
        
        cube = self.cube
        self.vertical = cube[int(cube.shape[0]/2),0:,0:]       
        self.horizontal = cube[0:,int(cube.shape[1]/2),0:]  
        self.zcut = cube[0:,0:,int(cube.shape[2]/2)]  
        
        integration = np.zeros((cube.shape[2]))
        below = np.zeros((cube.shape[2]))
        side = np.zeros((cube.shape[2]))
        maxalongz = np.zeros((cube.shape[2]))
        TIDP1meter = np.zeros((cube.shape[2]))
        feetdose = np.zeros((cube.shape[2]))
        pipe = np.zeros((cube.shape[2]))
        centre = np.zeros((cube.shape[2]))
        for r in range(0,cube.shape[2]):
            integration[r] = np.sum(cube[0:,0:,r])
            maxalongz[r] = np.max(cube[0:,0:,r])
            try:
                centre[r] = cube[int(cube.shape[0]/2), int(cube.shape[1]/2),r]
                pipe[r] = cube[int(23),13,r]
                feetdose[r] = cube[20,4,r]
                TIDP1meter[r] = cube[33,13,r]
                below[r] = cube[int(cube.shape[0]/2), 5,r]
                val = 0
                bins = 0
                for i in range(-1,2):
                    for j in range(-1,2): 
                        val = val + cube[14 + i ,int( cube.shape[1]/2) + j,r]
                        bins = bins +1
                side[r] = val/bins
            except:
                pass
            

        self.vmin = np.min(cube[np.nonzero(cube)])
        self.vmax = cube.max()           
            
            
        self.depthdeposition = integration
        self.below = below
        self.side = side
        self.maxalongz = maxalongz
        self.TIDP1meter = TIDP1meter
        self.feetdose = feetdose
        self.pipe = pipe
        self.centre = centre
        
        if self.binningtype == 'CAR':
            self.xcoordinates = np.arange(int(self.info['zmin'][0]),int(self.info['zmax'][0]),self.info['zwidth'][0]*1.0001)
            self.realxcoodinates = np.arange(int(self.info['xmin'][0]),int(self.info['xmax'][0]),self.info['xwidth'][0]*1.0001)
        
    
    
    def drawGeo_outside_of(self, ax , yCut, zCut, factor = 1 ,linewidth = 0.5, alpha = 1):

        for j in range(len(self.Xs)):
    
            xes = []
            yes = []        
    
            xesPre = self.Ys[j]
            yesPre = self.Xs[j]
            for i in range(len(xesPre)):
                if abs(yesPre[i]) < yCut and xesPre[i] < zCut:
                    pass
                else:
                    xes.append(xesPre[i])
                    yes.append(yesPre[i])
    
            plt.plot(xes,yes, 'k-',  linewidth=linewidth, alpha = alpha)
        return ax;
    
    
    def drawGeo_inside_of(self, ax , yCut, zCut , factor = 1 ,linewidth = 0.5, alpha = 1):
        # Only draws points that appear inside the rectangle defined by yCut and zCut
        # factor variable used to modify points in case m instead of cm
        
        
        
        for j in range(len(self.Xs)):
    
            xes = []
            yes = []        

            xesPre = np.asarray(self.Ys[j])/factor
            yesPre = np.asarray(self.Xs[j])/factor
            for i in range(len(xesPre)):
                if abs(yesPre[i]) < yCut and xesPre[i] < zCut:
                    xes.append(xesPre[i])
                    yes.append(yesPre[i])
                else:
                    pass
    
            plt.plot(xes,yes, 'k-',  linewidth=linewidth, alpha = alpha)
        return ax;






