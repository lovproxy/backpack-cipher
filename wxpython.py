import wx
import wx.grid as gridlib
from core import *

class Window(wx.Frame):

	def __init__(self, parent, title,c):
		wx.Frame.__init__(self, parent, title = title, size = (600,600))
		#myGrid = gridlib.Grid(self)
		self.cmh = c
		#myGrid.CreateGrid(1, 2)
		#self.outp = wx.Panel(self)
		#self.inp = wx.Panel(self, pos=(0, 50))
		self.fgs = wx.BoxSizer(wx.HORIZONTAL)
		self.texts = wx.BoxSizer(wx.VERTICAL)
		self.fgs.Add(self.texts)
		self.rcont= wx.BoxSizer(wx.VERTICAL)
		self.fgs.Add(self.rcont, proportion=1, flag=wx.EXPAND|wx.TOP, border=10)
		self.textc1 = wx.TextCtrl(self, style = wx.TE_MULTILINE, size=(400,150))
		self.textc2 = wx.TextCtrl(self, style = wx.TE_MULTILINE, size=(400,150))
		self.texts.Add(self.textc1)
		self.texts.Add(self.textc2)
		self.SetSizer(self.fgs)

		self.cb = wx.ComboBox(self, choices=list(self.cmh.cont.keys()), style=wx.CB_READONLY)
		self.cb.SetSelection(0)
		self.rcont.Add(self.cb, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=80)
		bdecrypt = wx.Button(self,label='Decrypt', size=(50,50))
		bencrypt = wx.Button(self,label='Encrypt', size=(50,50))
		self.rcont.Add(bdecrypt, flag=wx.ALIGN_CENTER|wx.BOTTOM)
		self.rcont.Add(bencrypt, flag=wx.ALIGN_CENTER|wx.BOTTOM)
		bencrypt.Bind(wx.EVT_BUTTON, self.onEncrypt)
		bdecrypt.Bind(wx.EVT_BUTTON,self.onDecrypt)

		menu = wx.Menu()
		importItem = menu.Append(wx.ID_ADD,'Import contact','Добавить контакт')
		aboutItem = menu.Append(wx.ID_ABOUT, "About","Push the button to get an information about this application")
		menu.Append(wx.ID_EXIT, "Exit", "Push the button to leave this application")
		bar = wx.MenuBar()
		bar.Append(menu,"File")
		self.SetMenuBar(bar)
		self.Bind(wx.EVT_MENU, self.OnAbout,aboutItem)
		self.Show(True)
		self.Bind(wx.EVT_MENU,self.OnExit)
		self.Bind(wx.EVT_MENU,self.OnAppend,importItem)

	def OnAppend(self,x):
		Fd = wx.FileDialog(self, "Открыть файл...", wildcard="Файлы контактов рюкзачного шифра (*.cg)|*.cg",\
						   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		Fd.ShowModal()
		with open(Fd.GetPath()) as f, open('cont.g','r') as c:
			stroki = f.readlines()
			strokic = c.readlines()
			stroki.append('*****\n')
			strokic.extend(stroki)
			z = int(strokic[0])
			z +=1
			strokic[0] = str(z) + '\n'
			print(strokic)
		with open('cont.g','w') as e:
			e.writelines(strokic)
		self.cmh.UpdateCont()
		self.cb.Clear()
		for nm in self.cmh.cont.keys():
			self.cb.Append(nm)
		self.cb.SetSelection(0)



	def onEncrypt(self,x):
		msg = self.textc1.GetValue()
		txt = self.cmh.encrypt(self.cb.GetStringSelection(),msg)
		self.textc2.write(str(txt))
		print(msg.encode('utf-8'))


	def onDecrypt(self,x):
		ch = self.textc2.GetValue()
		chifr = ch[1:len(ch)-1].split(', ')
		chifr = [int(x) for x in chifr]
		txt = self.cmh.decrypt(chifr,self.cb.GetStringSelection())
		self.textc1.write(str(txt))


	def OnAbout(self,x):
		dlg = wx.MessageDialog(self, "Эта программа выполняет алгоритм рюкзачного шифрования и расшифрования", "О программе",wx.OK)
		dlg.ShowModal()

	def OnExit(self,x):
		self.Close()

c = mh()
app = wx.App()
wnd = Window(None, "Рюкзачный алгоритм",c)
app.MainLoop()

# считывания ключей из файлов которые там есть и формировать из них список/словарь.
# заполнять таблицу тем ,что мы считали
# кнопочки на панель расшифровать/зашифровать
# кнопка расшифровать только для пользователя с фулл инфой, чтобы кнопка гасла.