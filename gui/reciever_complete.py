import math
import sys
import time
from cmath import cos, sin
from random import randrange

import geopy.distance
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from PyQt6.QtCore import QCoreApplication, QDate, QDateTime, QLine, QLineF, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, Qt, QTime, QUrl  # NOQA
from PyQt6.QtGui import QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QImage, QKeySequence, QLinearGradient, QPaintDevice, QPainter, QPalette, QPen, QPixmap, QRadialGradient, QTransform  # NOQA
from PyQt6.QtWidgets import QApplication, QDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget  # NOQA
from sqlalchemy import create_engine

#This is an open source library that I found - not my orginal work
import satellite_images
from utm.conversion import from_latlon, to_latlon

#Making of the app layout
class Example(QWidget):

    counter = 1
    total_runs = 0
    if_trans_outside = False
    data_dict = {'': 0, '2': 0, '3': 1, '4': 0, '5': 0}

    def __init__(self):
        super().__init__()

        #self.initUI()
        self.setupUi(self)
        


    def initUI(self):

        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colours')
        self.show()

    def setupUi(self, Widget):
        Widget.resize(800, 600)
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(550, 20, 211, 41))
        #self.pushButton.clicked.connect(self.loadReceiverData)
        self.lineEdit = QLineEdit(Widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(550, 110, 161, 31))
        self.lineEdit_2 = QLineEdit(Widget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(550, 170, 161, 31))
        self.lineEdit_3 = QLineEdit(Widget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(550, 230, 161, 31))
        self.lineEdit_4 = QLineEdit(Widget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(550, 490, 211, 31))
        self.lineEdit_5 = QLineEdit(Widget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(550, 430, 211, 31))
        self.lineEdit_6 = QLineEdit(Widget)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(550, 370, 211, 31))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(550, 90, 111, 16))
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(550, 150, 111, 16))
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(550, 210, 111, 16))
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(550, 350, 191, 16))
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(550, 410, 191, 16))
        self.label_6 = QLabel(Widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(550, 470, 191, 16))
        self.graphicsView = QGraphicsView(Widget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(30, 23, 501, 494))
        # self.graphicsScene = QGraphicsScene(Widget)
        # self.graphicsScene.setObjectName(u"graphicsScene")
        self.lineEdit_7 = QLineEdit(Widget)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setGeometry(QRect(720, 110, 61, 31))
        self.lineEdit_8 = QLineEdit(Widget)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setGeometry(QRect(720, 170, 61, 31))
        self.lineEdit_9 = QLineEdit(Widget)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setGeometry(QRect(720, 230, 61, 31))
        self.label_7 = QLabel(Widget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(720, 90, 111, 16))
        self.label_8 = QLabel(Widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(720, 150, 111, 16))
        self.label_9 = QLabel(Widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(720, 210, 111, 16))

        self.label_10 = QLabel(Widget)
        self.label_10.setGeometry(QRect(30, 20, 501, 501))
        self.label_10.setObjectName(u"label_10")

        self.label_11 = QLabel(Widget)
        self.label_11.setGeometry(QRect(30, 20, 200, 200))
        self.label_11.setObjectName(u"label_11")

        self.label_12 = QLabel(Widget)
        self.label_12.setGeometry(QRect(60, 20, 200, 200))
        self.label_12.setObjectName(u"label_12")

        self.label_13 = QLabel(Widget)
        self.label_13.setGeometry(QRect(90, 20, 200, 200))
        self.label_13.setObjectName(u"label_13")

        self.label_14 = QLabel(Widget)
        self.label_14.setGeometry(QRect(30, 20, 501, 501))
        self.label_14.setObjectName(u"label_13")

        self.label_15 = QLabel(Widget)
        self.label_15.setGeometry(QRect(30, 525, 300, 16))
        self.label_15.setObjectName(u"label_13")

        self.label_16 = QLabel(Widget)
        self.label_16.setGeometry(QRect(650, 575, 125, 16))
        self.label_16.setObjectName(u"label_13")

        self.pushButton2 = QPushButton(Widget)
        self.pushButton2.setObjectName(u"pushButton")
        self.pushButton2.setGeometry(QRect(775, 575, 25, 25))

        self.label_17 = QLabel(Widget)
        self.label_17.setGeometry(QRect(30, 5, 350, 16))
        self.label_17.setObjectName(u"label_13")

        #self.line_1 = QLine(0,0,50,50
        

        self.pushButton.clicked.connect(self.loadReceiverData)

        self.pushButton2.clicked.connect(self.fake_setup)
        #self.pushButton.clicked.connect(self.add_rectangle)
        #self.button.clicked.connect(self.add_rectangle)
        
        

        self.retranslateUi(Widget)

    
        
        

        

    #Button to reset layout
    def fake_setup(self ,Widget):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")

        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")

        self.lineEdit_6.setText("")
        self.lineEdit_5.setText("")
        self.label_15.setText("X grid size:       Y grid size:")
        self.lineEdit_4.setText("")
        pixmap3 = QPixmap("1x1.png")

        self.label_10.setPixmap(pixmap3)
        self.label_11.setPixmap(pixmap3)
        self.label_12.setPixmap(pixmap3)
        self.label_13.setPixmap(pixmap3)
        self.counter += 1
        if self.counter > 5:
            self.counter = 1
        self.label_16.setText("Currently Selected: " + str(self.counter % 6))
        self.label_17.setText("")
        if (self.counter - 1)%6 == 0:
            self.data_dict = {'': 0, '2': 0, '3': 1, '4': 0, '5': 0}
        self.if_trans_outside = False
        
        

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"403 GUI", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Receiver 1 Location", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Receiver 2 Location", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Receiver 3 Location", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Expected Transmitter Location", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Calculated Transmitter Location", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Error", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"Angle 1", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"Angle 2", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"Angle 3", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"", None))
        self.label_12.setText(QCoreApplication.translate("Widget", u"", None))
        self.label_13.setText(QCoreApplication.translate("Widget", u"", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"", None))
        self.label_15.setText(QCoreApplication.translate("Widget", u"X grid size:       Y grid size:", None))
        self.label_16.setText(QCoreApplication.translate("Widget", u"Currently Selected: " + str(self.counter), None))
        self.label_17.setText(QCoreApplication.translate("Widget", u"", None))
        self.pushButton2.setText(QCoreApplication.translate("Widget", u">", None))

    #Main
    def loadReceiverData(self):
        
        engine = create_engine('postgresql+psycopg2://postgres:Nyhr7fv245@project403.c6uydewvrqoi.us-east-2.rds.amazonaws.com:5432/postgres')
        check_row_count_query = "SELECT COUNT(*) FROM start"

        with engine.connect() as con:
            row_count = con.execute(check_row_count_query).scalar()

        #Checking the query and if so sending start signal
        if row_count > 0:
            update_query = "UPDATE start SET id = 1"

        with engine.connect() as con:
            con.execute(update_query)
        #Waiting 3 mins for all the motors to finish running
        print("Waiting")
        time.sleep(180)
        print("Done Waiting")

        st = time.time()
        

        
        data_list = [key for key in self.data_dict]

        self.data_dict[data_list[self.counter-1 % 6]] = self.data_dict[data_list[self.counter-1 % 6]] + 1

        check_query = "SELECT * FROM recdata" + data_list[self.counter-1 % 6]

        #Grabbing all required data
        with engine.connect() as con:
            names = con.execute(check_query).scalars(0).all()
            lats = con.execute(check_query).scalars(1).all()
            longs = con.execute(check_query).scalars(2).all()
            trans_lats = con.execute(check_query).scalars(3).all()
            trans_longs = con.execute(check_query).scalars(4).all()
            angles = con.execute(check_query).scalars(5).all()

        lats_longs = [None]*(len(lats)+len(longs))
        lats_longs[::2] = lats
        lats_longs[1::2] = longs

        trans_lats_longs = str(trans_lats[0])+str(trans_longs[0])

        lats_longs[0] = str(lats_longs[0])+ "," +str(lats_longs[1])
        lats_longs[1] = str(lats_longs[2])+ "," +str(lats_longs[3])
        lats_longs[2] = str(lats_longs[4])+ "," +str(lats_longs[5])

        self.lineEdit.setText(lats_longs[0])
        self.lineEdit_2.setText(lats_longs[1])
        self.lineEdit_3.setText(lats_longs[2])

        self.lineEdit_7.setText(str(angles[0]))
        self.lineEdit_8.setText(str(angles[1]))
        self.lineEdit_9.setText(str(angles[2]))

        self.lineEdit_6.setText(trans_lats_longs)

        if self.if_trans_outside == True:
            lats.append(trans_lats[0])
            longs.append(trans_longs[0])

        
        #Getting the points for the satelitte image
        i = 0
        k = 0
        lat_min = min(lats)-i
        lon_min = min(longs)-k
        lat_max = max(lats)+i
        lon_max = max(longs)+k

        minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
        maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)

        original_grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
        grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
        
        
        if grid_size[0] < 501 and grid_size[1] < 501:
            check = False
            while True:
                lat_min = min(lats)-i
                lon_min = min(longs)-k
                lat_max = max(lats)+i
                lon_max = max(longs)+k

                minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)

                grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                

                if  int(grid_size[0]) % 501 == 0:
                    
                    
                    while True:
                        lat_min = min(lats)-i
                        lat_max = max(lats)+i
                        minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                        maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)
                        grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                        if int(grid_size[1]) % 501 == 0:
                            break
                        i+=0.000001
                        
                    break

                    
                if  int(grid_size[1]) % 501 == 0:
                    
                    while True:
                        lon_min = min(longs)-k
                        lon_max = max(longs)+k
                        minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                        maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)
                        grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                        if int(grid_size[0]) % 501 == 0:
                            break
                        k+=0.000001
                        
                    break
                i += 0.000001
                k += 0.000001
        else:
            check = True
            while True:
                lat_min = min(lats)-i
                lon_min = min(longs)-k
                lat_max = max(lats)+i
                lon_max = max(longs)+k

                minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)

                grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                

                if grid_size[0] > 503:
                    
                    if  int(grid_size[0]) % 501 == 0:
                        
                        
                        while True:
                            lat_min = min(lats)-i
                            lat_max = max(lats)+i
                            minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                            maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)
                            grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                            if int(grid_size[1]) % 501 == 0:
                                break
                            i+=0.000001
                            
                        break

                if grid_size[1] > 503:
                    
                    if  int(grid_size[1]) % 501 == 0:
                        
                        while True:
                            lon_min = min(longs)-k
                            lon_max = max(longs)+k
                            minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                            maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)
                            grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                            if int(grid_size[0]) % 501 == 0:
                                break
                            k+=0.000001
                            
                        break
                i += 0.000001
                k += 0.000001
            
            
        

        lat_min = min(lats)
        lon_min = min(longs)
        lat_max = max(lats)
        lon_max = max(longs)

        

        lat_min = min(lats)-i
        lon_min = min(longs)-k
        lat_max = max(lats)+i
        lon_max = max(longs)+k

        minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
        maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)

        
        

        

        related_grid = (grid_size[0]/501, grid_size[1]/501)
        

        
        rec1 = from_latlon(latitude=  lats[0], longitude = longs[0])
        rec2 = from_latlon(latitude = lats[1], longitude = longs[1])
        rec3 = from_latlon(latitude = lats[2], longitude = longs[2])

        

        

        newrec1 = ((rec1[0] - minpoint[0])/related_grid[0], (501)-(rec1[1] - minpoint[1])/related_grid[1])
        newrec2 = ((rec2[0] - minpoint[0])/related_grid[0], (501)-(rec2[1] - minpoint[1])/related_grid[1])
        newrec3 = ((rec3[0] - minpoint[0])/related_grid[0], (501)-(rec3[1] - minpoint[1])/related_grid[1])

        

       
        

        #Getting the satellite image
        API_KEY = "b8WjT8oKxjhu9w0mBYjE"
        image = satellite_images.query((lat_min, lon_min), (lat_max, lon_max), key=API_KEY, resolution="auto")
        im = Image.fromarray(image)

        draw = ImageDraw.Draw(im)
        r = 500

        #Doing math from the angle to then get the line of the strongest signal
        rec1_point1 = (int(newrec1[0]), int(newrec1[1]))
        rec1_point2 = (int(newrec1[0]+r*math.cos(math.radians(angles[0]))), int(newrec1[1]-r*math.sin(math.radians(angles[0]))))

        

        rec2_point1 = (int(newrec2[0]), int(newrec2[1]))
        rec2_point2 = (int(newrec2[0]+r*math.cos(math.radians(angles[1]))), int(newrec2[1]-r*math.sin(math.radians(angles[1]))))


        rec3_point1 = (int(newrec3[0]), int(newrec3[1]))
        rec3_point2 = (int(newrec3[0]+r*math.cos(math.radians(angles[2]))), int(newrec3[1]-r*math.sin(math.radians(angles[2]))))

       

        #Math for the line to then make intersections
        def line(p1, p2):
            a = (p2[1] - p1[1])
            b = (p1[0] - p2[0])
            c = (p1[0]*p2[1] - p2[0]*p1[1])
            return a,b,-c

        def intersection(L1, L2):
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[1] * L2[2] - L1[2] * L2[1]
            Dy = L1[2] * L2[0] - L1[0] * L2[2]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x,y
            else:
                return False
            
        rec1_line = line(rec1_point1, rec1_point2)
        rec2_line = line(rec2_point1, rec2_point2)
        rec3_line = line(rec3_point1, rec3_point2)

        area_line1 = line(rec1_point1,rec2_point1)
        area_line2 = line(rec1_point1,rec3_point1)
        area_line3 = line(rec2_point1,rec3_point1)

        
        area1 = intersection(area_line1,area_line2)
        area2 = intersection(area_line1,area_line3)
        area3 = intersection(area_line2,area_line3)
        x = (area1[0],area2[0],area3[0])
        y = (area1[1],area2[1],area3[1])
        area = 0.5 * (x[0] * (y[1] - y[2]) + x[1] * (y[2] - y[0]) + x[2]
                  * (y[0] - y[1]))
        total_grid = grid_size[0]*grid_size[1]

        
        if(intersection(rec1_line, rec2_line)[0] < -5000 or intersection(rec1_line, rec2_line)[1] < -5000):
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            layout = QVBoxLayout(self)
            message = QLabel("Error in line 1 and 2")
            layout.addWidget(message)
            dlg.setLayout(layout)
            dlg.exec()
            print("error in line 1 and 2")

        if(intersection(rec1_line, rec3_line)[0] < -5000 or intersection(rec1_line, rec3_line)[1] < -5000):
            print("error in line 1 and 3")
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            layout = QVBoxLayout(self)
            message = QLabel("Error in line 1 and 3")
            layout.addWidget(message)
            dlg.setLayout(layout)
            dlg.exec()
            return 0

        if(intersection(rec2_line, rec3_line)[0] < -5000 or intersection(rec2_line, rec3_line)[1] < -5000):
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            layout = QVBoxLayout(self)
            message = QLabel("Error in line 2 and 3")
            layout.addWidget(message)
            dlg.setLayout(layout)
            dlg.exec()
            print("error in line 2 and 3")

        #Getting the intersecting points of the lines formed by the strongest angle
        line_1_2 = intersection(rec1_line, rec2_line)
        line_1_3 = intersection(rec1_line, rec3_line)
        line_2_3 = intersection(rec2_line, rec3_line)

        

        #finding the center of the area
        centroid_data = (line_1_2, line_1_3, line_2_3)
        centroid = np.mean(centroid_data, axis = 0)

        

        grid_min = (lat_min, lon_min)
        grid_max = (lat_max, lon_max)
        

        grid_distance1 = geopy.distance.geodesic(lats_longs[0], lats_longs[1]).m
        grid_distance2 = geopy.distance.geodesic(lats_longs[0], lats_longs[2]).m
        grid_distance3 = geopy.distance.geodesic(lats_longs[1], lats_longs[2]).m

        s = (grid_distance1 + grid_distance2 + grid_distance3) / 2  
        area = (s*(s-grid_distance1)*(s-grid_distance2)*(s-grid_distance3)) ** 0.5
        
        
        center_lat_lon_data = ((centroid[0]*related_grid[0] + minpoint[0]), (minpoint[1] - centroid[1]*related_grid[1] + grid_size[1]))

        

        center_lat_lon = to_latlon(easting=center_lat_lon_data[0], northing=center_lat_lon_data[1], zone_number=14, zone_letter='R')

        

        #This is needed if the area of the transmitters and recievers is bigger than 500 m
        if center_lat_lon[0] < lat_min or center_lat_lon[0] > lat_max:
            
            self.if_trans_outside = True
            self.loadReceiverData()
        
        if center_lat_lon[1] < lon_min or center_lat_lon[1] > lon_max:

            self.if_trans_outside = True
            self.loadReceiverData()
        

        display_center = str(round(center_lat_lon[0],5)) +","+ str(round(center_lat_lon[1],5))
        
        self.lineEdit_5.setText(display_center)
        trans_coords = (trans_lats[0], trans_longs[0])

        x_grid = ((lat_min, lon_min),(lat_min,lon_max))
        y_grid = ((lat_min, lon_min),(lat_max,lon_min))

        

        x_distance = geopy.distance.geodesic(x_grid[0], x_grid[1]).m
        
        y_distance = geopy.distance.geodesic(y_grid[0], y_grid[1]).m
        

        self.label_15.setText("X grid size: " + str(round(x_distance,2)) + "m" "      Y grid size: " + str(round(y_distance,2)) + 'm')
        

        #Doing error calcs
        errorcalc = geopy.distance.geodesic(trans_coords, center_lat_lon).m

        
        
        #Setting all of the lines and information calculated
        self.lineEdit_4.setText(str(round(errorcalc,3)) + " meters")
        
        draw.line(((rec1_point1),(rec1_point2)), fill=(255, 0, 0), width=3)
        draw.line(((rec2_point1),(rec2_point2)), fill=(255, 0, 0), width=3)
        draw.line(((rec3_point1),(rec3_point2)), fill=(255, 0, 0), width=3)
        draw.point((line_1_2), fill=(0, 0, 0))
        draw.point((line_1_3), fill=(0, 0, 0))
        draw.point((line_2_3), fill=(0, 0, 0))
        draw.polygon((line_1_2, line_1_3, line_2_3), fill=(255, 255, 0), outline=(0,0,0))
        draw.point((centroid[0], centroid[1]), fill=(0, 0, 0))
        im.save('background.jpg')

        pixmap = QPixmap('background.jpg')
        self.label_10.setPixmap(pixmap)
        

        pixmap2 = QPixmap('imageedit_2_9214147233.png')

        pixmap3 = QPixmap('rsz_2.png')
        
        
        self.label_11.move(int(newrec1[0]+20), int(newrec1[1]-80))
        
        self.label_11.setPixmap(pixmap2)
        self.label_12.move(int(newrec2[0]+20), int(newrec2[1]-80))

        
        self.label_12.setPixmap(pixmap2)
        self.label_13.move(int(newrec3[0]+20), int(newrec3[1]-80))
        
        self.label_13.setPixmap(pixmap2)

        

        et = time.time()

        print("Time taken for dataset" ,self.counter%6," is ", round(et-st,3))

        if self.if_trans_outside == True and ((center_lat_lon[0] < lat_min or center_lat_lon[0] > lat_max) or (center_lat_lon[1] < lon_min or center_lat_lon[1] > lon_max)):
            print("doing it again")
            self.loadReceiverData()
       
        





def main():

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()