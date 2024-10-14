import os
from PIL import Image, ImageDraw, ImageFont
# import zpl
from zebrafy import ZebrafyImage
import socket
from datetime import datetime, timedelta
import math
import pdf417 # For barcodes.

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REGULAR_FONT_PATH = os.path.join(SCRIPT_DIR, "fonts", "FragmentMono-Regular.ttf")
ITALIC_FONT_PATH = os.path.join(SCRIPT_DIR, "fonts", "FragmentMono-Italic.ttf")

PRINTER_DPI = 300
MM_PER_IN = 25.4
BOARDING_PASS_WIDTH_IN = 8
BOARDING_PASS_HEIGHT_IN = 3.25
BOARDING_PASS_FONT_SMALL_HEIGHT_MM = 2
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
    
    def __exit__(self):
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
        departure_datetime=datetime.now() - timedelta(minutes=30), 
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
    barcode_image.show()
    
    image.paste(barcode_image, mm2d((127,17)))

    # Header

    draw.text(mm2d((96, 10)), f"BOARDING PASS", font=font_medium, stroke_width=1, fill=COLOR_BLACK)


    # Left Info Section
    draw.text(mm2d((15, 12)), f"{lastname.upper()}/{firstname.upper()}", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((15, 16)), f"{firstname.upper()} {lastname.upper()}", font=font_small, fill=COLOR_BLACK)
    draw.text(mm2d((15, 20)), f"FLIGHT", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((35, 20)), f"{flight_number}", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((61, 20)), f"GATE", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((73, 20)), f"{gate}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 24)), f"{departure_datetime.strftime('%b %d, %Y')}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 28)), f"CONFIRMATION NUMBER: {confirmation_number}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 33)), f"FROM  TO  FLT    TIME    FB BOARDING", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 38)), f"{departure_airport_code}   {arrival_airport_code} {flight_number}  {departure_datetime.strftime('%I:%M%p')}  F  {boarding_datetime.strftime('%I:%M%p')}", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((15, 45)), f"Wanna Get A Treat(R)", font=font_medium, stroke_width=1, fill=COLOR_BLACK)
    draw.text(mm2d((15, 72)), f"{boarding_position}", font=font_medium, fill=COLOR_BLACK)

    # Left barcode section
    draw.rectangle([mm2d((107, 19)), mm2d((129, 49))], outline="black", width=3)
    draw.text(mm2d((108, 21)), f"BOARDING", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((112, 25)), f"GROUP", font=font_medium, fill=COLOR_BLACK)
    draw.text(mm2d((115, 29)), f"{boarding_group}", font=font_large, stroke_width=2, fill=COLOR_BLACK)
    draw.text(mm2d((108, 37)), f"POSITION", font=font_medium, fill=COLOR_BLACK)
    bp_str = f"{boarding_position}"
    bp_w = d2mm(draw.textlength(bp_str, font=font_large))
    print(bp_w)
    draw.text(mm2d((117-bp_w/2, 42)), bp_str, font=font_large, stroke_width=2, fill=COLOR_BLACK)

    image.show()

    return image

    # l = zpl.Label(in2mm(BOARDING_PASS_HEIGHT_IN), in2mm(BOARDING_PASS_WIDTH_IN), dpmm=round(PRINTER_DPI/MM_PER_IN))
    # l.origin(0,0)
    # image_height = l.write_graphic(
    #     image,
    #     in2d(BOARDING_PASS_WIDTH_IN))
    # l.endorigin()
    
    # l.origin(18, 15)
    # l.write_text(f"{lastname.upper()}/{firstname.upper()}", char_height=BOARDING_PASS_FONT_SMALL_HEIGHT_MM, char_width=BOARDING_PASS_FONT_SMALL_HEIGHT_MM, line_width=100, justification='L')
    # l.endorigin()
    # print(l.dumpZPL())
    # l.preview()
    # return l

def print_boarding_pass(image, printer_ip="192.168.1.173"):
    image_rotated = image.rotate(90, expand=True)
    # image_rotated.show()
    zpl_string = ZebrafyImage(image_rotated, invert=True, pos_x=mm2d(10)).to_zpl()
    # print(zpl_string)
    # with ZPLPrinter(printer_ip) as zd621:
    #     zd621.send_zpl(zpl_string)

print_boarding_pass(generate_boarding_pass())

    

# starting_serial = 0
# num_serials = 10

# MEDIA_WIDTH_MM=82
# MEDIA_MARGIN_MM=1.0
# LABELS_PER_ROW=7
# ROW_HEIGHT_MM=10
# ROW_X_OFFSET_MM=-1
# ROW_Y_OFFSET_MM=1 # + is down
# COL_WIDTH_MM=(MEDIA_WIDTH_MM-2*MEDIA_MARGIN_MM)/LABELS_PER_ROW

# num_rows = math.ceil(num_serials / LABELS_PER_ROW)

# with ZPLPrinter("192.168.1.40") as zt610:
#     for row in range(num_rows):
#         l = zpl.Label(ROW_HEIGHT_MM, MEDIA_WIDTH_MM, dpmm=24) # height, width, 600dpi
#         num_cols = min(num_serials-row*LABELS_PER_ROW, LABELS_PER_ROW)
#         for col in range(num_cols):
#             serial = starting_serial + row*LABELS_PER_ROW + col
#             # "NNNNNNNNNR-YYYYMMDD-VVCCCC"
#             # NNNNNNNNN = Part Number
#             # R = Revision
#             # YYYYMMDD = Manufacturing Date
#             # VV = Vendor Code
#             # CCCC = Daily Sequential Counter

#             label_qr_str = f"{PART_NUMBER_STR+REVISION_STR}-{datetime.now().strftime('%Y%m%d')}-{VENDOR_CODE_STR}{serial:04}"

            
#             label_x_offset = ROW_X_OFFSET_MM+col*COL_WIDTH_MM+MEDIA_MARGIN_MM
#             l.origin(1.8+label_x_offset, 0.2+ROW_Y_OFFSET_MM, justification='0') # left justify
#             l.barcode('Q', label_qr_str, magnification=6)
#             l.endorigin()
#             l.origin(10.65+label_x_offset,8+ROW_Y_OFFSET_MM, justification='1') # right justify
#             l.write_text(label_qr_str, char_height=1.2, char_width=0.55, line_width=11, justification='C')
#             l.endorigin()
#         l.preview()



#         print(l.dumpZPL())
#         zt610.send_zpl(l.dumpZPL())

# # height += 20
# # l.origin(0, height)
# # l.write_text('Happy Troloween!', char_height=5, char_width=4, line_width=60,
# #              justification='C')
# # l.endorigin()

# # l.preview()
