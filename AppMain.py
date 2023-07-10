from AppUI import RootUI, ManagerComUI
from AppSerial import SerialControl
from AppData import AppData

RootMain = RootUI()
AppSerial = SerialControl()
AppData = AppData()

ManagerComUI(RootMain.root, AppSerial, AppData)

RootMain.root.mainloop()