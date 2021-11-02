from ImageManager import ImageManager

# นาย ภูผา ศิริโกมลสิงห์ 61050273 \ Image Processing midterm event \
# Timeline process IMAGE : gamemaster_noise_2021.bmp -> denoiseimg.bmp -> lineimg.bmp -> grayscaleimg.bmp
# -> clusterlineimg.bmp -> clustercolorimg.bmp -> finalimg.bmp
# ps. Priority comment section : 1). """ comment """ > 2). # comment

def main():
    # เริ่มโปรแกรม
    print("program 61050273 imgage processing midterm event start here... \n")
    img = ImageManager()
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    """
        phase 1 : Denoise Image : ในเฟสที่ 1 โปรแกรมจะทำงานโดยเป้าหมายคือการลด noise ให้ได้มากที่สุด
    และต้องการทำให้ภาพไม่เสีย shape ของสีมากเกินไป
    
    """

    print("<<<<<<<< phase 1 : Denoise Image >>>>>>>> \n")
    img.read("images/gamemaster_noise_2021.bmp")
    if img is None:
        print("import failure")
        return
    print("image import successful ")
    img.deBlack()
    img.averagingFilter(9)
    img.alphaTrimmedFilter(7, 29)
    img.adjustContrast(40)
    img.averagingFilter(9)
    img.adjustContrast(40)
    img.alphaTrimmedFilter(7, 29)
    img.write("images/denoiseimg.bmp")
    print("phase 1 : Finished \n ")
    # จบ phase 1 : Denoise Image จะได้ภาพที่มีชื่อว่า denoiseimg.bmp

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    """    
        phase 2 : Turn RGB img to Grayscale img : ในเฟสที่ 2 การทำงานของโปรแกรมคือ
    จะเปลี่ยนค่าสี RGB ของภาพเป็น Grayscale เพื่อใช้ในการหาค่าสีในเฟสถัด ๆ ไปได้ง่ายขี้นในการจัดสี
    
    """

    print("<<<<<<<< phase 2 : Turn RGB img to Grayscale img >>>>>>>> \n")
    img.read("images/denoiseimg.bmp")
    if img is None:
        print("import failure")
        return
    print("image import successful")
    img.deBackground()
    img.setWhite()
    img.pickIndexEdge()
    img.makeItBlue()
    img.rgb2gray()
    img.write("images/lineimg.bmp")

    """
        สำคัญ ในเฟสที่ 2 นี้เราต้องการ Grayscale 2 รูปโดยมาจากรูป denoiseimg.bmp เหมือนกัน วิธีทำ grayscale เหมือนกัน
    แต่ จะไม่เหมือนกันตรงที่รูปแรกจะมีการเปลี่ยนพื้นหลังก่อน เป็นรูป lineimg.bmp เพื่อที่เราจะได้ความต่างตรงกรอบของตัวละครกับพื้นหลัง
    และจะทำการไล่ลงสีต่อไป
    
    """

    # การทำงานในเฟส 2 ทำเป็น grayscale คือเปลี่ยนสีทั้งรูปเป็ํนฟ้า จะได้คอนทราสที่มากพอที่จะไม่ทำให้ตัวละครไปกลืนพื่นหลัง
    #จากนั้นก็แปลงเป็น rgb to grayscale
    # จบ phase 2 : Turn RGB img to Grayscale img จะได้ภาพ
    # ภาพที่ 1 : lineimg.bmp

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    """"
    phase 3 : Find dominant colors in img , set color range : วิธีการนี้จะไล่ sort หาสีเพื่อมาแสดงว่าสีในถูกใช้มากที่สุด
    โดยจะใช้ค่าสีที่มากที่สุดของี๔ปนี้มา set range ของสีของภาพจากเฟส 2 คือ lineimg.bmp และ grayscaleimg.bmp
    process นี้จะได้ภาพเหมือนวิธีการทำ nearest color neighbour โดย spec ไว้ที่ 3 สีหลักของรูป (ได้มาจากหาสีที่มากที่สุด) (k = 3)
    
    """
    print("<<<<<<<< phase 3 : Find dominant colors in img , set color range >>>>>>>> \n")

    # ใช้วิเคราะห์สีที่ใช้มากที่สุด แต่ไม่ได้ใช้วิธีการนี้เพราะการลดขนาดรูปของ pillow เป็นการทำ average ทำให้เกิดสีใหม่ขึ้นจึงใช้ไม่ได้
    # img.read("images/colorimg.bmp")
    # img.find_dominant_color()
    # img.resizeImg()
    # img.writeTemp("images/2.bmp")

    """ 
    ใช้วิเคราะห์สีที่ใช้มากที่สุดโดย ใช้การทำ MaxPooling โดยมี Kernel = 10 * 10 จะได้สีที่เด่นที่สุดของรูปจริง ๆ และนำมาใช้ในการ set range สีของภาพ
    โดยที่วิธีนี้จะทำกับรูปที่ได้รับมาจากเฟสก่อน คือจะทำการเกลี่ยสีรูปทั้งรูปให้ได้แค่ 3 สี (ได้มาจากหาสีที่มากที่สุด)
    
    """

    # รูปแรกจะทำการเกลี่ยสีคือ lineimg.bmp ในการทำรูปนี้จะเก็บข้อมูลแค่เส้นกรอบรูประหว่างตัวละครและพื้นหลัง
    # จากนั้นจะเก็บ cordinate ของเส้นกรอบไว้เพื่อนำไปใช้เขียนลงในรูปหลัก
    img.read("images/lineimg.bmp")
    if img is None:
        print("import failure")
        return
    print("image import successful")
    img.maxPooling()
    img.find_dominant_color()
    img.setColbyPick()
    img.paddingBG()
    img.write("images/clusterlineimg.bmp")

    # จบ phase 3 : Find dominant colors in img , set color range
    # ภาพที่ 1 : clusterlineimg.bmp ใช้นำไปลงสี
    # รูปนี้คือรูปที่ต้องการจำเกลี่ยสีเพื่อนำไป set สีในภาพโดยจะเกลี่ยเป็น 3 สีคือ 1.พื้นหลัง 2.สีผม แว่นตา หนวด เสื้อ 3.หน้า คอ

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    """ 
    phase 4 : set colors : เปลี่ยนสีทั้งหมดของภาพ
    
    """
    print("<<<<<<<< phase 4 : set colors >>>>>>>> \n")

    img.read("images/clusterlineimg.bmp")
    if img is None:
        print("import failure")
        return
    print("image import successful")
    img.setColorMain()
    img.setColorSkin()
    img.drawEdge()
    img.paddingBG()
    img.setColorBG()
    img.write("images/finalimg.bmp")
    print("phase 4 : Finished \n ")
    # จบ phase 4 : set colors จะได้ภาพสุดท้ายที ลงสีตามโจทย์ ตัดเส้น paddingขอบรูป
    # ภาพที่ final : finalimg.bmp


if __name__ == "__main__":
    main()
