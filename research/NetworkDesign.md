Messages
    RaspberryPi to RoboRio
        Send to Port: 5804 (in range of 5800-5810 not on same port as listen port or driver station)

    Message 1 - Vision Target Found
        Format: 
            Message Id:         int     (4 bytes) should be a 1
            Horizontal Angle:   double  (8 bytes)
            Target Distance:    double  (8 bytes)
            Time Hour:          short   (2 bytes)
            Time Minute:        short   (2 bytes)
            Time Second:        short   (2 bytes)
            Time MicroSecond:   int     (4 bytes)
    
    Message 2 - No Vision Target Found
        Format: 
            Message Id:         int (4 bytes) should be a 2
            
    Message 3 - Contour Processed Image  
        Format:
            Message Id:         int (4 bytes) should be a 3
            Length:             int (4 bytes) size of image data
            Image Data:         byte array in BGR Mode
    
    Message 4 - Starting Camera Image 
        Format:
            Message Id:         int (4 bytes) should be a 4
            Length:             int (4 bytes) size of image data
            Image Data:         byte array in BGR Mode

    Driver Station To RaspberryPi
        RaspberryPi will listen on port: 5805 (in range of 5800-5810 not on same port as send port or driver station)

    Message 5 - Restart Vision Application
        Format:
            Message Id:         int (4 bytes) should be a 5

    Message 6 - Toggle Image Display
        Format:
            Message Id:         int (4 bytes) should be a 6
            Display Mode:       int (4 bytes)
                0 = both images off
                1 = Contour Process Image On (Message 3)
                2 = Starting Camera Image On (Message 4)
                3 = both images on
  
    Message 7 - Image Refresh Rate
        Format:
            Message Id:         int (4 Bytes) should be a 7
            Refresh Rate:       int (4 Bytes) Frames per reset (30 for every second) 