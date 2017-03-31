class jpeg_exif_handle(object):

    def __init__(self):
        self.filename = ""
        self.latitude = 0
        self.longitude = 0
        self.file_owner = "RPI3"
        return

    def set_gps(self, gps_latitude_dec, gps_longitude_dec):
        self.latitude = gps_latitude_dec
        self.longitude = gps_longitude_dec
        return

    def set_owner (self, owner_name = "RPI3"):
        self.file_owner = owner_name
        return

    def fix_jpeg_exif (self, jpg_file):
        self.filename = jpg_file
        self.create_exif()
        self.write_gps_tag()

        return

    def gps_to_dms(self, deg):
        d = int(deg)
        md = abs(deg - d) * 60
        m = int(md)
        sd = int((md - m) * 60)

        return [d, m, sd]

    def create_exif(self):

        o = io.BytesIO()
        thumb_im = Image.open(self.filename)

        #thumb_im.thumbnail([128,128], Image.ANTIALIAS)
        thumb_im.save(o, "jpeg")

        w,h = thumb_im.size
        zeroth_ifd = {piexif.ImageIFD.Make: u"RaspberryPI3",
                      piexif.ImageIFD.XResolution: (w, 1),
                      piexif.ImageIFD.YResolution: (h, 1),
                      piexif.ImageIFD.Software: u"Raspian RP3"
                      }

        filedatetime = time.strftime("%Y:%m:%d") + ' ' + time.strftime("%H:%M:%S")

        exif_ifd = {piexif.ExifIFD.DateTimeOriginal: filedatetime, #u"2017:03:16 15:29:10",
                    piexif.ExifIFD.LensMake: u"RPI3",
                    piexif.ExifIFD.Sharpness: 65535,
                    piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
                    }
        gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
                   piexif.GPSIFD.GPSAltitudeRef: 1,
                   piexif.GPSIFD.GPSDateStamp: filedatetime, #u"2017:03:16 03:45:32",

                   }
        first_ifd = {piexif.ImageIFD.Make: u"RaspberryPI3",
                     piexif.ImageIFD.XResolution: (40, 1),
                     piexif.ImageIFD.YResolution: (40, 1),
                     piexif.ImageIFD.Software: u"Raspian RP3"
                     }
        try:

            exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd}

            exif_bytes = piexif.dump(exif_dict)

            im = Image.open(self.filename)

            #im.thumbnail(thumb_im.size, Image.ANTIALIAS)
            im.save(self.filename, exif=exif_bytes)
            #print("**** create_exif() success File Name and Time ", self.filename, filedatetime)
        except OSError as err:
            print("create_exif() error: {0}".format(err))
        return

    #Function to write location of photo it shot
    def write_gps_tag (self):

        nameoffile = self.filename

        im = Image.open(nameoffile)
        exif_dict = piexif.load(im.info["exif"])
        """"
        w, h = im.size

        exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
        exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
        """

        #Modify Jpeg EXIF information
        exif_dict["0th"][piexif.ImageIFD.Copyright] = "RaspiRepo"
        exif_dict["0th"][piexif.ImageIFD.Make] = "RPI3"
        exif_dict["0th"][piexif.ImageIFD.Model] = "RPI3"
        exif_dict["Exif"][piexif.ExifIFD.CameraOwnerName] = self.file_owner

        #Writing  GPS location latitude
        d,m,sd = self.gps_to_dms(self.latitude)
        h = 'N'
        if (d < 0):
            h = 'S'

        #Set latitude
        gps_latitude = (abs(d), 1), (m, 1), (sd, 100)
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = h
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = gps_latitude

        lat_deg = str(d) + "." + str(m) + "." + str(sd) + h

        d,m,sd = self.gps_to_dms(self.longitude)
        h = 'E'
        if (d < 0):
            h = 'W'

        #Set longitude
        gps_longitude = (abs(d), 1), (m, 1), (sd, 100)
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = h
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = gps_longitude
        lon_deg = str(d) + "." + str(m) + "." + str(sd) + h

        #print("Location of Frame Coordinate " , lat_deg, lon_deg)
        try:
            exif_bytes = piexif.dump(exif_dict)
            im.save(nameoffile, "jpeg", exif=exif_bytes)
        except OSError as err:
            print("write_gps_tag() error: {0}".format(err))

        return

    def get_local_folder_images (self, folder_name):

        folder_name = '{}{}'.format('', folder_name)
        files = os.listdir(folder_name)
        #for filename in files:
            #print(filename)
        return files

    def getfiles(self, dirpath):
        a = [s for s in os.listdir(dirpath)
             if os.path.isfile(os.path.join(dirpath, s))]
        a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        return a

    def update_folder_images_exif(self, folder_name):
        file_list = self.getfiles(folder_name)
        for name_of_file in file_list:
            self.create_exif(name_of_file)
        return
