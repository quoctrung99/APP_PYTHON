import customtkinter 
import AppConstant as constant
from CTkMessagebox import CTkMessagebox

import threading

class RootUI():
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title("DC DC converter")
        self.root.geometry(f"{constant.WIDTH_SCREEN}x{constant.HEIGHT_SCREEN}")
       
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=6)
        
class ManagerComUI():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data
         
        self.frameCom = customtkinter.CTkFrame(master=self.root, corner_radius=12, border_width=2, border_color="black",
                                               bg_color=constant.COLOR_TRANSPARENT, fg_color=constant.COLOR_A)
        # self.frameData = customtkinter.CTkFrame(master=self.root, corner_radius=12, border_width=2, border_color="black",
        #                                         bg_color=constant.COLOR_TRANSPARENT, fg_color=constant.COLOR_TRANSPARENT)
        
        self.frameCom.grid(row=0, column=0, sticky=customtkinter.NSEW, padx = 10, pady = 24)
        # self.frameData.grid(row=0, column=1, sticky=customtkinter.NSEW, padx = 64, pady = 24)
        
        self.WidgetTitleCom()
        self.WidgetListCom()
        
        self.WidgetBaudRate()
        self.WidgetMonitorData()
        
        self.btnRefresh = customtkinter.CTkButton(master=self.frameCom, text="Refresh", command=self.ComRefresh)
        self.btnConnect = customtkinter.CTkButton(master=self.frameCom, text="Connect", command=self.SerialConnect, state="disabled")
        
        self.WidgetPublish()
    
    def WidgetTitleCom(self):
        self.label = customtkinter.CTkLabel(master=self.frameCom, text="Select COM:", 
                                            font=customtkinter.CTkFont(weight="bold", size=14, underline=True))    
        
        self.titleBd = customtkinter.CTkLabel(master=self.frameCom, text="BaudRate:",
                                              font=customtkinter.CTkFont(weight="bold", size=14, underline=True))
                                              
    def WidgetListCom(self):
        self.serial.getComList()
        self.clickedCom = customtkinter.StringVar()
        
        self.clickedCom.set(self.serial.comList[0])
        
        self.optionMenuCom = customtkinter.CTkOptionMenu(master=self.frameCom, variable=self.clickedCom, 
                                                         values=self.serial.comList, command=self.ConnectSerial)
    
    def WidgetBaudRate(self):
        self.clickedBd = customtkinter.StringVar()
        bds = [
            "-",
            "300",
            "600",
            "1200",
            "2400",
            "4800",
            "9600",
            "14400",
            "19200",
            "28800",
            "38400",
            "56000",
            "57600",
            "115200",
            "128000",
            "256000"
        ]
        self.clickedBd.set(bds[0])
        self.optionMenuBd = customtkinter.CTkOptionMenu(master=self.frameCom, variable=self.clickedBd, values=bds, command=self.ConnectSerial)
        
    def ConnectSerial(self, widget):        
        if "-" in self.clickedBd.get() or "-" in self.clickedCom.get():
            self.btnConnect.configure(state="disabled")
        else:
            self.btnConnect.configure(state="normal")
            self.btnConnect.configure(text="Connect")   
                                  
    def ComRefresh(self):
        self.optionMenuCom.destroy()
        self.WidgetListCom()
        self.btnConnect.configure(text="Connect") 
        
        self.optionMenuCom.grid(row=0, column=1)
        logic = []
        self.ConnectSerial(logic)
    
    def SerialConnect(self):
        if self.btnConnect.cget("text") in "Connect":
            self.serial.SerialOpen(self)

            if self.serial.ser.status:
                print("Connected")
                self.btnConnect.configure(text="Disconnect") 
                
                self.btnConnect.configure(state="disable")
                self.btnRefresh.configure(state="disable")
                
                self.optionMenuCom.configure(state="disable")
                self.optionMenuBd.configure(state="disable")
                
                InfoMsg = f"Successful UART connection using {self.clickedCom.get()}"
                CTkMessagebox(title="Info", message=InfoMsg)
                
                self.monitor = MonitorData(self.root, self.serial, self.data)
                
                # Start Sync threading
                self.serial.t1 = threading.Thread(target=self.serial.SerialSync, args=(self, ), daemon=True)
                self.serial.t1.start()

            else:
                ErrorMsg = f"Failure to estabish UART connection using {self.clickedCom.get()}"
                CTkMessagebox(title="Error", message=ErrorMsg, icon="cancel")
        else:
            self.serial.SerialClose(self)
            self.btnConnect.configure(text="Connect") 
            self.btnRefresh.configure(state="disable")
            self.optionMenuCom.configure(state="normal")
            self.optionMenuBd.configure(state="normal")
    
    def WidgetMonitorData(self):
        pass
        # self.dataMonitor = customtkinter.CTkLabel(master=self.frameData, font=customtkinter.CTkFont(weight="normal", size=14), text=self.data) 
            
    def WidgetPublish(self):
        #Title widget
        self.btnRefresh.grid(row=2, column=0, padx=12, pady=24)
        self.btnConnect.grid(row=2, column=1, padx=12, pady=24)
        
        self.label.grid(row=0, column=0, padx=8, pady=8)
        self.titleBd.grid(row=1, column=0, padx=8, pady=8)
        
        self.optionMenuCom.grid(row=0, column=1)
        self.optionMenuBd.grid(row=1, column=1)
        
        # self.dataMonitor.grid(row=0, column=2, padx=8, pady=8)

class MonitorData():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data
        
        self.frameData = customtkinter.CTkFrame(master=self.root, corner_radius=12, border_width=2, border_color="black",
                                                bg_color=constant.COLOR_TRANSPARENT, fg_color=constant.COLOR_TRANSPARENT, width=200, height=200)
        self.frameData.grid(row=0, column=1, sticky=customtkinter.NSEW, padx = 64, pady = 24)
        
        self.dataMonitor = customtkinter.CTkLabel(master=self.frameData, font=customtkinter.CTkFont(weight="normal", size=14), text="") 
        # self.dataMonitor.grid(row=0, column=2, padx=8, pady=8)
    
    def updateData(self, data):
        self.dataMonitor.configure(text=data)
        
        
if __name__ == "__main__":
    RootUI()
    ManagerComUI()
    # MonitorData()