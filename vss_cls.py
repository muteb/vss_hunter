import win32com.client
from datetime import datetime

class vss:
    def __init__(self):
        self.wcd = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        self.wmi = self.wcd.ConnectServer(".", "root\cimv2")
        self.colItems = self.wmi.ExecQuery("SELECT * FROM Win32_ShadowCopy")

    def WMIDateStringToDate(self,dtmDate):
        sepeartor = ''
        if "+" in dtmDate:
            dtUTCplus = int(dtmDate.split("+")[1]) / 60
            sepeartor = '+'
            print("TimeZone: " + sepeartor + str(dtUTCplus))
        else:
            dtUTCminus = (dtmDate.split("-")[1]) / 60
            sepeartor = '-'
            print("TimeZone: " + sepeartor + str(dtUTCminus))
        dtdateTime = dtmDate.split(sepeartor)[0]
        dtmDate = dtmDate + '0'
        strDateTime =datetime.strptime(dtdateTime, '%Y%m%d%H%M%S.%f')
        return strDateTime.isoformat()

    def get_devicesIDs(self):
        devcID = []
        for objItem in self.colItems:
            dict2={}
            if objItem.InstallDate != None:
                Datec= self.WMIDateStringToDate(objItem.InstallDate)
                dict2['date'] = Datec
            if objItem.DeviceObject != None:
                DeviceObject = str(objItem.DeviceObject)
                dict2['ID'] = DeviceObject
            devcID.append(dict2)
        return devcID