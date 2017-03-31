# Summary 
Now a days most of the photos captuted using phone tagged with gps location. So when you upload to online site like google photo it get photo captured location and show the map of that location.  This python script allows add GPS location OR change existing location of the photo if gps tag not added to picture or need to change the location of the photo.

# Dependancy

     $ pip install piexif 

# Example Usage

        jpg_gps = jpeg_exif_handle()
        jpg_gps.set_owner("RPI3 Tensorflow")
        
        latitude = 37.386051
        longitude = -122.083855
        #Set gps coordinate latitude, longitude
        jpg_gps.set_gps(latitude, longitude)
        
        jpg_gps.fix_jpeg_exif(jpg_image_file_name)

# Example picture

  gps-location-update.jpg

# Other application usage

The reason I wanted to edit or add gps location of picture mainly for opencv applications. For example  OpenCV video capture API we can capture photo or live Video. When you save these picture into jpg image format you dont get gps coordinate where that photo taken.

Added Android application which broadcast current gps location to server application which can run any system.

