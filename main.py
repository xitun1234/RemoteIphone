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
import requests
import re
import json
from urllib.parse import urlparse, parse_qs
import pandas as pd


listDeviceDict = {
    "192.168.3.21": "1",
    "192.168.3.22": "2",
    "192.168.3.23": "3",
    "192.168.3.24": "4",
    "192.168.3.25": "5",
    "192.168.3.26": "6",
    "192.168.3.27": "7",
    "192.168.3.28": "8",
    "192.168.3.29": "9",
    "192.168.3.30": "10",
    "192.168.3.31": "11",
    "192.168.3.32": "12",
    "192.168.3.33": "13",
    "192.168.3.34": "14",
    "192.168.3.35": "15",
    "192.168.3.36": "16",
    "192.168.3.37": "17",
    "192.168.3.38": "18",
    "192.168.3.39": "19",
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
        "192.168.3.21": "1",
        "192.168.3.22": "2",
        "192.168.3.23": "3",
        "192.168.3.24": "4",
        "192.168.3.25": "5",
        "192.168.3.26": "6",
        "192.168.3.27": "7",
        "192.168.3.28": "8",
        "192.168.3.29": "9",
        "192.168.3.30": "10",
        "192.168.3.31": "11",
        "192.168.3.32": "12",
        "192.168.3.33": "13",
        "192.168.3.34": "14",
        "192.168.3.35": "15",
        "192.168.3.36": "16",
        "192.168.3.37": "17",
        "192.168.3.38": "18",
        "192.168.3.39": "19",
    }

    def __init__(self, urlRemote, scriptKho, ipMay, parent=None):
        super().__init__()
        self.signals = WorkerSignals()

        self.urlRemote = urlRemote
        self.scriptKho = scriptKho
        self.ipMay = ipMay

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
            "owner": "admin"
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
            "owner": "admin"
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
            "owner": "admin"
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

        linkAPI = "http://lzd420.me/api/getKhoDatHang&deviceName=" + \
            self.listDeviceDict[self.ipMay] + "&owner=admin"
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
                "owner": "admin"
            }

            print(dataPost)
            response = requests.post("http://lzd420.me/API/setinfo", dataPost)
            print(response.json())

            result = {
                "status": True,
                "noiDung": "Nạp Acc Thành Công"
            }
            self.signals.result.emit(result)
        elif (jsonData["status"] == 'fail'):
            result = {
                "status": False,
                "noiDung": "Đã Hết Acc Trong Kho"
            }
            self.signals.result.emit(result)

    def capNhatLink(self):
        data = self.scriptKho.split("|")
        linkAPI = "http://lzd420.me/API/getinfo&deviceName=" + \
            data[1] + "&owner=admin"
        response = requests.get(linkAPI)
        dataJSON = (response.json())["data"]

        dataPost = {
            "username": dataJSON["username"],
            "password": dataJSON["password"],
            "phoneNumber": dataJSON["phoneNumber"],
            "deviceName": dataJSON["deviceName"],
            "address": dataJSON["address"],
            "link": data[0],
            "owner": "admin"
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
                resp["content"] = "Không có imei trong hệ thống"
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
        self.setWindowTitle(_translate("MainWindow", "Tool Điều Khiển Iphone"))

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

        # cap nhat kho va account
        # self.capNhatKho()

        # combo box list script
        listScript = {
            "Mua Ngay X5 - Xanh": "/RemoteWifi/TienIch-MuaNgayX5-1.js",
            "Mua Ngay X5 - Đen": "/RemoteWifi/TienIch-MuaNgayX5-2.js",
        }
        
        #self.comboBox_ListScript = QComboBox()
        
        for script in listScript:
            print(script)
            self.comboBox_ListScript.addItem(script)
        
        self.comboBox_ListScript.currentIndexChanged.connect(self.selectionchange)

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

        # add menu Full AppManager
        self.menuAppManager = QMenu()
        self.menuAppManager.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/Part1-RegAccAppManager.js"))

        # add menu Full Xoa Info
        self.menu = QMenu()
        self.menu.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/Part1-RegAccXoaInfo.js"))

        # add menu Add Mail
        self.menuAddMail = QMenu()
        self.menuAddMail.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/Part2-AddMail.js"))

        # add menu Add Mail
        self.menuAddMailLoi = QMenu()
        self.menuAddMailLoi.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/Part5-LoiAddMail.js"))

        # add menu Lay Lai Mat Khau
        self.menuLayLaiMatKhau = QMenu()
        self.menuLayLaiMatKhau.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/Part3-LayLaiMatKhau.js"))

        # add menu Dang Nhap LZD
        self.menuDangNhapLZD = QMenu()
        self.menuDangNhapLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/LZD1-DangNhapBangMatKhau.js"))

        # add menu MoLinkDeal 0D
        self.menuChiDangNhapLZD = QMenu()
        self.menuChiDangNhapLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/LZD11-ChiDangNhapLZD.js"))

        # add menu LuuRRS
        self.menuLuuRRS = QMenu()
        self.menuLuuRRS.triggered.connect(
            lambda x: self.apiPlayScript(x.text(), "/RemoteWifi/XoaInfo-LuuRRS.js"))

        # add menu RestoreRRS
        self.menuRestoreRRS = QMenu()
        self.menuRestoreRRS.triggered.connect(
            lambda x: self.apiPlayScript(x.text(), "/RemoteWifi/XoaInfo-Restore.js"))

        # add menu Dia Chi Thuong Tin
        self.menuDiaChiThuongTin = QMenu()
        self.menuDiaChiThuongTin.triggered.connect(
            lambda x: self.apiPlayScript(x.text(), "/RemoteWifi/LZD2-TaoDiaChi.js"))

        # add menu dia chi tan phu
        self.menuDiaChiTanPhu = QMenu()
        self.menuDiaChiTanPhu.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/LZD22-DiaChiLongBien.js"))

        # add menu mo link san pham
        self.menuMoLinkSanPham = QMenu()
        self.menuMoLinkSanPham.triggered.connect(
            lambda x: self.apiPlayScript(x.text(), "/RemoteWifi/LZD3-MoLinkNhanh.js"))

        # add menu click dat hang
        self.menuClickDatHang = QMenu()
        self.menuClickDatHang.triggered.connect(
            lambda x: self.playScriptDatHang(x.text(), "/RemoteWifi/LZD4-ClickDatHang.js"))

        # add menu chi dang nhap FB
        self.menuDangNhapFB = QMenu()
        self.menuDangNhapFB.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/Part12-DangNhapQuaFB.js"))

        # doi ten tai khoan
        self.menuDoiTenTaiKhoan = QMenu()
        self.menuDoiTenTaiKhoan.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/LZD12-DoiTenTaiKhoan.js"))

        # doi mat khau
        self.menuDoiMatKhauLZD = QMenu()
        self.menuDoiMatKhauLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/LZD13-DoiMatKhauLZD.js"))

        # add menu Nạp Acc Kho LZD
        self.menuNapAcc = QMenu()
        self.menuNapAcc.triggered.connect(lambda x: self.napAccLZD(x.text()))

        # add menu Test Add 30K
        self.menuThemGioHang = QMenu()
        self.menuThemGioHang.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/LZD21-ThemGioHang.js"))

        # add menu RRS Reg Acc
        self.menuRRSRegAcc = QMenu()
        self.menuRRSRegAcc.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/XoaInfo-LuuRRSRegAcc.js"))

        # add menu Lock Screen
        self.menuLockScreen = QMenu()
        self.menuLockScreen.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-LockScreen.js"))

        # add menu Unlock Screen
        self.menuUnlockScreen = QMenu()
        self.menuUnlockScreen.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-UnlockScreen.js"))

        self.pushButton_FullAppManager.setMenu(self.menuAppManager)
        self.pushButton_FullXoaInfo.setMenu(self.menu)
        self.pushButton_FullAddMail.setMenu(self.menuAddMail)
        # self.pushButton_LoiAddMail.setMenu(self.menuAddMailLoi)
        self.pushButton_FullAddMail_2.setMenu(self.menuLayLaiMatKhau)
        self.pushButton_DangNhapLZD.setMenu(self.menuDangNhapLZD)
        self.pushButton_ChiDangNhapLZD.setMenu(self.menuChiDangNhapLZD)
        self.pushButton_LuuRRS.setMenu(self.menuLuuRRS)
        self.pushButton_RestoreRRS.setMenu(self.menuRestoreRRS)
        self.pushButton_DiaChiThuongTin.setMenu(self.menuDiaChiThuongTin)
        self.pushButton_DiaChiTanPhu.setMenu(self.menuDiaChiTanPhu)
        self.pushButton_MoLinkNhanh.setMenu(self.menuMoLinkSanPham)
        self.pushButton_ClickDatHang.setMenu(self.menuClickDatHang)
        # self.pushButton_DangNhapFacebook.setMenu(self.menuDangNhapFB)
        self.pushButton_NapAccVaoMay.setMenu(self.menuNapAcc)
        self.pushButton_NapAccVaoMay_2.setMenu(self.menuNapAcc)
        self.pushButton_DoiTenTaiKhoan.setMenu(self.menuDoiTenTaiKhoan)
        self.pushButton_DoiMatKhauLZD.setMenu(self.menuDoiMatKhauLZD)
        self.pushButton_ThemGioHang.setMenu(self.menuThemGioHang)
        self.pushButton_LuuRRSRegAcc.setMenu(self.menuRRSRegAcc)
        self.pushButton_LockScreen.setMenu(self.menuLockScreen)
        self.pushButton_UnlockScreen.setMenu(self.menuUnlockScreen)

        ########## ADD MENU ############
        self.add_menu(self.myListDevice, self.menuAppManager)
        self.add_menu(self.myListDevice, self.menu)
        self.add_menu(self.myListDevice, self.menuAddMail)
        self.add_menu(self.myListDevice, self.menuAddMailLoi)
        self.add_menu(self.myListDevice, self.menuLayLaiMatKhau)
        self.add_menu(self.myListDevice, self.menuDangNhapLZD)
        self.add_menu(self.myListDevice, self.menuChiDangNhapLZD)

        self.add_menu(self.myListDevice, self.menuDiaChiThuongTin)
        self.add_menu(self.myListDevice, self.menuDiaChiTanPhu)
        self.add_menu(self.myListDevice, self.menuMoLinkSanPham)
        self.add_menu(self.myListDevice, self.menuClickDatHang)
        self.add_menu(self.myListDevice, self.menuDangNhapFB)
        self.add_menu(self.myListDevice, self.menuNapAcc)
        self.add_menu(self.myListDevice, self.menuLuuRRS)
        self.add_menu(self.myListDevice, self.menuRestoreRRS)
        self.add_menu(self.myListDevice, self.menuDoiTenTaiKhoan)
        self.add_menu(self.myListDevice, self.menuDoiMatKhauLZD)
        self.add_menu(self.myListDevice, self.menuThemGioHang)
        self.add_menu(self.myListDevice, self.menuRRSRegAcc)
        self.add_menu(self.myListDevice, self.menuLockScreen)
        self.add_menu(self.myListDevice, self.menuUnlockScreen)

        # add menu moi
        # add menu Menu Press Home
        self.menuPressHome = QMenu()
        self.menuPressHome.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-PressHome.js"))

        self.pushButton_PressHome.setMenu(self.menuPressHome)
        self.add_menu(self.myListDevice, self.menuPressHome)

        # add menu Menu Mo App Lzd
        self.menuMoAppLZD = QMenu()
        self.menuMoAppLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-MoAppLZDFake.js"))

        self.pushButton_MoAppLZD.setMenu(self.menuMoAppLZD)
        self.add_menu(self.myListDevice, self.menuMoAppLZD)

        # add menu Menu Respring
        self.menuRespring = QMenu()
        self.menuRespring.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-Respring.js"))

        self.pushButton_Respring.setMenu(self.menuRespring)
        self.add_menu(self.myListDevice, self.menuRespring)

        # add menu Dang Nhap Bang FB
        self.menuDangNhapByFB = QMenu()
        self.menuDangNhapByFB.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/Part12-DangNhapQuaFB.js"))

        self.pushButton_DangNhapBangFB.setMenu(self.menuDangNhapByFB)
        self.add_menu(self.myListDevice, self.menuDangNhapByFB)

        # add menu Fake Version
        self.menuFakeVersionLZD = QMenu()
        self.menuFakeVersionLZD.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-FakeVersionApp.js"))

        self.pushButton_FakeVersionApp.setMenu(self.menuFakeVersionLZD)
        self.add_menu(self.myListDevice, self.menuFakeVersionLZD)

        # add menu Dia Chi Ha Dong
        self.menuDiaChiHaDong = QMenu()
        self.menuDiaChiHaDong.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/LZD22-DiaChiHaDong.js"))

        self.pushButton_QuanHaDong.setMenu(self.menuDiaChiHaDong)
        self.add_menu(self.myListDevice, self.menuDiaChiHaDong)

        # add menu Dia Chi Hoang Mai
        self.menuDiaChiHoangMai = QMenu()
        self.menuDiaChiHoangMai.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/ZD22-DiaChiQuan10.js"))

        self.pushButton_QuanHoangMai.setMenu(self.menuDiaChiHoangMai)
        self.add_menu(self.myListDevice, self.menuDiaChiHoangMai)

        # add menu Xoa Info
        self.menuChiXoaInfo = QMenu()
        self.menuChiXoaInfo.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-XoaInfo.js"))

        self.pushButton_ChiXoaInfo.setMenu(self.menuChiXoaInfo)
        self.add_menu(self.myListDevice, self.menuChiXoaInfo)

        # add menu Mo App LZD Goc
        self.menuMoAppLZDGoc = QMenu()
        self.menuMoAppLZDGoc.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), "/RemoteWifi/TienIch-MoAppLazadaGoc.js"))

        self.pushButton_MoAppLZDGoc.setMenu(self.menuMoAppLZDGoc)
        self.add_menu(self.myListDevice, self.menuMoAppLZDGoc)
        
        # add menu Mo App LZD Goc
        self.menuRunScript = QMenu()
        self.menuRunScript.triggered.connect(lambda x: self.apiPlayScript(
            x.text(), listScript[self.comboBox_ListScript.currentText()]))

        self.pushButton_RunScript.setMenu(self.menuRunScript)
        self.add_menu(self.myListDevice, self.menuRunScript)

        # pushButton_ThemDuLieu
        self.pushButton_ThemDuLieu.clicked.connect(self.ThemDuLieu)

        self.pushButton_ResetKho.clicked.connect(self.resetKho)

        # self.pushButton_ThemAccount.clicked.connect(self.themDuLieuAccount)

        # copy du lieu
        self.pushButton_CopyAccLZD.clicked.connect(self.getAccountLZD)
        self.pushButton_ExcelAccLZD.clicked.connect(self.xuatExcelAccLZD)
        self.pushButton_ExcelListImei.clicked.connect(self.xuatExcelListImei)
        # self.getAccountLZD(0,0)

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


    def selectionchange(self,i):
        print ("Items in the list are :")
		
        for count in range(self.comboBox_ListScript.count()):
            print (self.comboBox_ListScript.itemText(count))
        print ("Current index",i,"selection changed ",self.comboBox_ListScript.currentText())


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

            tenMay = "Máy " + listDeviceDict[str(listDevice[i])]

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

        chonTatCaAction = contextMenu.addAction("Chọn Tất Cả")
        chon136Action = contextMenu.addAction("!!! Chọn Ngược !!!")
        boChonAction = contextMenu.addAction("Bỏ Chọn")
        refreshDuLieuAction = contextMenu.addAction("Refresh Dữ Liệu")

        action = contextMenu.exec_(self.mapToGlobal(event))

        if action == chonTatCaAction:
            print("Chọn Tất Cả")
            for i in range(self.tableWidget_IPMay.rowCount()):
                self.tableWidget_IPMay.item(
                    i, 0).setCheckState(QtCore.Qt.Checked)
        if action == chon136Action:
            print("Chọn Ngược")
            for i in range(self.tableWidget_IPMay.rowCount()):
                if (self.tableWidget_IPMay.item(i, 0).checkState() == QtCore.Qt.Checked):
                    self.tableWidget_IPMay.item(
                        i, 0).setCheckState(QtCore.Qt.Unchecked)
                else:
                    self.tableWidget_IPMay.item(
                        i, 0).setCheckState(QtCore.Qt.Checked)
        if action == boChonAction:
            print("Bỏ Chọn Tất Cả")
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

        msg = QMessageBox()
        msg.setText("Nạp Acc Thành Công")
        x = msg.exec_()

        self.capNhatKho()
        self.showDataKhoDatHang()

    def playScriptDatHang(self, ip, path):

        if (ip != "START" and ip != "STOP"):
            linkURL = "http://" + ip + ":8080/control/start_playing?path=" + path

            response = requests.get(linkURL, timeout=20)

            # print(response.json())

            # self.capNhatKho()
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

            # self.capNhatKho()
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

            # self.capNhatKho()

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
        msg.setText("Thêm dữ liệu vào kho thành công")
        x = msg.exec_()

    def resetKho(self):
        linkURL = "https://lzd420.me/api/resetkho"
        response = requests.get(linkURL)
        print(response.json())

        msg = QMessageBox()
        msg.setText("Đã Xóa Toàn Bộ Dữ Liệu Kho")
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
        msg.setText("Thêm dữ liệu Account Thành Công")
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
        msg.setText("Đã Copy Acc Lazada")
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
        msg.setText("Đã Xuất Dữ Liệu Ra File Excel")
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
        msg.setText("Đã Xuất Dữ Liệu Ra File Excel")
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
        msg.setText("Đã Xóa Toàn Bộ Dữ Liệu Kho Đặt Hàng")
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
        msg.setText("Cập Nhật Link Đặt Hàng Thành Công")
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
                        row_number, 3, QtWidgets.QTableWidgetItem(str("Đã Lấy")))
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
                "owner": "admin"
            }

            jsonData = json.dumps(dataPost)

            response = requests.post(apiUpdateTrangThai, dataPost)
            print(response.json())

        msg = QMessageBox()
        msg.setText("Cập Nhật Trạng Thái Cho Tài Khoản " +
                    self.lineEdit_Username.text() + " thành công")
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
        msg.setText("Đã Copy " + str(row_number) +
                    " Tài Khoản Kho Đặt Hàng Lazada")
        x = msg.exec_()

    def napAccNew(self, ipMay):

        linkAPI = "http://lzd420.me/api/getKhoDatHang&deviceName=" + \
            listDeviceDict[ipMay] + "&owner=admin"
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
                "owner": "admin"
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
        print(versionApp)

        checkFakeVersionAppRandom = self.checkBox_FakeIos.isChecked()
        print(checkFakeVersionAppRandom)

        if (checkFakeVersionAppRandom == True):
            isFakeAppRandom = 'false'
        elif (checkFakeVersionAppRandom == False):
            isFakeAppRandom = 'true'

        print(isFakeAppRandom)
        dataPost = {
            "appVersion": versionApp,
            "isFakeAppRandom": isFakeAppRandom,
            "owner": "admin"
        }

        # print(dataPost)
        response = requests.post(
            "http://lzd420.me/API/setCauHinhFake", dataPost)
        print(response.json())

    def showCauHinh(self):
        apiViewCauHinh = "https://lzd420.me/api/getCauHinhFake&owner=admin"
        response = requests.get(apiViewCauHinh, timeout=20)
        jsonData = response.json()[0]
        self.lineEdit_InputFakeVersionApp.setText(str(jsonData["appVersion"]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
