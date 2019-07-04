import time
import logging
import sys

#Let's emulate the flipdot sign
class flipdotSim:
 
    reset = "\u001b[0m"
    blank_string = "\u001b[30;1m░" + reset
    filled_string = "\u001b[33;1m▓" + reset
    init_string = "\u001b[0;0H"
    erase_line = "\u001b[K"
    clear_display = "\u001b[2J"
    restore_cursor = "\u001b[u"
    LOG_LEVEL = logging.DEBUG

    def __init__(self, columns, rows):
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)
        self.columns = columns
        self.rows = rows
        #sys.stdout.write(self.clear_display)
        #sys.stdout.flush()
        pass

    def render_image(self, image):

        image_error = False
        error_message = ""

        # Check if image is valid (rows)
        if len(image) != self.rows:
            if len(image) > self.rows:
                error_message += "Image is too long. "
            elif len(image) < self.rows:
                error_message += "Image is too short. "
            error_message += "{} found, expected {}. ".format(len(image), self.rows)
            image_error = True
            
        # Check if image is valid (columns)
        if len(image[0]) != self.columns:
            if len(image[0]) > self.columns:
                error_message += "Image is too tall. "
            elif len(image[0]) < self.columns:
                error_message += "Image is too short. "
            error_message += "{} found, expected {}. ".format(len(image[0]), self.columns)
            image_error = True

        if image_error:
            error_message += "Refusing to display a invalid image."
            self.logger.error(error_message)
            raise ValueError(error_message)

        sys.stdout.write(self.init_string)
        for x in image:
            for y in x:
                if y == True:
                    sys.stdout.write(self.filled_string)
                if y == False:
                    sys.stdout.write(self.blank_string)
            sys.stdout.write("\n")
        for i in range(6):
            sys.stdout.write(self.erase_line+ "\n")

        sys.stdout.flush()
        time.sleep( .8 )

    
    def clean(self):
        sys.stdout.write(self.restore_cursor)
        sys.stdout.flush()


            
                



        
