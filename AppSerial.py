import serial.tools.list_ports
import time

class SerialControl():
    def __init__(self):
        pass
    
    def getComList(self):
        ports = serial.tools.list_ports.comports()
        self.comList = [com[0] for com in ports]
        self.comList.insert(0, "-")
    
    def SerialOpen(self, ManagerComUI):
        try:
            self.ser.is_open
        except:
            PORT = ManagerComUI.clickedCom.get()
            BAUD = ManagerComUI.clickedBd.get()
            
            self.ser = serial.Serial()
            self.ser.baudrate = BAUD
            self.ser.port = PORT
            self.ser.timeout = 0.1
        
        try:
            if self.ser.is_open:
                print("Already Open")
                self.ser.status = True
            else:
                PORT = ManagerComUI.clickedCom.get()
                BAUD = ManagerComUI.clickedBd.get()
                self.ser = serial.Serial()
                self.ser.baudrate = BAUD
                self.ser.port = PORT
                self.ser.timeout = 0.1
                self.ser.open()
                self.ser.status = True
        except:
            self.ser.status = False
    
    def SerialClose(self, ManagerComUI):
        try:
            self.ser.is_open
            self.ser.close()
            self.ser.status = False
        except:
            self.ser.status = False
    
    def SerialSync(self, gui):
        self.threading = True
        time.sleep(0.2)
        
        while self.threading:
            try:
                gui.data.msg = self.ser.readline()
                gui.data.DecodeData()
                # print(gui.data.msg)
                gui.monitor.updateData(gui.data.msg.rstrip('\n'))
                
            except Exception as e:
                print(e)
            

if __name__ == "__main__":
    pass