import mechanize
from BeautifulSoup import BeautifulSoup
import re
import os
from Tkinter import *
import tkFileDialog
import tkMessageBox


class SearchApp():
	def __init__(self):
		self.master = Tk()
		self.master.geometry('450x400+250+250')
		self.master.title('Lolking Tool Gui')
		self.master.mlabel = Label(self.master, text="Welcome to lolking Searching Tool").pack()
		self.master.mbutton4 = Button(self.master, text='please Select Your LOL R3d log directory', command=self.askdirectory)
		self.master.mbutton4.pack()
		self.master.mlabel2 = Label(self.master, text="").pack()
		self.master.mbutton1 = Button(self.master, text = 'Search', command = self.loking).place(x=250, y=350)
		self.master.mbutton2 = Button(self.master, text = 'Clear All', command = self.mlremove).place(x=300, y=350)
		self.master.mbutton3 = Button(self.master, text = 'Exit Program', command = self.exit).place(x=360, y=350)
		self.userlist = []
		self.dir = 'C:'



	def askdirectory(self):
		self.dir = tkFileDialog.askdirectory(initialdir='C:',  title='please select League of Legends/logs/Game - R3d Logs')


	def run(self):
		self.master.mainloop()

	def mlremove(self):
		try: 
			for i in self.userlist:
				i.pack_forget()
		except AttributeError:
			pass

		self.userlist = []


#	def loking(self):
#		for x in range(8):
#			x = str(x)
#			exec('self.master.ml%s = Label(self.master, text="Label%s")' %  (x, x))
#			exec("self.master.ml%s.pack()" % x)

	def exit(self):
		self.master.destroy()

	def loking(self):
		if len(self.userlist) != 0:
			tkMessageBox.showerror("List not empty", "please clean the list first")
			pass
		else:

			# Browser
			br = mechanize.Browser()			

			# Cookie Jar
			cj = mechanize.LWPCookieJar()
			br.set_cookiejar(cj)			

			# Browser options
			br.set_handle_equiv(True)
			#br.set_handle_gzip(True)
			br.set_handle_redirect(True)
			br.set_handle_referer(True)
			br.set_handle_robots(False)			

			# Follows refresh 0 but not hangs on refresh > 0
			br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)			

			# User-Agent
			br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]	
			
					

			# load R3d logs file from client
			try:
				ch2r3d = os.chdir(self.dir)
				lr3d = os.listdir(".")
				lr3d.sort()
				f= open(lr3d[-1], 'r')		

				r3dlog = f.readlines()
				nl = []
				for l in r3dlog:
					if re.match("^.*created for", l.split("|")[-1]):
						nl.append(l.split("|")[-1])				

				f.close()
				userlist = []
				for x in nl:
					a = x.split("for ")[-1]
					b = a.split("\n")[0]
					userlist.append(b)	
			
	#			userlist = ["theoddone"]		

				# web starting
				for sname in userlist:
					sn = sname.replace(" ", "+")
					
					link = "http://www.lolking.net/search?name=" + sn
				
					t = br.open(link)
					html = t.get_data()
					soup = BeautifulSoup(html)
					for search_result in soup.findAll('div', attrs={'class': 'search_result_item'}):
						trim = search_result.getText('|').split('|')
						lbname = trim[2].replace(" ", '_')
						if "North America" in trim:
							#print "player [" + trim[2] + "]:" + " rank " + " ".join(trim[3:])
							#mlabel = Label(mGui, text="[" + trim[2] + "]:" + " rank " + " ".join(trim[3:]), fg='blue').pack()
							txt = '[' + trim[2] + ']:' + ' rank ' + ' '.join(trim[3:])
							exec("self.master.ml%s = Label(self.master, text='%s', fg='blue')" %  (lbname, txt))
							exec("self.master.ml%s.pack()" % lbname)
							exec("self.userlist.append(self.master.ml%s)" % lbname)		

				self.master.mbutton4.pack_forget()
			except:
				tkMessageBox.showerror("Directory Error", "please select a correct lol R3d log directory")
			
