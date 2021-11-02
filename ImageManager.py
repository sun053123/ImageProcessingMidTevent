import math
import random
from PIL import Image
import numpy as np


class ImageManager:

    def __init__(self, width=None, height=None, bitDepth=None, img=None, data=None, origin=None, tempdata=None,
                 maxpool=None, edge=None, index_skin=None, index_glasses=None, index_mouth=None):
        self.width = width
        self.height = height
        self.bitDepth = bitDepth
        self.img = img
        self.data = data
        self.origin = origin

        self.tempdata = tempdata
        self.maxpool = maxpool
        self.edge = edge
        self.index_skin = index_skin
        self.index_glasses = index_glasses
        self.index_mouth = index_mouth

    def read(self, fileName):
        self.img = Image.open(fileName)
        self.data = np.array(self.img)
        self.original = np.copy(self.data)
        self.width = self.data.shape[0]
        self.height = self.data.shape[1]
        mode_to_bpp = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32,
                       "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}
        bitDepth = mode_to_bpp[self.img.mode]

        print(
            "Image %s with %s x %s pixels (%s bits per pixel)  data has been read!" % (
                self.img.filename, self.width, self.height, bitDepth))

    def write(self, fileName):
        img = Image.fromarray(self.data)
        try:
            img.save(fileName)
        except:
            print("Write file error")
        else:
            print("Image %s has been written!" % (fileName))

    def writeTemp(self, TempImg):
        img = Image.fromarray(self.tempdata)
        try:
            img.save(TempImg)
        except:
            print("Temp for avg fail")
        else:
            print("Image %s has been written!" % (TempImg))

    def restoreToOriginal(self):
        self.data = np.copy(self.original)

    def alphaTrimmedFilter(self, size: int, d: int):
        data = self.data
        width = self.width
        height = self.height

        if (size % 2 == 0):
            print("Size Invalid: must be odd number!")
            return

        data_zeropaded = np.zeros([width + int(size / 2) * 2, height + int(size / 2) * 2, 3])
        data_zeropaded[int(size / 2):width + int(size / 2), int(size / 2):height + int(size / 2), :] = data

        for y in range(height):
            for x in range(width):
                subData = data_zeropaded[x:x + size + 1, y:y + size + 1, :]
                sortedRed = np.sort(subData[:, :, 0:1], axis=None)
                sortedGreen = np.sort(subData[:, :, 1:2], axis=None)
                sortedBlue = np.sort(subData[:, :, 2:3], axis=None)

                r = np.mean(sortedRed[int(d / 2): size * size - int(d / 2) + 1])
                r = 255 if r > 255 else r
                r = 0 if r < 0 else r
                g = np.mean(sortedGreen[int(d / 2): size * size - int(d / 2) + 1])
                g = 255 if g > 255 else g
                g = 0 if g < 0 else g
                b = np.mean(sortedBlue[int(d / 2): size * size - int(d / 2) + 1])
                b = 255 if b > 255 else b
                b = 0 if b < 0 else b

                data[x, y, 0] = r
                data[x, y, 1] = g
                data[x, y, 2] = b

    def rgb2gray(self):
        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                graysclae = (self.data[x, y, 0] * 0.299) + (self.data[x, y, 1] * 0.587) + (self.data[x, y, 2] * 0.114)
                self.data[x, y] = graysclae

    def setWhite(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x, y, 0] <= 200 \
                        and self.data[x, y, 0] >= 165 \
                        and self.data[x, y, 1] <= 200 \
                        and self.data[x, y, 1] >= 165 \
                        and self.data[x, y, 2] <= 200 \
                        and self.data[x, y, 2] >= 165:
                    self.data[x, y, 0] = 120
                    self.data[x, y, 1] = 120
                    self.data[x, y, 2] = 120

    def deBlack(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x, y, 0] == 0 and self.data[x, y, 0] == 0 and self.data[x, y, 0] == 0:
                    self.data[x, y, 0] = self.data[x, y - 1, 0]
                    self.data[x, y, 1] = self.data[x, y - 1, 1]
                    self.data[x, y, 2] = self.data[x, y - 1, 2]
                else:
                    self.data[x, y] = self.data[x, y]

    def resizeImg(self):
        resized_img = self.img.resize((round(self.img.size[0] * 0.15), round(self.img.size[1] * 0.15)))
        self.tempdata = np.array(resized_img)

    def find_most_color(self):
        pixels = self.img.getcolors(self.width * self.height)
        sorted_pixels = sorted(pixels, key=lambda t: t[0])
        # Get the most frequent color
        dominant_color = sorted_pixels[-1][1]
        print(dominant_color)  #

    def averagingFilter(self, size):
        if (size % 2 == 0):
            print("Size Invalid: must be odd number!")
            return

        data_zeropaded = np.zeros([self.width + int(size / 2) * 2, self.height + int(size / 2) * 2, 3])
        data_zeropaded[int(size / 2):self.width + int(size / 2), int(size / 2):self.height + int(size / 2),
        :] = self.data

        for y in range(int(size / 2), int(size / 2) + self.height):
            for x in range(int(size / 2), int(size / 2) + self.width):
                subData = data_zeropaded[x - int(size / 2):x + int(size / 2) + 1,
                          y - int(size / 2):y + int(size / 2) + 1, :]

                avgRed = np.mean(subData[:, :, 0:1])
                avgGreen = np.mean(subData[:, :, 1:2])
                avgBlue = np.mean(subData[:, :, 2:3])
                avgRed = 255 if avgRed > 255 else avgRed
                avgRed = 0 if avgRed < 0 else avgRed
                avgGreen = 255 if avgGreen > 255 else avgGreen
                avgGreen = 0 if avgGreen < 0 else avgGreen
                avgBlue = 255 if avgBlue > 255 else avgBlue
                avgBlue = 0 if avgBlue < 0 else avgBlue
                self.data[x - int(size / 2), y - int(size / 2), 0] = avgRed
                self.data[x - int(size / 2), y - int(size / 2), 1] = avgGreen
                self.data[x - int(size / 2), y - int(size / 2), 2] = avgBlue

    def adjustBrightness(self, brightness):
        for y in range(self.height):
            for x in range(self.width):
                r = self.data[x, y, 0]
                g = self.data[x, y, 1]
                b = self.data[x, y, 2]
                r = r + brightness
                r = 255 if r > 255 else r
                r = 0 if r < 0 else r
                g = g + brightness
                g = 255 if g > 255 else g
                g = 0 if g < 0 else g
                b = b + brightness
                b = 255 if b > 255 else b
                b = 0 if b < 0 else b
                self.data[x, y, 0] = r
                self.data[x, y, 1] = g
                self.data[x, y, 2] = b

    def getGrayscaleHistogram(self):
        histogram = np.array([0] * 256)
        for y in range(self.height):
            for x in range(self.width):
                histogram[self.data[x, y, 0]] += 1

        return histogram

    def getContrast(self):
        contrast = 0.0

        histogram = self.getGrayscaleHistogram()
        avgIntensity = 0.0
        pixelNum = self.width * self.height

        for i in range(len(histogram)):
            avgIntensity += histogram[i] * i

        avgIntensity /= pixelNum

        for y in range(self.height):
            for x in range(self.width):
                contrast += (self.data[x, y, 0] - avgIntensity) ** 2

        contrast = (contrast / pixelNum) ** 0.5
        return contrast

    def adjustContrast(self, contrast):
        currentContrast = self.getContrast()
        histogram = self.getGrayscaleHistogram()
        avgIntensity = 0.0
        pixelNum = self.width * self.height
        for i in range(len(histogram)):
            avgIntensity += histogram[i] * i
        avgIntensity /= pixelNum
        min = avgIntensity - currentContrast
        max = avgIntensity + currentContrast
        newMin = avgIntensity - currentContrast - contrast / 2
        newMax = avgIntensity + currentContrast + contrast / 2
        newMin = 0 if newMin < 0 else newMin
        newMax = 0 if newMax < 0 else newMax
        newMin = 255 if newMin > 255 else newMin
        newMax = 255 if newMax > 255 else newMax

        if (newMin > newMax):
            temp = newMax
            newMax = newMin
            newMin = temp

        contrastFactor = (newMax - newMin) / (max - min)

        for y in range(self.height):
            for x in range(self.width):
                r = self.data[x, y, 0]
                g = self.data[x, y, 1]
                b = self.data[x, y, 2]
                contrast += (self.data[x, y, 0] - avgIntensity) ** 2
                r = (int)((r - min) * contrastFactor + newMin)
                r = 255 if r > 255 else r
                r = 0 if r < 0 else r
                g = (int)((g - min) * contrastFactor + newMin)
                g = 255 if g > 255 else g
                g = 0 if g < 0 else g
                b = (int)((b - min) * contrastFactor + newMin)
                b = 255 if b > 255 else b
                b = 0 if b < 0 else b
                self.data[x, y, 0] = r
                self.data[x, y, 1] = g
                self.data[x, y, 2] = b

    def makeItBlue(self):
        for x in range(self.width):
            for y in range(self.height):
                self.data[x, y, 0] = self.data[x, y, 0] * 0.1
                self.data[x, y, 1] = self.data[x, y, 1] * 0.1

    def deBackground(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x, y, 0] <= 255 \
                        and self.data[x, y, 0] >= 183 \
                        and self.data[x, y, 1] <= 255 \
                        and self.data[x, y, 1] >= 230 \
                        and self.data[x, y, 2] <= 230:
                    self.data[x, y, 0] = 254
                    self.data[x, y, 1] = 254
                    self.data[x, y, 2] = 254

    def setColbyPick(self):
        for x in range(self.width):
            for y in range(self.height):
                col1 = self.data[x, y, 0] - 36
                col2 = self.data[x, y, 0] - 51
                col3 = self.data[x, y, 0] - 29
                col4 = self.data[x, y, 0] - 47

                # print("sum" , col1,col2,col3,col4)
                if abs(col1) <= abs(col2) and abs(col3) and abs(col4):
                    self.data[x, y, 0] = 39
                    self.data[x, y, 1] = 39
                    self.data[x, y, 2] = 39
                if abs(col2) <= abs(col1) and abs(col3) and abs(col4):
                    self.data[x, y, 0] = 254
                    self.data[x, y, 1] = 254
                    self.data[x, y, 2] = 254
                if abs(col3) <= abs(col1) and abs(col2) and abs(col4):
                    self.data[x, y, 0] = 24
                    self.data[x, y, 1] = 24
                    self.data[x, y, 2] = 24
                if abs(col4) <= abs(col1) and abs(col2) and abs(col4):
                    self.data[x, y, 0] = 47
                    self.data[x, y, 1] = 47
                    self.data[x, y, 2] = 47

    def maxPooling(self):
        kernel_size = 10
        final_size = self.width - kernel_size + 1

        final = [[0 for i in range(final_size)] for j in range(final_size)]
        arr_tmp = [[0 for i in range(kernel_size)] for j in range(kernel_size)]

        for y in range(final_size):
            # print('y: ', y)
            for x in range(final_size):
                # print('x: ', x)
                for i in range(kernel_size):
                    for j in range(kernel_size):
                        arr_tmp[i][j] = self.data[y + i, x + j, 0]
                final[y][x] = np.amax(arr_tmp)
                # print(arr_tmp)
        self.maxpool = final

    def find_dominant_color(self):
        dictc = {}
        self.maxpool = np.array(self.maxpool)
        maxpool_w = self.maxpool.shape[0]
        maxpool_h = self.maxpool.shape[1]
        for x in range(maxpool_w):
            for y in range(maxpool_h):
                h = self.maxpool[x, y]
                if h in dictc:
                    dictc[h] = dictc[h] + 1
                else:
                    dictc[h] = 1
                    # now sort it by values rather than keys descending
        print("Dominant Colors =  ", sorted(dictc.items(), key=lambda x: x[1], reverse=True))

    def pickIndexEdge(self):
        edge = []
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x, y, 0] == 120 and self.data[x, y, 1] == 120 and self.data[x, y, 2] == 120:
                    edge.append([y, x])
        self.edge = edge

    def drawEdge(self):
        for i in range(len(self.edge)):
            self.data[self.edge[i][1], self.edge[i][0], 0] = 255
            self.data[self.edge[i][1], self.edge[i][0], 1] = 255
            self.data[self.edge[i][1], self.edge[i][0], 2] = 255

    def paddingBG(self):
        for x in range(8):
            for y in range(self.height):
                self.data[x, y, 0] = 254
                self.data[x, y, 1] = 254
                self.data[x, y, 2] = 254
        for x in range(self.height):
            for y in range(35):
                self.data[x, y, 0] = 254
                self.data[x, y, 1] = 254
                self.data[x, y, 2] = 254
        for x in range(self.width):
            for y in range(self.height - 30, self.height):
                self.data[x, y, 0] = 254
                self.data[x, y, 1] = 254
                self.data[x, y, 2] = 254
        for x in range(self.width - 5, self.width):
            for y in range(self.height):
                self.data[x, y, 0] = 254
                self.data[x, y, 1] = 254
                self.data[x, y, 2] = 254

    def setColorMain(self):
        map_colour = {
            0: [0, 0, 0],
            1: [160, 160, 160],
            2: [0, 0, 0],
            3: [255, 80, 0],
            4: [255, 0, 0]
        }

        target = 24
        target_skin = 47
        target_skin2 = 39
        self.index_skin = []
        self.index_glasses = []
        self.index_mouth = []
        switch_zone = True
        zone = 0

        for x in range(self.height - 6):
            tmp = []
            for y in range(self.width):
                tmp.append(self.data[x, y, 0])
                if self.data[x, y, 0] == target:
                    self.data[x, y, 0] = map_colour[zone][0]
                    self.data[x, y, 1] = map_colour[zone][1]
                    self.data[x, y, 2] = map_colour[zone][2]
                    switch_zone = True
                    if zone == 2:
                        self.index_glasses.append([y, x])
                    elif zone == 3:
                        self.index_mouth.append([y, x])
                elif self.data[x, y, 0] == target_skin or self.data[x, y, 0] == target_skin2:
                    self.index_skin.append([y, x])
            if not target in tmp and switch_zone:
                zone += 1
                print("switch to zone ", zone)
                switch_zone = False

    def setColorSkin(self):
        for i in range(len(self.index_skin)):
            self.data[self.index_skin[i][1], self.index_skin[i][0], 0] = 189
            self.data[self.index_skin[i][1], self.index_skin[i][0], 1] = 154
            self.data[self.index_skin[i][1], self.index_skin[i][0], 2] = 122

    def setColorBG(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x, y, 0] == 254 and self.data[x, y, 1] == 254 and self.data[x, y, 2] == 254:
                    self.data[x, y, 0] = 0
                    self.data[x, y, 1] = 100
                    self.data[x, y, 2] = 190

53