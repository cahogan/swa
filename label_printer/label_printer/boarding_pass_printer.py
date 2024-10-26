import os
from PIL import Image, ImageDraw, ImageFont
# import zpl
from zebrafy import ZebrafyImage
import socket
from datetime import datetime, timedelta
import math
import pdf417 # For barcodes.
from random import randint # for boarding pass greebling

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REGULAR_FONT_PATH = os.path.join(SCRIPT_DIR, "fonts", "FragmentMono-Regular.ttf")
ITALIC_FONT_PATH = os.path.join(SCRIPT_DIR, "fonts", "FragmentMono-Italic.ttf")

PRINTER_DPI = 300
MM_PER_IN = 25.4
BOARDING_PASS_WIDTH_IN = 8
BOARDING_PASS_HEIGHT_IN = 3.25
BOARDING_PASS_FONT_SMALL_HEIGHT_MM = 2.3
BOARDING_PASS_FONT_MEDIUM_HEIGHT_MM = 4
BOARDING_PASS_FONT_LARGE_HEIGHT_MM = 7

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

class ZPLPrinter:
    def __init__(self, ip, port=9100):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def __enter__(self):
        self.socket.connect((self.ip, self.port)) #connecting to ip
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.socket.close() #closing connection
    
    def send_zpl(self, zpl_str):
        """
        Encodes a ZPL string as ASCII and sends it to the printer.
        """
        try:
            self.socket.send(zpl_str.encode("ascii"))#using bytes
            
        except:
            raise Exception("Error with the connection")
        
def in2d(inches):
    """
    Helper function that converts inch value to dots using PRINTER_DPI.
    @param[in] inches Single value or tuple, in inches, to be converted to dots.
    """
    if isinstance(inches, tuple):
        return tuple(round(dim * PRINTER_DPI) for dim in inches)
    else:
        return round(inches * PRINTER_DPI)
    
def in2mm(inches):
    """
    Helper function that converts inch value to mm using MM_PER_IN.
    @param[in] inches Single value or tuple, in inches, to be converted to mm.
    """
    if isinstance(inches, tuple):
        return tuple(round(dim * MM_PER_IN) for dim in inches)
    else:
        return round(inches * MM_PER_IN)
    
def mm2d(mm):
    """
    Helper function that converts mm value to dots using PRINTER_DPI.
    @param[in] mm Single value or tuple, in millimeters, to be converted to dots.
    """
    if isinstance(mm, tuple):
        return tuple(round(dim * PRINTER_DPI / MM_PER_IN) for dim in mm)
    else:
        return round(mm * PRINTER_DPI / MM_PER_IN)
    
def d2mm(dots):
    """
    Helper function that converts dots value to mm using PRINTER_DPI.
    @param[in] dots Single value or tuple, in dots, to be converted to mm.
    """
    if isinstance(dots, tuple):
        return tuple(round(dim / PRINTER_DPI * MM_PER_IN) for dim in dots)
    else:
        return round(dots / PRINTER_DPI * MM_PER_IN)
    
        
def generate_boarding_pass(
        ticket_id="123",
        lastname="Paxton", 
        firstname="Edween", 
        gate="E6", 
        departure_datetime=datetime.now() + timedelta(minutes=30), 
        boarding_datetime=datetime.now(), 
        confirmation_number="3BHRJA", 
        departure_airport_code="HNL",
        departure_airport_city="Honolulu",
        departure_airport_name="Daniel K. Inouye International Airport",
        arrival_airport_city="San Jose",
        arrival_airport_name="Norman Y. Mineta San Jose International Airport", 
        arrival_airport_code="SJC", 
        flight_number="1204", 
        boarding_group="A", 
        boarding_position=52
):
    image = Image.new('RGB', in2d((BOARDING_PASS_WIDTH_IN, BOARDING_PASS_HEIGHT_IN)), COLOR_WHITE) # white background
    draw = ImageDraw.Draw(image)

    # Load a font (adjust size as necessary for larger DPI)
    font_large = ImageFont.truetype(REGULAR_FONT_PATH, mm2d(BOARDING_PASS_FONT_LARGE_HEIGHT_MM))
    font_medium = ImageFont.truetype(REGULAR_FONT_PATH, mm2d(BOARDING_PASS_FONT_MEDIUM_HEIGHT_MM))
    font_small = ImageFont.truetype(REGULAR_FONT_PATH, mm2d(BOARDING_PASS_FONT_SMALL_HEIGHT_MM))

    # Barcode
    barcode_str = f"{ticket_id}-{flight_number}-{confirmation_number}-{lastname}/{firstname}-{boarding_group}{boarding_position}"
    barcode_image = pdf417.render_image(pdf417.encode(barcode_str, security_level=6, columns=10)).rotate(270, expand=True)
    # barcode_image.show()
    image.paste(barcode_image, mm2d((127,17))) # Primary barcode
    image.paste(barcode_image, mm2d((185,17))) # Tab barcode

    # Header
    logo_image = Image.open(os.path.join(SCRIPT_DIR, "images", "swa_ticket_logo.png"))
    image.paste(logo_image, mm2d((14,0)))
    draw.text(mm2d((96, 10)), f"BOARDING PASS", font=font_medium, stroke_width=1, fill=COLOR_BLACK)


    # Primary Info Section
    offset_y = 4
    draw.text(mm2d((15, 12+offset_y)), f"{lastname.upper()}/{firstname.upper()}", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((15, 16+offset_y)), f"{firstname.upper()} {lastname.upper()}", font=font_small, fill=COLOR_BLACK)
    draw.text(mm2d((15, 20+offset_y)), f"FLIGHT", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((35, 20+offset_y)), f"{flight_number}", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((61, 20+offset_y)), f"GATE", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((73, 20+offset_y)), f"{gate}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 24+offset_y)), f"{departure_datetime.strftime('%b %d, %Y')}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 28+offset_y)), f"CONFIRMATION NUMBER: {confirmation_number}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 33+offset_y)), f"FROM  TO  FLT    TIME    FB BOARDING", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 38+offset_y)), f"{departure_airport_code}   {arrival_airport_code} {flight_number}  {departure_datetime.strftime('%I:%M%p')}  F  {boarding_datetime.strftime('%I:%M%p')}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 45+offset_y)), f"Wanna Get A Treat(R)", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((15, 72+offset_y)), f"{boarding_position}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((101, 74+offset_y)), f"{confirmation_number}", font=font_medium, fill=COLOR_BLACK)

    # Primary Barcode Section
    draw.rectangle([mm2d((107, 19)), mm2d((129, 49))], outline="black", width=4)
    draw.text(mm2d((108, 21)), f"BOARDING", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((112, 25)), f"GROUP", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((115, 29)), f"{boarding_group}", font=font_large, stroke_width=2, fill=COLOR_BLACK)
    draw.text(mm2d((108, 37)), f"POSITION", font=font_medium, fill=COLOR_BLACK)
    bp_str = f"{boarding_position}"
    bp_w = d2mm(draw.textlength(bp_str, font=font_large))
    draw.text(mm2d((117-bp_w/2, 42)), bp_str, font=font_large, stroke_width=2, fill=COLOR_BLACK)

    # Tab
    draw.text(mm2d((188, 11)), f"{boarding_position}", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((148, 3)), f"SWEETWEST AIRLINES", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((148, 7)), f"OPEN SEATING", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((148, 19)), f"{lastname.upper()}/{firstname.upper()}", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((148, 24)), f"CONF {confirmation_number}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((148, 28)), f"{departure_datetime.strftime('%b %d, %Y')}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((148, 34)), f"{flight_number} {departure_airport_city.upper()} {departure_airport_name.upper()}"[:25], font=font_small, fill=COLOR_BLACK)
    draw.text(mm2d((148, 38)), f"TO {arrival_airport_city.upper()} {arrival_airport_name.upper()}"[:25], font=font_small, fill=COLOR_BLACK)
    draw.text(mm2d((148, 49)), f"{''.join([str(randint(0, 9)) for i in range(11)])}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((148, 54)), f"TT", font=font_medium, fill=COLOR_BLACK)

    draw.rectangle([mm2d((148, 62)), mm2d((176, 72))], outline="black", width=4)
    draw.text(mm2d((149, 63)), f"{boarding_group}", font=font_large, stroke_width=2, fill=COLOR_BLACK)
    draw.text(mm2d((165-bp_w/2, 63)), bp_str, font=font_large, stroke_width=2, fill=COLOR_BLACK)

    # image.show()

    return image

def print_boarding_pass(image, printer_ip="192.168.1.173"):
    image_rotated = image.rotate(90, expand=True)
    # image_rotated.show()
    zpl_string = ZebrafyImage(image_rotated, invert=True, pos_x=mm2d(12)).to_zpl()
    # print(zpl_string)
    with ZPLPrinter(printer_ip) as zd621:
        zd621.send_zpl(zpl_string)

# Test it out!
# print_boarding_pass(generate_boarding_pass())