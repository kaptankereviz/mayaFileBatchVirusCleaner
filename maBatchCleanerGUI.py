import tkinter as tk
from tkinter import filedialog
import webbrowser
import os
import subprocess

def getInfectedMayaFiles(root_dir):
  ''' '''
  infected_string = '$zifu_jiance_name_kaitou'
  maya_files = []
  for root, d, mafiles in os.walk(root_dir):
    for mafile in mafiles:
      if mafile.endswith('.ma'):
        full_path = os.path.join(root, mafile)
        f = open(full_path, 'r')
        contents = f.read()
        f.close()
        if infected_string in contents:
          maya_files.append(full_path.replace('/', '\\'))
  return maya_files


def fix_file_for_windows(mayapath, filepath):
  command = f'"{mayapath}" -batch -file "{filepath}" -command "evalDeferred (\\"loadPlugin MayaScanner; MayaScan;\\")"'
  subprocess.call(command)



class MaBatchCleaner:
  ''' '''
  def __init__(self):
    super().__init__()
    self.window = tk.Tk()
    self.window.title('maFile CoronaVirus Batch Temizleyici... KaptanKereviz (Bug check yapmadım ama calisiyor olmasi lazim)')
    self.window.geometry('900x600')
    self.buildUI()
    self.window.mainloop()
    self.root_dir = ''
    self.maya_path = ''
    self.infected_files = []

  def buildUI(self, *args):
    # titles roadmap
    self.ui_title_1 = tk.Label(self.window, text='Once suradan maya plugin\'ini indirip kurun ---> ')
    self.ui_au_site_link = tk.Button(self.window, text='Autodesk sitesi', command=self.goAutodeskSite)
    self.ui_title_1.grid(column=0, row=0)
    self.ui_au_site_link.grid(column=1, row=0)
    self.ui_separator_01 = tk.Label(self.window, text='')
    self.ui_separator_01.grid(column=0, row=1)

    # maya.exe dosyası path'i
    self.ui_mayaexe_path = tk.Label(self.window, text='Maya dosyası nerede? (c:/program files/autodesk/maya????/bin/maya.exe) --->')
    self.ui_mayaexe_path_button = tk.Button(self.window, text='Bakayim nerede', command=self.setMayaPath)
    self.ui_mayaexe_path.grid(column=0, row= 3)
    self.ui_mayaexe_path_button.grid(column=1, row=3)
    self.ui_separator_02 = tk.Label(self.window, text='')
    self.ui_separator_02.grid(column=0, row=4)

    # root folder selection
    self.ui_root_dir = tk.Label(self.window, text="Taranacak dosyalar icin baslangic klasorunu secin --->")
    self.ui_root_dir_browse = tk.Button(self.window, text="Arama klasörünü seceyim", command=self.setRootDir)
    self.ui_root_dir.grid(column=0, row=5)
    self.ui_root_dir_browse.grid(column=1, row=5)
    self.ui_separator_03 = tk.Label(self.window, text='')
    self.ui_separator_03.grid(column=0, row=6)
    self.ui_list_label = tk.Label(self.window, text='Muhtemel viruslu dosyalar bunlar:')
    self.ui_list_label.grid(column=0, row=7)

    # possible infected files list
    self.ui_infected_list = tk.Listbox(self.window, width=140, height=20)
    self.ui_infected_list.grid(column=0, row=8, columnspan=2)

    # fix buttons
    self.ui_fix_all_button = tk.Button(self.window, text="Hepsini duzeltmeye calis (biraz surebilir)", width=100, command=self.fixAll)
    self.ui_fix_all_button.grid(column=0, row=9, columnspan=2)


  def goAutodeskSite(self, *args):
    webbrowser.open('https://apps.autodesk.com/MAYA/en/Detail/Index?id=8637238041954239715&os=Win64&appLang=en&_ga=2.161697466.728507207.1593459874-1842720612.1593267195')

  def setMayaPath(self, *args):
    self.maya_path = filedialog.askopenfilename()
    if self.maya_path and self.maya_path.endswith('maya.exe'):
      self.maya_path = self.maya_path.replace('/', '\\')
      self.ui_mayaexe_path.configure(text = self.maya_path)


  def setRootDir(self, *args):
    self.root_dir = filedialog.askdirectory()
    if self.root_dir:
      self.ui_root_dir.configure(text = self.root_dir)
      self.populateList()

  def populateList(self, *args):
    if self.root_dir:
      self.infected_files = getInfectedMayaFiles(self.root_dir)
      for f in self.infected_files:
        self.ui_infected_list.insert(tk.END, f)
    
  def fixAll(self, *args):
    if self.root_dir and self.infected_files and self.maya_path:
      for f in self.infected_files:
        fix_file_for_windows(self.maya_path, f)
        self.ui_infected_list.delete(0)
        self.window.update()
        self.window.update_idletasks()

if __name__ == '__main__':
  gui = MaBatchCleaner()
