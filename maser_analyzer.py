import matplotlib.pyplot as plt
import numpy as np
import os
import sys

class Fourier1:
    def __init__(self,Mx,My,ax,fig,line1,line2,line3,line4,vline1,vline2,vline3,vline4,text1,text2):
        self.x1, self.y1 = line1.get_data()
        self.x2, self.y2 = line2.get_data()
        self.x3, self.y3 = line3.get_data()
        self.x4, self.y4 = line4.get_data()
        self.dt = self.x1[1] - self.x1[0]
        self.fs = 1.0/self.dt
        self.ax = ax
        self.fig = fig
        self.vline1 = vline1
        self.vline2 = vline2
        self.text1 = text1
        self.vline3 = vline3
        self.vline4 = vline4 
        self.text2 = text2
        self.Mx = Mx
        self.My = My
        self.Mt = Mx + 1j * My

    def button_press(self,event):
        if event.inaxes is ax[0,0]:
            x1, y1 = event.xdata, event.ydata
            global x1in
            x1in = min(np.searchsorted(self.x1, x1), len(self.x1) - 1)
	    
        if event.inaxes is ax[1,0]:
            x3, y3 = event.xdata, event.ydata
            global x3in
            x3in = min(np.searchsorted(self.x3, x3), len(self.x3) - 1)

        if event.inaxes is ax[0,1]:
            x2, y2 = event.xdata, event.ydata
            global x2in
            x2in = x2
            self.vline1.set_xdata([x2in])
            plt.draw()

        if event.inaxes is ax[1,1]:
            x4, y4 = event.xdata, event.ydata
            global x4in
            x4in = x4
            self.vline3.set_xdata([x4in])
            plt.draw()

    def button_release(self,event):
        if event.inaxes is ax[0,0]:
            x1, y1 = event.xdata, event.ydata
            global x1fi
            x1fi = min(np.searchsorted(self.x1, x1), len(self.x1) - 1)
	        
            spectrum = np.fft.fft(self.Mt[x1in:x1fi])
            spectrum = np.fft.fftshift(spectrum)
            freq = np.linspace(-self.fs/2,self.fs/2,spectrum.shape[-1])
            la = ax[0,1].get_lines()
            la[-1].remove()
            line2, = self.ax[0,1].plot(self.x2,np.absolute(self.y2),"-", color='blue')
            #line, = self.ax[0,1].plot(freq,spectrum,"-", color='red')
            line, = self.ax[0,1].plot(freq,np.absolute(spectrum),"-", color='red')
            plt.draw()

        if event.inaxes is ax[1,0]:
            x3, y3 = event.xdata, event.ydata
            global x3fi
            x3fi = min(np.searchsorted(self.x3, x3), len(self.x3) - 1)
            y3 = self.y3
            print(y3.shape)
            window = np.zeros((y3.shape[-1]))
            window[x3in:x3fi] = 1.0
            sig = np.fft.ifftshift(y3*window)
            sig = np.fft.ifft(sig)
            t = np.linspace(0,self.dt*y3.shape[-1],y3.shape[-1])
            lb = ax[1,1].get_lines()
            lb[-1].remove()
            line4, = self.ax[1,1].plot(self.x4,self.y4,'-', color='blue')
            line, = self.ax[1,1].plot(t,sig,"-", color='red')
            plt.draw()

        if event.inaxes is ax[0,1]:
            x2, y2 = event.xdata, event.ydata
            global x2fi
            x2fi = x2
            self.vline2.set_xdata([x2fi])
            self.text1.set_text(f'Freq={abs(x2fi-x2in):1.5f} Hz')
            plt.draw()

        if event.inaxes is ax[1,1]:
            x4, y4 = event.xdata, event.ydata
            global x4fi
            x4fi = x4
            self.vline4.set_xdata([x4fi])
            self.text2.set_text(f'Time={abs(x4fi-x4in):1.5f} s')
            plt.draw()
            
folder = int(sys.argv[1])# 800
AQ = float(sys.argv[2]) #29.999
DW = float(sys.argv[3]) * 1.0e-6 #125.0e-6
dt = 2 * DW
fs = 1.0/dt
path = os.getcwd()
path = path + '/' + str(folder) + '/fid'
data = np.fromfile(path,dtype=np.int32)
Mx = data[0::2]
My = data[1::2]
sig = Mx + 1j * My
t = np.linspace(0.0,AQ,Mx.shape[-1])

spec = np.fft.fft(sig)
spec = np.fft.fftshift(spec)
freq = np.linspace(-fs/2,fs/2,sig.shape[-1])	

# --------- Fourier Plotting

fig, ax = plt.subplots(2,2)
plt.figure(1, figsize=(20, 20))

line1, = ax[0,0].plot(t,sig,"-", color='green')
ax[0,0].set_xlabel("time [s]")
ax[0,0].set_ylabel("signal" )
ax[0,0].grid()

vline1 = ax[0,1].axvline(color='k', lw=0.8, ls='--')
vline2 = ax[0,1].axvline(color='k', lw=0.8, ls='--')
text1 = ax[0,1].text(0.0, 0.0, '', transform=ax[0,1].transAxes)
line2, = ax[0,1].plot(freq,spec,"-", color='green')
ax[0,1].set_xlabel("Frequency [Hz]")
ax[0,1].set_ylabel("spectrum" )
#ax[0,1].set_xlim(0,40)
ax[0,1].grid()

line3, = ax[1,0].plot(freq,spec,"-", color='green')
ax[1,0].set_xlabel("Frequency [Hz]")
ax[1,0].set_ylabel("spectrum" )
#ax[1,0].set_xlim(0,40)
ax[1,0].grid()

vline3 = ax[1,1].axvline(color='k', lw=0.8, ls='--')
vline4 = ax[1,1].axvline(color='k', lw=0.8, ls='--')
text2 = ax[1,1].text(0.0, 0.0, '', transform=ax[1,1].transAxes)
line4, = ax[1,1].plot(t,sig,"-", color='green')
ax[1,1].set_xlabel("time [s]")
ax[1,1].set_ylabel("signal" )
ax[1,1].grid()

fourier = Fourier1(Mx,My,ax,fig,line1,line2,line3,line4,vline1,vline2,vline3,vline4,text1,text2)
fig.canvas.mpl_connect("button_press_event",fourier.button_press)
fig.canvas.mpl_connect("button_release_event",fourier.button_release)
plt.show()



