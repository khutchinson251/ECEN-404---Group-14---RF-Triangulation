"""
ZetCode PyQt6 tutorial
This example draws three rectangles in three
different colours.
Author: Jan Bodnar
Website: zetcode.com
"""

import math
import sys
from cmath import cos, sin
from random import randrange

import geopy.distance
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from PyQt6.QtCore import QCoreApplication, QDate, QDateTime, QLine, QLineF, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, Qt, QTime, QUrl  # NOQA
from PyQt6.QtGui import QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QImage, QKeySequence, QLinearGradient, QPaintDevice, QPainter, QPalette, QPen, QPixmap, QRadialGradient, QTransform  # NOQA
from PyQt6.QtWidgets import QApplication, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QLabel, QLineEdit, QPushButton, QSizePolicy, QWidget  # NOQA
from sqlalchemy import create_engine

import satellite_images
from utm.conversion import from_latlon, to_latlon


class Example(QWidget):

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
        self.graphicsView.setGeometry(QRect(30, 20, 501, 501))
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

        #self.line_1 = QLine(0,0,50,50
        

        self.pushButton.clicked.connect(self.loadReceiverData)
        #self.pushButton.clicked.connect(self.add_rectangle)
        #self.button.clicked.connect(self.add_rectangle)
        


        self.retranslateUi(Widget)

    
        
        

        

        

        

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
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
        

    def loadReceiverData(self):
        # print("bangerr")
        engine = create_engine('postgresql+psycopg2://postgres:nyhr7fv245@localhost:5432/rec403')

        check_query = "SELECT * FROM recdata"

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

        

        
        i = 0
        k = 0
        while True:
            
            lat_min = min(lats)-i
            lon_min = min(longs)-k
            lat_max = max(lats)+i
            lon_max = max(longs)+k

            minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
            maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)

            grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
            print(grid_size)

            if  501 < grid_size[0] < 502:
                print("Done finding values for lat", grid_size)
                
                while True:
                    lat_min = min(lats)-i
                    lat_max = max(lats)+i
                    minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                    maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)
                    grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                    if 501< grid_size[1] < 502:
                        break
                    i+=0.000001
                    print(grid_size)
                break

                
            if  501 < grid_size[1] < 502:
                print("Done finding values for long", grid_size)
                while True:
                    lon_min = min(longs)-k
                    lon_max = max(longs)+k
                    minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
                    maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)
                    grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
                    if 501< grid_size[0] < 502:
                        break
                    k+=0.000001
                    print(grid_size)
                break
            i += 0.000001
            k += 0.000001
       

        # 30.62550842898528, -96.3353954198505

        # 30.623668922074334, -96.33266485523458

        
        rec1 = from_latlon(latitude=  lats[0], longitude = longs[0])
        rec2 = from_latlon(latitude = lats[1], longitude = longs[1])
        rec3 = from_latlon(latitude = lats[2], longitude = longs[2])

        # minpoint = from_latlon(latitude= lat_min, longitude= lon_min)
        # maxpoint = from_latlon(latitude=lat_max, longitude=lon_max)

        print(rec1)
        print(rec2)
        print(rec3)

        print(minpoint)
        print(maxpoint)

        newrec1 = (rec1[0] - minpoint[0], rec1[1] - minpoint[1])
        newrec2 = (rec2[0] - minpoint[0], rec2[1] - minpoint[1])
        newrec3 = (rec3[0] - minpoint[0], rec3[1] - minpoint[1])

        grid_size = (maxpoint[0] - minpoint[0], maxpoint[1]-minpoint[1])
        print(grid_size)


        print("Receiver 1", "X position: ", round(newrec1[0],5), "Y position: ", round(newrec1[1],5))
        print("Receiver 2", "X position: ", round(newrec2[0],5), "Y position: ", round(newrec2[1],5))
        print("Receiver 3", "X position: ", round(newrec3[0],5), "Y position: ", round(newrec3[1],5))


        API_KEY = "b8WjT8oKxjhu9w0mBYjE"
        image = satellite_images.query((lat_min, lon_min), (lat_max, lon_max), key=API_KEY, resolution="auto")
        im = Image.fromarray(image)

        draw = ImageDraw.Draw(im)
        r = 200

        rec1_point1 = (int(newrec1[0]+5), int(newrec1[1]-40))
        rec1_point2 = (int(newrec1[0]+5+r*math.cos(math.radians(angles[0]))), int(newrec1[1]-30+r*math.sin(math.radians(angles[0]))))

        rec2_point1 = (int(newrec2[0]+25), int(newrec2[1]-10))
        rec2_point2 = (int(newrec2[0]+25+r*math.cos(math.radians(angles[1]))), int(newrec2[1]-10+r*math.sin(math.radians(angles[1]))))

        rec3_point1 = (int(newrec3[0]), int(newrec3[1]))
        rec3_point2 = (int(newrec3[0]+r*math.cos(math.radians(angles[2]))), int(newrec3[1]+r*math.sin(math.radians(angles[2]))))

        def line(p1, p2):
            a = (p1[1] - p2[1])
            b = (p2[0] - p1[0])
            c = (p1[0]*p2[1] - p2[0]*p1[1])
            return a,b,-c

        def intersection(L1, L2):
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x,y
            else:
                return False
            
        rec1_line = line(rec1_point1, rec1_point2)
        rec2_line = line(rec2_point1, rec2_point2)
        rec3_line = line(rec3_point1, rec3_point2)

        line_1_2 = intersection(rec1_line, rec2_line)
        line_1_3 = intersection(rec1_line, rec3_line)
        line_2_3 = intersection(rec2_line, rec3_line)

        centroid_data = (line_1_2, line_1_3, line_2_3)
        centroid = np.mean(centroid_data, axis = 0)
        
        center_lat_lon_data = (centroid[0]+ minpoint[0]-30, centroid[1] + minpoint[1]+50)

        center_lat_lon = to_latlon(easting=center_lat_lon_data[0], northing=center_lat_lon_data[1], zone_number=14, zone_letter='R')

        
        display_center = str(round(center_lat_lon[0],6)) +","+ str(round(center_lat_lon[1],6))
        
        self.lineEdit_5.setText(display_center)
        trans_coords = (trans_lats[0], trans_longs[0])

        errorcalc = geopy.distance.geodesic(trans_coords, center_lat_lon).m
        

        self.lineEdit_4.setText(str(round(errorcalc,2)) + " meters")
        
        draw.line((int(newrec1[0]+5), int(newrec1[1]-40), int(newrec1[0]+5+r*math.cos(math.radians(angles[0]))), int(newrec1[1]-30+r*math.sin(math.radians(angles[0])))), fill=(255, 0, 0), width=3)
        draw.line((int(newrec2[0]+25), int(newrec2[1]-10), int(newrec2[0]+25+r*math.cos(math.radians(angles[1]))), int(newrec2[1]-10+r*math.sin(math.radians(angles[1])))), fill=(255, 0, 0), width=3)
        draw.line((int(newrec3[0]), int(newrec3[1]), int(newrec3[0]+r*math.cos(math.radians(angles[2]))), int(newrec3[1]+r*math.sin(math.radians(angles[2])))), fill=(255, 0, 0), width=3)
        draw.point((line_1_2), fill=(255, 255, 0))
        draw.point((line_1_3), fill=(255, 255, 0))
        draw.point((line_2_3), fill=(255, 255, 0))
        draw.polygon((line_1_2, line_1_3, line_2_3), fill=(255, 255, 0), outline=(0, 0, 0))
        draw.point((centroid[0], centroid[1]), fill=(0, 0, 0))
        im.save('background.jpg')

        pixmap = QPixmap('background.jpg')
        self.label_10.setPixmap(pixmap)
        

        pixmap2 = QPixmap('imageedit_2_9214147233.png')

        pixmap3 = QPixmap('rsz_2.png')
        
        
        self.label_11.move(int(newrec1[0]+25), int(newrec1[1]-120))
        
        self.label_11.setPixmap(pixmap2)
        self.label_12.move(int(newrec2[0]+50), int(newrec2[1]-90))
        #self.label_12.move(20, -80)
        
        self.label_12.setPixmap(pixmap2)
        self.label_13.move(int(newrec3[0]+20), int(newrec3[1]-80))
        
        self.label_13.setPixmap(pixmap2)

        # self.label_14.setPixmap(pixmap3)
        # self.label_14.move(int(newrec3[0]+20), int(newrec3[1]-80))
       
        





def main():

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()