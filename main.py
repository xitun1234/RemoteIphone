import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas
from giaodien import Ui_MainWindow
import random
import os
from PyQt5.QtCore import QMutex, QObject, QRunnable, QThread, Qt, QThreadPool, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import time
import datetime
import requests
import re
import json
from urllib.parse import urlparse, parse_qs
import pandas as pd

fileOwner = open("./Config/owner.txt", "r", encoding="utf-8")
listOwner = fileOwner.readlines()
owner = listOwner[0]


listDeviceDict = {
    "192.168.3.101": "1",
    "192.168.3.102": "2",
    "192.168.3.103": "3",
    "192.168.3.104": "4",
    "192.168.3.105": "5",
    "192.168.3.106": "6",
    "192.168.3.107": "7",
    "192.168.3.108": "8",
    "192.168.3.109": "9",
    "192.168.3.110": "10",
    "192.168.3.111": "11",
    "192.168.3.112": "12",
    "192.168.3.113": "13",
    "192.168.3.114": "14",
    "192.168.3.115": "15",
    "192.168.3.116": "16",
    "192.168.3.117": "17",
    "192.168.3.118": "18",
    "192.168.3.119": "19",
    "192.168.3.120": "20",
    "192.168.3.121": "21",
    "192.168.3.122": "22",
    "192.168.3.123": "23",
    "192.168.3.124": "24",
    "192.168.3.125": "25",
    "192.168.3.126": "26",
    "192.168.3.127": "27",
    "192.168.3.128": "28",
    "192.168.3.129": "29",
    "192.168.3.130": "30",
}


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    - finished: No data
    - error:`tuple` (exctype, value, traceback.format_exc() )
    - result: `object` data returned from processing, anything
    - progress: `tuple` indicating progress metadata
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(dict)
    progress = pyqtSignal(tuple)


class Remote(QRunnable):
    resultSignal = pyqtSignal(dict)
    resultTienTrinh = pyqtSignal()

    listDeviceDict = {
        "192.168.3.101": "1",
        "192.168.3.102": "2",
        "192.168.3.103": "3",
        "192.168.3.104": "4",
        "192.168.3.105": "5",
        "192.168.3.106": "6",
        "192.168.3.107": "7",
        "192.168.3.108": "8",
        "192.168.3.109": "9",
        "192.168.3.110": "10",
        "192.168.3.111": "11",
        "192.168.3.112": "12",
        "192.168.3.113": "13",
        "192.168.3.114": "14",
        "192.168.3.115": "15",
        "192.168.3.116": "16",
        "192.168.3.117": "17",
        "192.168.3.118": "18",
        "192.168.3.119": "19",
        "192.168.3.120": "20",
        "192.168.3.121": "21",
        "192.168.3.122": "22",
        "192.168.3.123": "23",
        "192.168.3.124": "24",
        "192.168.3.125": "25",
        "192.168.3.126": "26",
        "192.168.3.127": "27",
        "192.168.3.128": "28",
        "192.168.3.129": "29",
        "192.168.3.130": "30",
    }

    def __init__(self, urlRemote, scriptKho, ipMay, parent=None):
        super().__init__()
        self.signals = WorkerSignals()

        self.urlRemote = urlRemote
        self.scriptKho = scriptKho
        self.ipMay = ipMay
        self.mutex = QMutex()

    def playScript(self):
        response = requests.get(self.urlRemote, timeout=20)
        jsonData = response.json()
        print(jsonData["status"])

    def themDuLieuKho(self):
        data = self.scriptKho.split("|")
        dataPost = {
            "username": "",
            "password": "",
            "mail": "",
            "passMail": "",
            "twoFA": "",
            "owner": owner,
        }

        dataPost["username"] = data[0]
        dataPost["password"] = data[1]
        dataPost["twoFA"] = data[2]
        dataPost["mail"] = data[3]
        dataPost["passMail"] = data[4]
        # if (data[4] !=""):
        #     dataPost["twoFA"] = data[4]

        jsonData = json.dumps(dataPost)

        response = requests.post("http://lzd420.me/API/setkhodulieu", dataPost)
        print(response.json())

    def addDataAccount(self):
        dataParse = parse_qs(self.scriptKho)

        dataPost = {
            "username": dataParse["username"][0],
            "password": dataParse["password"][0],
            "phoneNumber": dataParse["phoneNumber"][0],
            "deviceName": dataParse["deviceName"][0],
            "address": dataParse["address"][0],
            "link": dataParse["link"][0],
            "owner": owner,
        }

        print(dataPost)
        response = requests.post("http://lzd420.me/API/setinfo", dataPost)
        print(response.json())

        time.sleep(0.5)
        response = requests.post("http://lzd420.me/API/setdatareg", dataPost)
        print(response.json())

    def themDuLieuKhoDatHang(self):

        data = self.scriptKho.split("|")

        file = open("./Config/dataDiaChi.txt", "r", encoding="utf-8")
        allLines = file.readlines()

        address = allLines[random.randrange(
            0, len(allLines))].replace("\n", "")

        dauSo = ['090', '093', '070', '076', '077', '078', '079', '091', '094', '081', '082',
                 '084', '085', '088', '096', '097', '098', '086', '032', '034', '035', '036', '037', '038', '039']
        soDienThoai = dauSo[random.randrange(0, len(
            dauSo))] + str(random.randint(100, 999)) + str(random.randint(1000, 9999))

        dataPost = {
            "username": "",
            "password": "",
            "address": "",
            "phoneNumber": "",
            "owner": owner
        }

        dataPost["username"] = data[0]
        dataPost["password"] = data[1]
        dataPost["address"] = address
        dataPost["phoneNumber"] = soDienThoai

        jsonData = json.dumps(dataPost)

        response = requests.post(
            "http://lzd420.me/API/setKhoDatHang", dataPost)
        print(response.json())

    def napAcc(self):
        self.mutex.lock()
        
        linkAPI = "http://lzd420.me/api/getKhoDatHang&deviceName=" + \
            self.listDeviceDict[self.ipMay] + "&owner=" + owner
        response = requests.get(linkAPI,timeout=10)
        jsonData = response.json()
        if (jsonData["status"] == 'success'):

            dataAcc = jsonData["data"]

            dataPost = {
                "username": dataAcc["username"],
                "password": dataAcc["password"],
                "phoneNumber": dataAcc["phoneNumber"],
                "deviceName": dataAcc["deviceName"],
                "address": dataAcc["address"],
                "link": "",
                "owner": owner
            }

            print(dataPost)
            response = requests.post("http://lzd420.me/API/setinfo", dataPost)
            print(response.json())

            result = {
                "status": True,
                "noiDung": "N???p Acc Th??nh C??ng"
            }
            self.signals.result.emit(result)
        elif (jsonData["status"] == 'fail'):
            result = {
                "status": False,
                "noiDung": "???? H???t Acc Trong Kho"
            }
            self.signals.result.emit(result)
        
        self.mutex.unlock()

    def capNhatLink(self):
        data = self.scriptKho.split("|")
        linkAPI = "http://lzd420.me/API/getinfo&deviceName=" + \
            data[1] + "&owner=" + owner 
        response = requests.get(linkAPI)
        dataJSON = (response.json())["data"]
        print(dataJSON)

        dataPost = {
            "username": dataJSON["username"],
            "password": dataJSON["password"],
            "phoneNumber": dataJSON["phoneNumber"],
            "deviceName": dataJSON["deviceName"],
            "address": dataJSON["address"],
            "link": data[0],
            "owner": owner
        }

        respSetInfo = requests.post("http://lzd420.me/API/setinfo", dataPost)
        print(respSetInfo.json())

    def locImei(self):
        index = 0
        for imei in self.scriptKho:

            resp = {
                "imei": "",
                "ngayKichHoat": "",
                "model": "",
                "content": "",
                "tienTrinh": str(index + 1)
            }
            resp["imei"] = imei

            url = 'https://csone.vn/api/mcs?ownerType=3&owner=0911111111&imei=' + imei
            # print(url)

            response = requests.get(url, timeout=5)
            jsonData = (response.json())

            messageContent = (jsonData["Item"]["Message"])
            if (messageContent == "Not yet activated"):
                resp["content"] = "Kh??ng c?? imei trong h??? th???ng"
            else:

                thoiGianKichHoat = self.convertToDate(
                    jsonData["Item"]["SurveyDate"])
                ngayBH = int(thoiGianKichHoat["date"])
                thangBH = int(thoiGianKichHoat["month"])

                resp["model"] = jsonData["Item"]["ModelCode"]
                resp["ngayKichHoat"] = thoiGianKichHoat["content"]

                if (thangBH == 8 and ngayBH >= 20) or (thangBH == 9):
                    #
                    # add imei
                    apiUpdateTrangThai = "https://lzd420.me/api/setImei"
                    dataPost = {
                        "imei": resp["imei"],
                        "model": resp["model"],
                        "ngayKichHoat": resp["ngayKichHoat"]
                    }

                    response1 = requests.post(apiUpdateTrangThai, dataPost)
                    print(response1.json())

                    resp["content"] = response1.json()["data"]["content"]

            self.signals.result.emit(resp)

            index = index + 1

            time.sleep(0.1)

    def convertToDate(self, ngayKichHoat):
        date = ngayKichHoat[(len(ngayKichHoat)-2):len(ngayKichHoat)]
        month = ngayKichHoat[(len(ngayKichHoat)-4):(len(ngayKichHoat)-2)]
        year = ngayKichHoat[0:4]

        content = date + "/" + month + "/" + year

        resp = {
            "date": date,
            "month": month,
            "year": year,
            "content": content
        }

        return resp


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./iconlzd.png"))
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Tool ??i???u Khi???n Iphone"))

        self.myListDevice = []
        self.initListDevice()

        # SHOW list ip may
        header = self.tableWidget_IPMay.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.showListMay()

        self.showCauHinh()

        # sshow list check imei
        headerCheckImei = self.tableWidget_CheckImei.horizontalHeader()
        headerCheckImei.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        headerCheckImei.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)

        # context menu cho show list may
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.chuotPhaiShowListMay)

        ##label success
        self.label_KetQuaChay.setText(str(""))

        ######## List Script #####################
        # I. Chuc Nang Reg Acc
        # 1. Xoa Info
        listScriptXoaInfo = {
            "Full X??a Info": "/RemoteWifi/Part1-RegAccXoaInfo.js",
            "Ch??? X??a Info - M??? App Fake": "/RemoteWifi/TienIch-XoaInfo.js",
        }

        for script in listScriptXoaInfo:
            self.comboBox_XoaInfo.addItem(script)

        # 2. Dang Nhap Bang FB
        listScriptDangNhapBangFB = {
            "????ng Nh???p B???ng FB": "/RemoteWifi/Part12-DangNhapQuaFB.js",
        }

        for script in listScriptDangNhapBangFB:
            self.comboBox_DangNhapBangFB.addItem(script)

        # 3. Add Mail & Lay Lai Mat Khau
        listScriptAddMail = {
            "Full Add Mail & L???y L???i MK": "/RemoteWifi/Part2-AddMail.js",
            "L???y L???i M???t Kh???u": "/RemoteWifi/Part3-LayLaiMatKhau.js",
            "?????i M???t Kh???u": "/RemoteWifi/LZD13-DoiMatKhauLZD.js",
            "?????i T??n T??i Kho???n": "/RemoteWifi/LZD12-DoiTenTaiKhoan.js",
            "V??o Khung Y??u Th??ch": "/RemoteWifi/Lazada-VaoKhungYeuThich.js",
        }

        for script in listScriptAddMail:
            self.comboBox_AddMail.addItem(script)

        # II. Cac Chuc Nang Dat Hang
        # 1. Mo App Lazada
        listScriptMoApp = {
            "M??? App Fake": "/RemoteWifi/TienIch-MoAppLZDFake.js",
            "M??? App G???c": "/RemoteWifi/TienIch-MoAppLazadaGoc.js",
            "[Ch???] App G???c": "/RemoteWifi/TienIch-ChiMoAppLazadaGoc.js",
            "[Ch???] App Fake": "/RemoteWifi/TienIch-ChiMoAppLazadaFake.js",
            "M??? App G???c - Xem G???n ????y": "/RemoteWifi/TienIch-MoAppVaoCaNhan.js",
        }

        for script in listScriptMoApp:
            self.comboBox_MoAppLZD.addItem(script)

        # 2. Dang Nhap Lazada
        listScriptDangNhapLZD = {
            "Full ????ng Nh???p": "/RemoteWifi/LZD1-DangNhapBangMatKhau.js",
            "Ch??? ????ng Nh???p - App Fake": "/RemoteWifi/LZD11-ChiDangNhapLZD.js",
        }

        for script in listScriptDangNhapLZD:
            self.comboBox_DangNhapLZD.addItem(script)

        # 3. Mo Link
        listScriptMoLink = {
            "M??? Link B??nh Th?????ng": "/RemoteWifi/TienIch-MoLink.js",
            "M??? Link App G???c": "/RemoteWifi/LZD3-MoLinkNhanh.js",
            
        }

        for script in listScriptMoLink:
            self.comboBox_MoLink.addItem(script)

        # 4. Tao Dia Chi
        listScriptTaoDiaChi = {
            "[HCM] - Qu???n T??n Ph??": "/RemoteWifi/TaoDiaChi-TanPhu.js",
            "[H?? N???i] - Thanh Oai - Full": "/RemoteWifi/TaoDiaChi-ThanhOai.js",
            "[H?? N???i] - Th?????ng T??n - Full": "/RemoteWifi/LZD2-TaoDiaChi.js",
            "[H?? N???i] - Long Bi??n - Full": "/RemoteWifi/TaoDiaChi-LongBien.js",
            "[H?? N???i] - Ho??ng Mai - Full": "/RemoteWifi/TaoDiaChi-HoangMai.js",
            "[H?? N???i] - Gia L??m - Full": "/RemoteWifi/TaoDiaChi-GiaLam.js",
            "[H?? N???i] - ?????ng ??a": "/RemoteWifi/TaoDiaChi-DongDa.js",
            "[H?? N???i] - H?? ????ng": "/RemoteWifi/TaoDiaChi-HaDong.js",
            "[HCM] - Qu???n 10 - P13": "/RemoteWifi/LZD22-DiaChiQuan10.js",
            "[HCM] - Qu???n 5": "/RemoteWifi/TaoDiaChi-Quan5.js",
            "[Click L??u ?????a Ch???]": "/RemoteWifi/TaoDiaChi-LuuDiaChi.js",
        }

        for script in listScriptTaoDiaChi:
            self.comboBox_TaoDiaChi.addItem(script)

        # III. Cac Tien Ich
        # 1. Tien Ich
        listScriptTienIch = {
            "?????i IP 4G": "/RemoteWifi/TienIch-DoiIP4G.js",
            "Respring": "/RemoteWifi/TienIch-Respring.js",
            "Press Home": "/RemoteWifi/TienIch-PressHome.js",
            "Unlock Screen": "/RemoteWifi/TienIch-UnlockScreen.js",
            "Lock Screen": "/RemoteWifi/TienIch-LockScreen.js",
        }

        for script in listScriptTienIch:
            self.comboBox_TienIch.addItem(script)

        # 2. Luu & Restore RRS
        listScriptRRS = {
            "L??u RRS Acc": "/RemoteWifi/XoaInfo-LuuRRS.js",
            "L??u RRS Khung 30K": "/RemoteWifi/XoaInfo-LuuRRSRegAcc.js",
            "Restore RRS": "/RemoteWifi/XoaInfo-Restore.js",
        }

        for script in listScriptRRS:
            self.comboBox_RRS.addItem(script)

        # combo box list script
        listScript = {
            "Theo D??i Shop": "/RemoteWifi/TienIch-TheoDoiShop.js",
            "Click Ho??n T???t": "/RemoteWifi/TienIch-ClickHoanTat.js",
            "Tr?????t T???i Khung MGG": "/RemoteWifi/TienIch-TruotToiKhungFreeShip.js",
            "Click Mua Ngay": "/RemoteWifi/TienIch-ClickMuaNgay.js",
            "Click Thu Th???p - M?? Gi???m Gi??": "/RemoteWifi/TienIch-ClickThuThap.js",
            "Th??m Gi??? H??ng X3": "/RemoteWifi/TienIch-ThemGioHangX3.js",
            "T???t Khung Voucher D???ch V???": "/RemoteWifi/TienIch-TatKhungDiaChi.js",
            "S???a ?????a Ch??? V??? Qu???n 10": "/RemoteWifi/TienIch-SuaDiaChiVeQuan10.js",
            "S???a ?????a Ch??? V??? Qu???n 5": "/RemoteWifi/TienIch-SuaDiaChiVeQuan5.js",
            "S???a ?????a Ch??? V??? Qu???n T??n Ph??": "/RemoteWifi/TienIch-SuaDiaChiVeQuanTanPhu.js",
            "Ch???p ????n H??ng": "/RemoteWifi/TienIch-ChupDonHang.js",
            
        }

        for script in listScript:
       
            self.comboBox_ListScript.addItem(script)
            
        # 2. Luu & Restore RRS
        listScriptRecord = {
            "Record - Thu Th???p M?? 30K": "/RemoteWifi/Lazada-ThuThapMa30K.js",
            "V??o Trang Apple": "/RemoteWifi/Record-VaoTrangApple.js",
            "V??o Trang Vivo": "/RemoteWifi/Record-VaoTrangVivo.js",
            "Vao Trang Realme": "/RemoteWifi/Record-VaoTrangRealme.js",
            "V??o Trang Xiaomi": "/RemoteWifi/Record-VaoTrangXiaomi.js",
            "Vivo X5 - Xanh": "/RemoteWifi/Record-VivoY12s-Xanh.js",
            "Vivo X5 - ??en": "/RemoteWifi/Record-VivoY12s-Den.js",
            "C21Y X5 - Xanh": "/RemoteWifi/Record-C21YXanhX5.js",
            "Poco X5 - ??en": "/RemoteWifi/Record-PocoX3ProX5Den.js",
            "Poco X5 - V??ng": "/RemoteWifi/Record-PocoX3ProX5Vang.js",
            
            "13 Pro Max 128GB - Xanh " : "/RemoteWifi/Record-13PM128GB-Xanh.js",
            "13 Pro Max 128GB - V??ng " : "/RemoteWifi/Record-13PM128GB-Vang.js",
            "13 Pro Max 128GB - Tr???ng " : "/RemoteWifi/Record-13PM128GB-Trang.js",
            "Ipad Gen 9 64GB - X??m " : "/RemoteWifi/Record-IPAD-Xam.js",
            "Ipad Gen 9 64GB - Tr???ng " : "/RemoteWifi/Record-IPAD-Trang.js",
        }

        for script in listScriptRecord:
            print(script)
            self.comboBox_ListScriptRecord.addItem(script)

        # button cac chuc nang
        # I
        # 1. Xoa Info
        self.menuXoaInfo = QMenu()
        self.menuXoaInfo.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptXoaInfo[self.comboBox_XoaInfo.currentText()]))

        self.pushButton_FullXoaInfo.setMenu(self.menuXoaInfo)
        self.add_menu(self.myListDevice, self.menuXoaInfo)

        # 2. ????ng nh???p b???ng fb
        self.menuDangNhapFB = QMenu()
        self.menuDangNhapFB.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptDangNhapBangFB[self.comboBox_DangNhapBangFB.currentText()]))

        self.pushButton_DangNhapBangFB.setMenu(self.menuDangNhapFB)
        self.add_menu(self.myListDevice, self.menuDangNhapFB)

        # 3. Add mail & lay lai mat kahu
        self.menuAddMail = QMenu()
        self.menuAddMail.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptAddMail[self.comboBox_AddMail.currentText()]))

        self.pushButton_FullAddMail.setMenu(self.menuAddMail)
        self.add_menu(self.myListDevice, self.menuAddMail)

        # II. Cac chuc nang dat hang
        # 1. Mo App LZD
        self.menuMoAppLZD = QMenu()
        self.menuMoAppLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptMoApp[self.comboBox_MoAppLZD.currentText()]))

        self.pushButton_MoAppLZD.setMenu(self.menuMoAppLZD)
        self.add_menu(self.myListDevice, self.menuMoAppLZD)

        # 2. Dang Nhap LZD
        self.menuDangNhapLZD = QMenu()
        self.menuDangNhapLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptDangNhapLZD[self.comboBox_DangNhapLZD.currentText()]))

        self.pushButton_DangNhapLZD.setMenu(self.menuDangNhapLZD)
        self.add_menu(self.myListDevice, self.menuDangNhapLZD)

        # 3. Mo Link LZD
        self.menuMoLink = QMenu()
        self.menuMoLink.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptMoLink[self.comboBox_MoLink.currentText()]))

        self.pushButton_MoLink.setMenu(self.menuMoLink)
        self.add_menu(self.myListDevice, self.menuMoLink)

        # 4. Tao Dia Chi
        self.menuTaoDiaChi = QMenu()
        self.menuTaoDiaChi.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptTaoDiaChi[self.comboBox_TaoDiaChi.currentText()]))

        self.pushButton_TaoDiaChi.setMenu(self.menuTaoDiaChi)
        self.add_menu(self.myListDevice, self.menuTaoDiaChi)
        
        
        ### III. Cac chuc nang tien ich
        # 1. Tien Ich
        self.menuTienIch = QMenu()
        self.menuTienIch.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptTienIch[self.comboBox_TienIch.currentText()]))

        self.pushButton_TienIch.setMenu(self.menuTienIch)
        self.add_menu(self.myListDevice, self.menuTienIch)
        
        # 2. RRS Xoa Info
        self.menuRRS = QMenu()
        self.menuRRS.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptRRS[self.comboBox_RRS.currentText()]))

        self.pushButton_RRS.setMenu(self.menuRRS)
        self.add_menu(self.myListDevice, self.menuRRS)
        
        # 3. Cac chuc nang phu
        self.menuChucNangPhu = QMenu()
        self.menuChucNangPhu.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScript[self.comboBox_ListScript.currentText()]))

        self.pushButton_RunScript.setMenu(self.menuChucNangPhu)
        self.add_menu(self.myListDevice, self.menuChucNangPhu)  
        
        # 4. Record
        self.menuRecord = QMenu()
        self.menuRecord.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptRecord[self.comboBox_ListScriptRecord.currentText()]))

        self.pushButton_Record.setMenu(self.menuRecord)
        self.add_menu(self.myListDevice, self.menuRecord)  
        
              

        # tao menu
        listDevice = []
        menuStop = []
        listDevice.append("START")
        for device in self.myListDevice:
            if (device.find("192") != -1):
                listDevice.append(device)
                menuStop.append(device)

        listDevice.append({'STOP': menuStop})
        print(listDevice)

        # add menu click dat hang
        self.menuClickDatHang = QMenu()
        self.menuClickDatHang.triggered.connect(
            lambda x: self.playScriptDatHang(x.text(), "/RemoteWifi/LZD4-ClickDatHang.js"))

        # add menu N???p Acc Kho LZD
        self.menuNapAcc = QMenu()
        self.menuNapAcc.triggered.connect(lambda x: self.napAccLZD(x.text()))

        self.pushButton_ClickDatHang.setMenu(self.menuClickDatHang)
        self.pushButton_NapAccVaoMay_2.setMenu(self.menuNapAcc)

        ########## ADD MENU ############
        self.add_menu(self.myListDevice, self.menuClickDatHang)
        self.add_menu(self.myListDevice, self.menuNapAcc)

        # add menu Fake Version
        self.menuFakeVersionLZD = QMenu()
        self.menuFakeVersionLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-FakeVersionApp.js"))

        self.pushButton_FakeVersionApp.setMenu(self.menuFakeVersionLZD)
        self.add_menu(self.myListDevice, self.menuFakeVersionLZD)

        # Fake ten app
        self.menuFakeAll = QMenu()
        self.menuFakeAll.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-FakeAll.js"))

        self.pushButton_FakeTenApp.setMenu(self.menuFakeAll)
        self.add_menu(self.myListDevice, self.menuFakeAll)


        # pushButton_ThemDuLieu
        self.pushButton_ThemDuLieu.clicked.connect(self.ThemDuLieu)

        self.pushButton_ResetKho.clicked.connect(self.resetKho)

        # copy du lieu
        self.pushButton_CopyAccLZD.clicked.connect(self.getAccountLZD)
        self.pushButton_ExcelAccLZD.clicked.connect(self.xuatExcelAccLZD)
        self.pushButton_ExcelListImei.clicked.connect(self.xuatExcelListImei)

        self.pushButton_ThemDuLieuKhoLZD.clicked.connect(
            self.ThemDuLieuVaoKhoDatHang)
        self.pushButton_ResetKhoLZD.clicked.connect(self.resetKhoDatHang)
        self.pushButton_UpdateLinkChoMay.clicked.connect(
            self.updateLinkDatHang)

        # button Cap Nhat Trang Thai
        self.pushButton_CapNhatTrangThaiKhoDatHang.clicked.connect(
            self.capNhatTrangThaiKhoDatHang)

        # copy tai khoan && mat khau
        self.pushButton_CopyTaiKhoanKhoDatHang.clicked.connect(
            self.copyTaiKhoanKhoDatHang)

        self.pushButton_RefreshKhoDatHang.clicked.connect(
            self.showDataKhoDatHang)

        self.showDataKhoDatHang()

        # detect selected cell tableWidget_KhoDuLieuDatHang
        self.listAccountSelected = []
        self.tableWidget_KhoDuLieuDatHang.selectionModel(
        ).selectionChanged.connect(self.checkSelectAcc)

        # click button create imei 1000
        self.pushButton_Create1000Imei.clicked.connect(self.create1000Imei)

        self.pushButton_LocImei.clicked.connect(self.runLocImei)

        # luu cau hinh fake
        self.pushButton_LuuCauHinhFake.clicked.connect(self.luuCauHinhFake)
        
        
        
        ########################## 11-11-2021 ################################
        ########################### Vivo #####################################
        #Vao San Pham
        listScriptVaoSanPhamVivo = {
            "V??o S???n Ph???m Vivo Y12S": "/RemoteWifi/1111-VaoSanPham-Y12S.js",
           
        }

        for script in listScriptVaoSanPhamVivo:
            self.comboBox_SanSale_VaoTrangVivo.addItem(script)
            
        # Vao San Pham
        self.menuVaoSanPhamVivo = QMenu()
        self.menuVaoSanPhamVivo.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptVaoSanPhamVivo[self.comboBox_SanSale_VaoTrangVivo.currentText()]))

        self.pushButton_SanSale_VaoSanPhamVivo.setMenu(self.menuVaoSanPhamVivo)
        self.add_menu(self.myListDevice, self.menuVaoSanPhamVivo)
        
        #Vivo ?????t H??ng
        listScriptDatHangVivo= {
            "Mua - X10": "/RemoteWifi/1212-MuaX10-Y12s.js",
            "Y12S X5 - M??u xanh": "/RemoteWifi/1111-SanSale-Y12S-Xanh.js",
            "Y12S X5 - M??u ??en": "/RemoteWifi/1111-SanSale-Y12S-Den.js",
            "Y12S X5 - M??u xanh 2021": "/RemoteWifi/1111-SanSale-Y12S-Xanh-2021.js",
            "Y12S X5 - M??u ??en 2021": "/RemoteWifi/1111-SanSale-Y12S-Den-2021.js",
           
        }

        for script in listScriptDatHangVivo:
            self.comboBox_SanSale_VivoY12S.addItem(script)
            
        # Dat Hang Vivo
        self.menuDatHangVivo = QMenu()
        self.menuDatHangVivo.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptDatHangVivo[self.comboBox_SanSale_VivoY12S.currentText()]))

        self.pushButton_SanSale_DatHang_Y12S.setMenu(self.menuDatHangVivo)
        self.add_menu(self.myListDevice, self.menuDatHangVivo)
        
        
        ########################### Realme #####################################
        #Vao San Pham
        listScriptVaoSanPhamRealme = {
            "V??o S???n Ph???m C21Y": "/RemoteWifi/1111-VaoSanPham-C21Y.js",
            "V??o S???n Ph???m C11": "/RemoteWifi/1111-VaoSanPham-C11.js",
            "V??o S???n Ph???m Narzo": "/RemoteWifi/1111-VaoSanPham-Narzo.js",
           
        }

        for script in listScriptVaoSanPhamRealme:
            self.comboBox_SanSale_VaoTrangRealme.addItem(script)
            
        # Vao San Pham
        self.menuVaoSanPhamRealme = QMenu()
        self.menuVaoSanPhamRealme.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptVaoSanPhamRealme[self.comboBox_SanSale_VaoTrangRealme.currentText()]))

        self.pushButton_SanSale_VaoSanPham_Realme.setMenu(self.menuVaoSanPhamRealme)
        self.add_menu(self.myListDevice, self.menuVaoSanPhamRealme)
        
        #Realme ?????t H??ng
        #C21Y
        listScriptC21Y= {
            "C21Y X5 - M??u xanh": "/RemoteWifi/1111-SanSale-C21Y-Xanh.js",
           
        }

        for script in listScriptC21Y:
            self.comboBox_SanSale_RealmeC21Y.addItem(script)
            

        self.menuC21Y = QMenu()
        self.menuC21Y.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptC21Y[self.comboBox_SanSale_RealmeC21Y.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_C21Y.setMenu(self.menuC21Y)
        self.add_menu(self.myListDevice, self.menuC21Y)
        
        #C11
        listScriptC11= {
            "C11 X5 - M??u xanh": "/RemoteWifi/1111-SanSale-C11-Xanh.js",
            "C11 X5 - ??en": "/RemoteWifi/1111-SanSale-C11-Den.js",
           
        }

        for script in listScriptC11:
            self.comboBox_SanSale_RealmeC11.addItem(script)
            
        # Dat Hang Vivo
        self.menuC11 = QMenu()
        self.menuC11.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptC11[self.comboBox_SanSale_RealmeC11.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_C11.setMenu(self.menuC11)
        self.add_menu(self.myListDevice, self.menuC11)
        
        
        # Narzo 50i
        listScriptNarzo= {
            "Mua - X10": "/RemoteWifi/1212-MuaX10-Narzo.js",
            
            "Narzo X5 - M??u xanh": "/RemoteWifi/1111-SanSale-Narzo-Xanh.js",
            "Narzo X5 - ??en": "/RemoteWifi/1111-SanSale-Narzo-Den.js",
            
            "Xem ????n ?????t": "/RemoteWifi/1212-XemDonDat.js",
            
           
        }

        for script in listScriptNarzo:
            self.comboBox_SanSale_RealmeNarzo50.addItem(script)
            
        # Dat Hang Vivo
        self.menuNarzo = QMenu()
        self.menuNarzo.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptNarzo[self.comboBox_SanSale_RealmeNarzo50.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_Narzo50.setMenu(self.menuNarzo)
        self.add_menu(self.myListDevice, self.menuNarzo)
        
        
        ########################### Samsung #####################################
        #Vao San Pham
        listScriptVaoSanPhamSamsung = {
            "V??o S???n Ph???m A12": "/RemoteWifi/1111-VaoSanPham-A12.js",
            "V??o S???n Ph???m M32": "/RemoteWifi/1111-VaoSanPham-M32.js",
            "V??o S???n Ph???m Tab A7 Lite": "/RemoteWifi/1111-VaoSanPham-TabA7Lite.js",
            "V??o S???n Ph???m A03S": "/RemoteWifi/1111-VaoSanPham-A03S.js",
           
        }

        for script in listScriptVaoSanPhamSamsung:
            self.comboBox_SanSale_VaoTrangSamsung.addItem(script)
            
        # Vao San Pham
        self.menuVaoSanPhamSamsung = QMenu()
        self.menuVaoSanPhamSamsung.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptVaoSanPhamSamsung[self.comboBox_SanSale_VaoTrangSamsung.currentText()]))

        self.pushButton_SanSale_VaoSanPhamSamsung.setMenu(self.menuVaoSanPhamSamsung)
        self.add_menu(self.myListDevice, self.menuVaoSanPhamSamsung)
        
        #Samsung ?????t H??ng
        #A12
        listScriptA12= {
            "A12 X5 - M??u xanh": "/RemoteWifi/1111-SanSale-A12-Xanh.js",
            "A12 X5 - M??u ??en": "/RemoteWifi/1111-SanSale-A12-Den.js",
           
        }

        for script in listScriptA12:
            self.comboBox_SanSale_A12.addItem(script)
            

        self.menuA12 = QMenu()
        self.menuA12.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptA12[self.comboBox_SanSale_A12.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_A12.setMenu(self.menuA12)
        self.add_menu(self.myListDevice, self.menuA12)
        
        
        #M32
        listScriptM32= {
            "M32 X5 - M??u xanh": "/RemoteWifi/1111-SanSale-M32-Xanh.js",
            "M32 X5 - M??u ??en": "/RemoteWifi/1111-SanSale-M32-Den.js",
           
        }

        for script in listScriptM32:
            self.comboBox_SanSale_M32.addItem(script)
            

        self.menuM32 = QMenu()
        self.menuM32.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptM32[self.comboBox_SanSale_M32.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_M32.setMenu(self.menuM32)
        self.add_menu(self.myListDevice, self.menuM32)
        
        #Tab A7 Lite
        listScriptTabA7Lite= {
            "Tab A7 Lite X5 - M??u B???c": "/RemoteWifi/1111-SanSale-TabA7Lite.js",
           
        }

        for script in listScriptTabA7Lite:
            self.comboBox_SanSale_TabA7Lite.addItem(script)
            

        self.menuTabA7Lite = QMenu()
        self.menuTabA7Lite.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptTabA7Lite[self.comboBox_SanSale_TabA7Lite.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_TabA7Lite.setMenu(self.menuTabA7Lite)
        self.add_menu(self.myListDevice, self.menuTabA7Lite)
        
        #A03S
        listScriptA03S= {
            "A03S X5 - M??u xanh": "/RemoteWifi/1111-SanSale-A03S-Xanh.js",
            "A03S X5 - M??u ??en": "/RemoteWifi/1111-SanSale-A03S-Den.js",
           
        }

        for script in listScriptA03S:
            self.comboBox_SanSale_A03S.addItem(script)
            

        self.menuTabA03S = QMenu()
        self.menuTabA03S.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptA03S[self.comboBox_SanSale_A03S.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_A03S.setMenu(self.menuTabA03S)
        self.add_menu(self.myListDevice, self.menuTabA03S)
        
        
        ########################### Xiaomi #####################################
        #Vao San Pham
        listScriptVaoSanPhamXiaomi= {
            "V??o S???n Ph???m Redmi 9A": "/RemoteWifi/1111-VaoSanPham-Redmi9A.js",
            
        }

        for script in listScriptVaoSanPhamXiaomi:
            self.comboBox_SanSale_VaoTrangXiaomi.addItem(script)
            
        # Vao San Pham
        self.menuVaoSanPhamXiaomi= QMenu()
        self.menuVaoSanPhamXiaomi.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptVaoSanPhamXiaomi[self.comboBox_SanSale_VaoTrangXiaomi.currentText()]))

        self.pushButton_SanSale_VaoSanPhamXiaomi.setMenu(self.menuVaoSanPhamXiaomi)
        self.add_menu(self.myListDevice, self.menuVaoSanPhamXiaomi)
        
        #Samsung ?????t H??ng
        #A12
        listScriptRedmi9A= {
            "Redmi9A X5 - M??u xanh": "/RemoteWifi/1111-SanSale-Redmi9A-Xanh.js",
            "Redmi9A X5 - M??u ??en": "/RemoteWifi/1111-SanSale-Redmi9A-Den.js",
           
        }

        for script in listScriptRedmi9A:
            self.comboBox_SanSale_Redmi9A.addItem(script)
            

        self.menuRedmi9A = QMenu()
        self.menuRedmi9A.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptRedmi9A[self.comboBox_SanSale_Redmi9A.currentText()]))

        #connect button
        self.pushButton_SanSale_DatHang_9A.setMenu(self.menuRedmi9A)
        self.add_menu(self.myListDevice, self.menuRedmi9A)
        
        
        ########################### Chuc Nang Phu #####################################

        listScriptChucNangPhu= {
            "?????i IP 4G": "/RemoteWifi/TienIch-DoiIP4G.js",
            "Full ????ng Nh???p TK Kh??c": "/RemoteWifi/LZD1-DangNhapBangMatKhau.js",
            "L??u RRS": "/RemoteWifi/XoaInfo-LuuRRS.js",
            "Restore RRS": "/RemoteWifi/XoaInfo-Restore.js",
            
        }

        for script in listScriptChucNangPhu:
            self.comboBox_SanSale_ChucNangPhu.addItem(script)
            
        # Vao San Pham
        self.menuChucNangPhuDatHang= QMenu()
        self.menuChucNangPhuDatHang.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptChucNangPhu[self.comboBox_SanSale_ChucNangPhu.currentText()]))

        
        self.pushButton_SanSale_ChucNangPhu.setMenu(self.menuChucNangPhuDatHang)
        self.add_menu(self.myListDevice, self.menuChucNangPhuDatHang)
        
        
        ###list script
        listScriptTruot= {
            "Xem ????n ?????t": "/RemoteWifi/1212-XemDonDat.js",
            "Tr?????t V?? ?????t (L???n 1)": "/RemoteWifi/1212-TruotMuaHang.js",
            "Click Thanh Toan": "/RemoteWifi/1212-ClickThanhToan.js",
            "Click ?????t ????n": "/RemoteWifi/1111-ClickDatDon.js",
            
        }

        for script in listScriptTruot:
            self.comboBox_SanSale_TruotVaDatDon.addItem(script)
        
        
        test = (listScriptTruot[self.comboBox_SanSale_TruotVaDatDon.currentText()])
        self.menuTruot= QMenu()
        self.menuTruot.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScriptTruot[self.comboBox_SanSale_TruotVaDatDon.currentText()]))

        self.pushButton_SanSale_TruotVaDatDon.setMenu(self.menuTruot)
        
        self.add_menu(self.myListDevice, self.menuTruot)
        
        
        

    def selectionchange(self, i):
        print("Items in the list are :")

        for count in range(self.comboBox_ListScript.count()):
            print(self.comboBox_ListScript.itemText(count))
        print("Current index", i, "selection changed ",
              self.comboBox_ListScript.currentText())

    def checkSelectAcc(self, selected, deselected):

        for ix in selected.indexes():
            value = ix.sibling(ix.row(), ix.column()).data()
            self.listAccountSelected.append(value)

        for ix in deselected.indexes():
            value = ix.sibling(ix.row(), ix.column()).data()
            self.listAccountSelected.remove(value)

    def initListDevice(self):
        file = open("listDevice.txt", "r", encoding="utf-8")
        allLines = file.readlines()

        for line in allLines:
            data = line.strip()

            self.myListDevice.append(data)

    def add_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QMenu(k, menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.add_menu(element, menu_obj)
        else:
            action = menu_obj.addAction(data)
            action.setIconVisibleInMenu(False)

    def showListMay(self):
        self.tableWidget_IPMay.setRowCount(0)

        listDevice = []
        for device in self.myListDevice:
            if (device.find("192") != -1):
                listDevice.append(device)

        for i in range(len(listDevice)):

            row_number = self.tableWidget_IPMay.rowCount()
            self.tableWidget_IPMay.insertRow(row_number)

            tenMay = "M??y " + listDeviceDict[str(listDevice[i])]

            chkBoxItem = QtWidgets.QTableWidgetItem(str(listDevice[i]))
            chkBoxItem.setText(str(tenMay))
            chkBoxItem.setFlags(
                QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget_IPMay.setItem(row_number, 0, chkBoxItem)
            self.tableWidget_IPMay.setItem(
                row_number, 1, QtWidgets.QTableWidgetItem(str(listDevice[i])))

    def chuotPhaiShowListMay(self, event):
        contextMenu = QtWidgets.QMenu(self)

        chonTatCaAction = contextMenu.addAction("Ch???n T???t C???")
        chon136Action = contextMenu.addAction("!!! Ch???n Ng?????c !!!")
        boChonAction = contextMenu.addAction("B??? Ch???n")
        refreshDuLieuAction = contextMenu.addAction("Refresh D??? Li???u")

        action = contextMenu.exec_(self.mapToGlobal(event))

        if action == chonTatCaAction:
            print("Ch???n T???t C???")
            for i in range(self.tableWidget_IPMay.rowCount()):
                self.tableWidget_IPMay.item(
                    i, 0).setCheckState(QtCore.Qt.Checked)
        if action == chon136Action:
            print("Ch???n Ng?????c")
            for i in range(self.tableWidget_IPMay.rowCount()):
                if (self.tableWidget_IPMay.item(i, 0).checkState() == QtCore.Qt.Checked):
                    self.tableWidget_IPMay.item(
                        i, 0).setCheckState(QtCore.Qt.Unchecked)
                else:
                    self.tableWidget_IPMay.item(
                        i, 0).setCheckState(QtCore.Qt.Checked)
        if action == boChonAction:
            print("B??? Ch???n T???t C???")
            for i in range(self.tableWidget_IPMay.rowCount()):
                self.tableWidget_IPMay.item(
                    i, 0).setCheckState(QtCore.Qt.Unchecked)

        if action == refreshDuLieuAction:
            self.capNhatKho()

    def apiPlayScript(self, ip, path):
        print(path)

        if (ip != "START" and ip != "STOP"):
            linkURL = "http://" + ip + ":8080/control/start_playing?path=" + path

            pool = QThreadPool.globalInstance()

            runnableRemote = Remote(urlRemote=linkURL, scriptKho="", ipMay=ip)

            pool.start(runnableRemote.playScript)

        elif (ip == "START"):

            pool = QThreadPool.globalInstance()

            checkListDevice = []

            for i in range(self.tableWidget_IPMay.rowCount()):
                if (self.tableWidget_IPMay.item(i, 0).checkState() == QtCore.Qt.Checked):
                    checkListDevice.append(
                        self.tableWidget_IPMay.item(i, 1).text())

            for device in checkListDevice:
                linkURL = "http://" + device + ":8080/control/start_playing?path=" + path
                print(linkURL)
                runnableRemote = Remote(
                    urlRemote=linkURL, scriptKho="", ipMay=device)
                pool.start(runnableRemote.playScript)
                time.sleep(0.3)

        elif (ip == "STOP"):
            print("STOP")
            pool = QThreadPool.globalInstance()

            checkListDevice = []

            for i in range(self.tableWidget_IPMay.rowCount()):
                if (self.tableWidget_IPMay.item(i, 0).checkState() == QtCore.Qt.Checked):
                    checkListDevice.append(
                        self.tableWidget_IPMay.item(i, 1).text())
            print(checkListDevice)

            for device in checkListDevice:
                linkURL = "http://" + device + ":8080/control/stop_playing?path=" + path
                print(linkURL)
                runnableRemote = Remote(
                    urlRemote=linkURL, scriptKho="", ipMay=device)
                pool.start(runnableRemote.playScript)
                time.sleep(0.5)

    def napAccLZD(self, ip):
        
        self.label_KetQuaChay.setText(str("??ang N???p Acc"))
        
        if (ip != "START" and ip != "STOP"):

            self.napAccNew(ip)

        elif (ip == "START"):

            pool = QThreadPool.globalInstance()

            checkListDevice = []

            for i in range(self.tableWidget_IPMay.rowCount()):
                if (self.tableWidget_IPMay.item(i, 0).checkState() == QtCore.Qt.Checked):
                    checkListDevice.append(
                        self.tableWidget_IPMay.item(i, 1).text())

            # self.myListDevice.remove("START")
            print(checkListDevice)
            for device in checkListDevice:
                print(device)
                self.napAccNew(device)

        content = "N???p Acc Th??nh C??ng\n" + str(datetime.datetime.now())
        self.label_KetQuaChay.setText(str(content))

        self.capNhatKho()
        self.showDataKhoDatHang()

    def playScriptDatHang(self, ip, path):

        if (ip != "START" and ip != "STOP"):
            linkURL = "http://" + ip + ":8080/control/start_playing?path=" + path

            response = requests.get(linkURL, timeout=20)


        elif (ip == "START"):

            checkListDevice = []

            for i in range(self.tableWidget_IPMay.rowCount()):
                if (self.tableWidget_IPMay.item(i, 0).checkState() == QtCore.Qt.Checked):
                    checkListDevice.append(
                        self.tableWidget_IPMay.item(i, 1).text())

            for device in checkListDevice:
                linkURL = "http://" + device + ":8080/control/start_playing?path=" + path
                print(linkURL)
                response = requests.get(linkURL, timeout=20)

                print(response.json())
                time.sleep(3)

        elif (ip == "STOP"):
            checkListDevice = []

            for i in range(self.tableWidget_IPMay.rowCount()):
                if (self.tableWidget_IPMay.item(i, 0).checkState() == QtCore.Qt.Checked):
                    checkListDevice.append(
                        self.tableWidget_IPMay.item(i, 1).text())

            for device in checkListDevice:
                linkURL = "http://" + device + ":8080/control/stop_playing?path=" + path
                print(linkURL)
                response = requests.get(linkURL, timeout=20)

                print(response.json())



    def printSignal(self, s):
        if (s["status"] == False):
            msg = QMessageBox()
            msg.setText(s['noiDung'])
            x = msg.exec_()

    def ThemDuLieu(self):

        contentData = (self.plainTextEdit_KhoDuLieu.toPlainText()).split("\n")
        pool = QThreadPool.globalInstance()
        for i in range(len(contentData)):

            runnableRemote = Remote(
                urlRemote="", scriptKho=contentData[i], ipMay="")
            pool.start(runnableRemote.themDuLieuKho)

        time.sleep(2)
        msg = QMessageBox()
        msg.setText("Th??m d??? li???u v??o kho th??nh c??ng")
        x = msg.exec_()

    def resetKho(self):
        linkURL = "https://lzd420.me/api/resetkho"
        response = requests.get(linkURL)
        print(response.json())

        msg = QMessageBox()
        msg.setText("???? X??a To??n B??? D??? Li???u Kho")
        x = msg.exec_()

    def themDuLieuAccount(self):
        contentData = (
            self.plainTextEdit_ThemDuLieuAccount.toPlainText()).split("\n")
        pool = QThreadPool.globalInstance()
        for i in range(len(contentData)):

            runnableRemote = Remote(
                urlRemote="", scriptKho=contentData[i], ipMay="")
            pool.start(runnableRemote.addDataAccount)

        msg = QMessageBox()
        msg.setText("Th??m d??? li???u Account Th??nh C??ng")
        x = msg.exec_()

    def capNhatKho(self):
        print("Cap nhat du lieu kho")

        urlAPIGetKho = "http://lzd420.me/api/getCountKho"
        responseGetKho = requests.get(urlAPIGetKho)
        jsonDataGetKho = responseGetKho.json()

        self.label_ResultKhoDuLieu.setText(str(jsonDataGetKho["data"]))
        time.sleep(0.5)

        urlAPIGetAccountLazada = "http://lzd420.me/api/getCountAccLZD"
        responseGetAccLZD = requests.get(urlAPIGetAccountLazada)
        jsonDataGetAccLZD = responseGetAccLZD.json()

        urlAPIGetKhoDatHang = "http://lzd420.me/api/getCountKhoDatHang"
        responseGetKhoDatHang = requests.get(urlAPIGetKhoDatHang)
        jsonDataGetKhoLZD = responseGetKhoDatHang.json()

        self.label_ResultAccLazada.setText(str(jsonDataGetAccLZD["data"]))
        self.lineEdit_End.setText(str(jsonDataGetAccLZD["data"]))
        self.label_ResultKhoDuLieuAccLZD.setText(
            str(jsonDataGetKhoLZD["data"]))
        self.label_ResultKhoDuLieuAccLZD_2.setText(
            str(jsonDataGetKhoLZD["data"]))

    def getAccountLZD(self):
        urlAPIGetDataAccount = "http://lzd420.me/api/getAccountLZD"
        responseGetDataAccount = requests.get(urlAPIGetDataAccount)
        jsonDataGetDataAccount = responseGetDataAccount.json()["data"]

        data = {
            "STT": [],
            "Username": [],
            "PasswordLZD": [],
        }

        intFrom = int(self.lineEdit_From.text())
        intEnd = int(self.lineEdit_End.text())

        for i in range(intFrom, intEnd+1):
            stt = i - 1
            data["STT"].append(str(stt))
            data["Username"].append(
                str(jsonDataGetDataAccount[i-1]["username"]))
            data["PasswordLZD"].append(
                str(jsonDataGetDataAccount[i-1]["passwordLZD"]))

        df = pd.DataFrame(data)
        df.to_clipboard(index=False, header=False)
        print(df)

        msg = QMessageBox()
        msg.setText("???? Copy Acc Lazada")
        x = msg.exec_()

    def xuatExcelAccLZD(self):
        urlAPIGetDataAccount = "http://lzd420.me/api/getAccountLZD"
        responseGetDataAccount = requests.get(urlAPIGetDataAccount)
        jsonDataGetDataAccount = responseGetDataAccount.json()["data"]

        data = {
            "STT": [],
            "Username": [],
            "PasswordLZD": [],
            "deviceName": [],
            "owner": []
        }

        index = 1
        for item in jsonDataGetDataAccount:
            data["STT"].append(str(index))
            data["Username"].append(str(item["username"]))
            data["PasswordLZD"].append(str(item["passwordLZD"]))
            # data["PassMail"].append(str(item["passwordGmail"]))
            data["deviceName"].append(str(item["deviceName"]))
            data["owner"].append(str(item["owner"]))

            index = index + 1

        df = pd.DataFrame(data)
        df.to_csv('./accLZDaTao.csv', encoding='utf-8-sig',
                  mode='a', index=False, header=False,)

        msg = QMessageBox()
        msg.setText("???? Xu???t D??? Li???u Ra File Excel")
        x = msg.exec_()

    def xuatExcelListImei(self):
        urlApiListImei = "http://lzd420.me/api/getAllImei"
        responseListImei = requests.get(urlApiListImei)
        jsonDataListImei = responseListImei.json()["data"]

        data = {
            "STT": [],
            "imei": [],
            "ngayKichHoat": [],
            "model": [],
            "content": []
        }

        index = 1
        for item in jsonDataListImei:
            data["STT"].append(str(index))
            data["imei"].append(str(item["imei"]))
            data["ngayKichHoat"].append(str(item["ngayKichHoat"]))

            data["model"].append(str(item["model"]))
            data["content"].append(str(item["content"]))

            index = index + 1

        df = pd.DataFrame(data)
        df.to_csv('./Config/listImei.csv', encoding='utf-8-sig',
                  mode='a', index=False, header=False,)

        msg = QMessageBox()
        msg.setText("???? Xu???t D??? Li???u Ra File Excel")
        x = msg.exec_()

    def ThemDuLieuVaoKhoDatHang(self):

        contentData = (
            self.plainTextEdit_KhoDuLieuDatHang.toPlainText()).split("\n")
        pool = QThreadPool.globalInstance()
        for i in range(len(contentData)):

            runnableRemote = Remote(
                urlRemote="", scriptKho=contentData[i], ipMay="")
            pool.start(runnableRemote.themDuLieuKhoDatHang)

        self.capNhatKho()
        self.showDataKhoDatHang()

    def resetKhoDatHang(self):
        linkURL = "http://lzd420.me/api/resetKhoDatHang"
        response = requests.get(linkURL)
        print(response.json())

        msg = QMessageBox()
        msg.setText("???? X??a To??n B??? D??? Li???u Kho ?????t H??ng")
        x = msg.exec_()

        self.capNhatKho()
        self.showDataKhoDatHang()

    def updateLinkDatHang(self):
        contentData = (
            self.plainTextEdit_KhoDuLieuDatHang.toPlainText()).split("\n")
        pool = QThreadPool.globalInstance()
        for i in range(len(contentData)):

            runnableRemote = Remote(
                urlRemote="", scriptKho=contentData[i], ipMay="")
            pool.start(runnableRemote.capNhatLink)

        msg = QMessageBox()
        msg.setText("C???p Nh???t Link ?????t H??ng Th??nh C??ng")
        x = msg.exec_()

    def showDataKhoDatHang(self):
        self.capNhatKho()
        header = self.tableWidget_KhoDuLieuDatHang.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        self.tableWidget_KhoDuLieuDatHang.setRowCount(0)

        apiViewKhoDatHang = "https://lzd420.me/api/getkhodathang"
        response = requests.get(apiViewKhoDatHang)
        jsonData = response.json()["data"]

        if len(jsonData) > 0:
            for account in jsonData:
                row_number = self.tableWidget_KhoDuLieuDatHang.rowCount()
                self.tableWidget_KhoDuLieuDatHang.insertRow(row_number)

                self.tableWidget_KhoDuLieuDatHang.setItem(
                    row_number, 0, QtWidgets.QTableWidgetItem(str(account["username"])))
                self.tableWidget_KhoDuLieuDatHang.setItem(
                    row_number, 1, QtWidgets.QTableWidgetItem(str(account["password"])))
                self.tableWidget_KhoDuLieuDatHang.setItem(
                    row_number, 2, QtWidgets.QTableWidgetItem(str(account["deviceName"])))
                if (account["isGet"] == True):
                    self.tableWidget_KhoDuLieuDatHang.setItem(
                        row_number, 3, QtWidgets.QTableWidgetItem(str("???? L???y")))
                else:
                    self.tableWidget_KhoDuLieuDatHang.setItem(
                        row_number, 3, QtWidgets.QTableWidgetItem(str("")))

                self.tableWidget_KhoDuLieuDatHang.setItem(
                    row_number, 4, QtWidgets.QTableWidgetItem(str(account["status"])))

    def capNhatTrangThaiKhoDatHang(self):

        print(self.listAccountSelected)

        for account in self.listAccountSelected:
            apiUpdateTrangThai = "https://lzd420.me/api/updateTrangThaiKhoDatHang"
            dataPost = {
                "username": account,
                "status": self.lineEdit_Status.text(),
                "owner": owner
            }

            jsonData = json.dumps(dataPost)

            response = requests.post(apiUpdateTrangThai, dataPost)
            print(response.json())

        msg = QMessageBox()
        msg.setText("C???p Nh???t Tr???ng Th??i Cho T??i Kho???n " +
                    self.lineEdit_Username.text() + " th??nh c??ng")
        x = msg.exec_()

        self.showDataKhoDatHang()

    def copyTaiKhoanKhoDatHang(self):
        row_number = self.tableWidget_KhoDuLieuDatHang.rowCount()
        print("Tong acc: " + str(row_number))
        data = {
            "username": [],
            "password": [],
            "status": [],
        }
        for i in range(row_number):
            username = (self.tableWidget_KhoDuLieuDatHang.item(i, 0).text())
            password = (self.tableWidget_KhoDuLieuDatHang.item(i, 1).text())
            status = (self.tableWidget_KhoDuLieuDatHang.item(i, 4).text())

            data["username"].append(username)
            data["password"].append(password)
            data["status"].append(status)

        df = pd.DataFrame(data)
        df.to_clipboard(index=False, header=False)
        print(df)

        msg = QMessageBox()
        msg.setText("???? Copy " + str(row_number) +
                    " T??i Kho???n Kho ?????t H??ng Lazada")
        x = msg.exec_()

    def napAccNew(self, ipMay):

        linkAPI = "http://lzd420.me/api/getKhoDatHang&deviceName=" + \
            listDeviceDict[ipMay] + "&owner=" + owner
        response = requests.get(linkAPI)
        jsonData = response.json()
        if (jsonData["status"] == 'success'):

            dataAcc = jsonData["data"]

            dataPost = {
                "username": dataAcc["username"],
                "password": dataAcc["password"],
                "phoneNumber": dataAcc["phoneNumber"],
                "deviceName": dataAcc["deviceName"],
                "address": dataAcc["address"],
                "link": "",
                "owner": owner
            }

            print(dataPost)
            response = requests.post("http://lzd420.me/API/setinfo", dataPost)
            print(response.json())

    def create1000Imei(self):
        self.plainTextEdit_ListImeiRandom.clear()
        print("Create 1000 IMEI")
        imeiChuanHoa = self.lineEdit_Imei.text()[0:12]

        self.lineEdit_Imei.setText(str(imeiChuanHoa))

        listImeiRandom = []
        for i in range(0, 1000):
            imeiTemp = imeiChuanHoa
            if (i < 10):
                imeiTemp = imeiTemp + "00" + str(i)
            elif (i >= 10 and i < 100):
                imeiTemp = imeiTemp + "0" + str(i)
            else:
                imeiTemp = imeiTemp + str(i)

            listImeiRandom.append(imeiTemp)

        for imei in listImeiRandom:
            self.plainTextEdit_ListImeiRandom.appendPlainText(imei)

    def runLocImei(self):
        listImei = (self.plainTextEdit_ListImeiRandom.toPlainText()).split("\n")
        self.label_TongListImei.setText(str(len(listImei)))
        self.tableWidget_CheckImei.setRowCount(0)

        pool = QThreadPool.globalInstance()
        runnableRemote = Remote(
            urlRemote="", scriptKho=listImei, ipMay="")
        runnableRemote.signals.result.connect(self.CapNhatNoiDungCheckImei)
        pool.start(runnableRemote.locImei)

    def CapNhatNoiDungCheckImei(self, result):
        print(result)
        self.label_ResultTienTrinhImei.setText(str(result["tienTrinh"]))

        if (result["ngayKichHoat"] != ''):
            row_number = self.tableWidget_CheckImei.rowCount()
            self.tableWidget_CheckImei.insertRow(row_number)

            self.tableWidget_CheckImei.setItem(
                row_number, 0, QtWidgets.QTableWidgetItem(str(result["imei"])))
            self.tableWidget_CheckImei.setItem(
                row_number, 1, QtWidgets.QTableWidgetItem(str(result["ngayKichHoat"])))
            self.tableWidget_CheckImei.setItem(
                row_number, 2, QtWidgets.QTableWidgetItem(str(result["content"])))

    def luuCauHinhFake(self):

        versionApp = self.lineEdit_InputFakeVersionApp.text()

        checkFakeVersionAppRandom = self.checkBox_FakeIos.isChecked()
        
        tenApp = self.lineEdit_InputFakeTenApp.text()

        if (checkFakeVersionAppRandom == True):
            isFakeAppRandom = 'false'
        elif (checkFakeVersionAppRandom == False):
            isFakeAppRandom = 'true'


        dataPost = {
            "appVersion": versionApp,
            "isFakeAppRandom": isFakeAppRandom,
            "CFBundleIdentifier": tenApp,
            "owner": owner,
        }
        print(dataPost)

        # print(dataPost)
        response = requests.post(
            "http://lzd420.me/API/setCauHinhFake", dataPost)
        print(response.json())

    def showCauHinh(self):
        print(owner)
        apiViewCauHinh = "https://lzd420.me/api/getCauHinhFake&owner=" + owner
        response = requests.get(apiViewCauHinh, timeout=20)
        jsonData = response.json()[0]
        self.lineEdit_InputFakeVersionApp.setText(str(jsonData["appVersion"]))
        self.lineEdit_InputFakeTenApp.setText(str(jsonData["CFBundleIdentifier"]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
