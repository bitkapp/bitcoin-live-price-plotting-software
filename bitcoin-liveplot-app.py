import time,json,urllib2          
from matplotlib import pyplot as pl
import numpy as np
import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import OrderedDict

# Created By BitKapp.com
# This software is released under GNU License
# (c) 2013
# Donate at 1Bc9Jr8rxcp3be4DUHfVdSh3sZ9My9pqog

running_time = 1000  
end_time = time.time() + running_time
yaxis_scale = 1.5

currencies = OrderedDict([('US Dollar','USD'),('British Pound','GBP'),('Euro','EUR')])
init_curr = 1
currency = currencies[currencies.keys()[0]]
curr_links = {'USD':'https://data.mtgox.com/api/2/BTCUSD/money/ticker_fast',
  	'GBP':'https://data.mtgox.com/api/2/BTCGBP/money/ticker_fast',
		'EUR':'https://data.mtgox.com/api/2/BTCEUR/money/ticker_fast' }
curr_symbol = {'USD':'$','GBP':u'\u00A3','EUR':u'\u20AC'}

#Price Request Function
def req_price(url):
	url_read = urllib2.urlopen(url)
	read = url_read.read()
	dec_json = json.loads(read)['data']['last']['value']
	return dec_json
	
price=[req_price(curr_links[currency])]   
t_out = [time.time()]

line, = pl.plot(t_out,price)
pl.title("Bitcoin Price Live Plot")
pl.xlabel("Time")

#Defining the Time Labels in Human format
def time_labels():
	t_label = []
	label_points = running_time/200 + 2

	t_label_range = range (0, running_time, running_time/label_points) 
	for i in t_label_range:
		t_label.append(time.strftime("%H:%M:%S", time.localtime(time.time()+i)))
	pl.xlim([time.time(),time.time()+running_time])
	pl.xticks(np.arange(time.time(),time.time()+running_time,running_time/label_points),t_label)
	
time_labels()

#AutoUpdating Y-Axis
def yaxisupdate(scale):
	pl.ylabel('Price' + ' ' + '('+ currency + ')')
	ylim = round(float(price[-1]),1)
	ylimd = round(float(price[-2]),1)
	if ylim < ylimd-(scale/2):
		pl.ylim([ylimd-scale,ylimd+scale])
		ylim = ylimd
	if ylim > ylimd+(scale/2):
		pl.ylim([ylimd-scale,ylimd+scale])
		ylim = ylimd
	else:
		pl.ylim([ylim-scale,ylim+scale])
	
#Color of the Line changes if price goes up or down	
def linecolor():
	if price[-1] > price[-2]:
		line.set_color("green")
	if price[-1] < price[-2]:
		line.set_color("red")
	if price[-1] == price[-2]:
		line.set_color("blue")
	
#Updates plot with new information
def update_plot():
	global end_time,price,t_out
	if time.time() >= end_time:
		time_labels()
		end_time = time.time() + running_time
	price_now=req_price(curr_links[currency])
	price.append(price_now)
	t_out.append(time.time())
	yaxisupdate(yaxis_scale)
	linecolor()
	line.set_xdata(t_out)
	line.set_ydata(price)

#GUI Class	
class App(object):
	
	def __init__(self):
		global currencies
		self.root = Tkinter.Tk()
		self.root.wm_title("BitKapp Live Plot") 
		
		self.fig = pl.figure(1)
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
		self.canvas.show()
		
		self.button = Tkinter.Button(master=self.root, text = 'Exit', font=(13), command = self._quit)
		
		self.refresh_scale = Tkinter.Scale(master=self.root, label= 'Request Time:', from_=10, to=60, orient=Tkinter.HORIZONTAL )
		self.refresh_scale.set(10)
		
		self.yaxis = Tkinter.Scale(master=self.root, label='Price Scale:', from_=0.5, to = 5, orient=Tkinter.HORIZONTAL)
		self.yaxis.set(1.5)
		
		self.v = Tkinter.StringVar()
		self.label = Tkinter.Label(master = self.root, textvariable = self.v, font=("Arial",16))
		
		self.var = Tkinter.StringVar()
		self.currencies = currencies.keys()
		self.var.set(self.currencies[0])
		args = [self.root,self.var] + self.currencies
		keyw = {'command':self.curr}
		self.option = Tkinter.OptionMenu(*args,**keyw)
	
	#Defining the Currency according to the Menu
	def curr(self,e):
		global currency,price,t_out
		currency = currencies[self.var.get()]
		price = [req_price(curr_links[currency])]
		t_out = [time.time()]
		time_labels()
		
	def _quit(self):
		self.root.quit()
		self.root.destroy()
	
	#Updating the GUI
	def update(self):
		global yaxis_scale
		yaxis_scale = self.yaxis.get()
		update_plot()
		self.canvas.draw()
		self.v.set('Current Price: ' +curr_symbol[currency]+' ' + str(price[-1]))
		self.root.after(1000*(self.refresh_scale.get()),self.update)
		
	def run(self):
		self.button.grid(row=2,column=3,rowspan=2)
		self.canvas._tkcanvas.grid(row = 1, column=1,columnspan = 3)
		self.label.grid(row=2,column=1)
		self.refresh_scale.grid(row=2,column =2)
		self.yaxis.grid(row=3,column=2)
		self.option.grid(row=3,column=1)
		self.root.after(10,self.update)
		self.root.protocol("WM_DELETE_WINDOW", self._quit)
		self.root.mainloop()
	

if __name__ == '__main__':
	try:
		App().run()
	except:
		App()._quit()
			
