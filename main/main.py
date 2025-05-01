import wx


class Window(wx.Frame):

	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (1000,1000))
		outp =wx.Panel(self)
		self.img = wx.Panel(self,pos =(0,50))
		#img.Create(self,pos =(0,100))
		self.fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
		self.img1 = wx.Image('ing.jpg',wx.BITMAP_TYPE_ANY)
		w , h = self.img1.GetWidth(), self.img1.GetHeight()
		img2 = self.img1.Scale(int(w/4),int(h/4))
		self.sb1 = wx.StaticBitmap(self.img, -1, wx.BitmapFromImage(self.img1.Scale(int(w/2),int(h/2))))
		self.sb2 = wx.StaticBitmap(self.img, -1, wx.BitmapFromImage(img2))
		self.fgs.Add(self.sb1)
		self.fgs.Add(self.sb2)
		self.img.SetSizerAndFit(self.fgs)
		outp.Fit()

	#TextCtrl(self, style = wx.TE_MULTILINE) # создаём текстовое поле
		self.Show(True)
		menu = wx.Menu() # создаём экземпляр меню
		aboutItem = menu.Append(wx.ID_ABOUT,"About","Push the button to get an information about this application") # добавляем подпункты к меню
		menu.Append(wx.ID_EXIT,"Exit","Push the button to leave this application") # а как ещё?
		bar = wx.MenuBar() # создаём рабочую область для меню
		bar.Append(menu,"File") # добавляем пункт меню
		self.SetMenuBar(bar) # указываем, что это меню надо показать в нашей форме
		self.Bind(wx.EVT_MENU, self.OnAbout,aboutItem)
		tb = self.CreateToolBar()
		btn = wx.Image('ok.png',wx.BITMAP_TYPE_ANY)
		w, h = btn.GetWidth(), btn.GetHeight()
		btn1 = btn.Scale(int(w/6),int(h/6))
		tb.AddTool(1,'rotate',btn1.ConvertToBitmap())
		tb.Realize()
		self.Bind(wx.EVT_TOOL,self.OnRotateRight, id=1)


	def OnRotateRight(self,e):
		self.img1 = self.img1.Rotate90(clockwise=True)
		newsb1 = wx.StaticBitmap(self.img1, -1, wx.BitmapFromImage(self.img1))
		#self.fgs.Add(newsb1)
		self.img.SetSizerAndFit(self.fgs)
		#newsb1 = self.img1.ConvertToBitmap()# sizer убрать и сделать две панели одну для двух панд,а на них нанести изображение.


	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "This is a mini editor keeping your text", "About pyNote",wx.OK)  # создаём всплывашку
		dlg.ShowModal()  # показываем окошко



app = wx.App()
wnd = Window(None, "pyNote")
app.MainLoop()
