from bottle import Bottle, get, post, request
from PIL import Image
from io import BytesIO
import base64
import json

app = Bottle()

class ImageUtils:

    @staticmethod
    def convertJPG(im):
        with BytesIO() as f:
           im = im.convert("RGB")
           im.save(f, format='JPEG')
           return base64.encodebytes(f.getvalue())

    @staticmethod
    def convertPNG(im):
        with BytesIO() as f:
           im.save(f, format='PNG')
           return base64.encodebytes(f.getvalue())

@app.route("/imgcnv", methods=["POST"])
def convert_image():
    if request.json['image'] and request.json['to']:
        format = request.json['to']
        img = Image.open(BytesIO(base64.b64decode(request.json['image'])))
        try:
           return getattr(ImageUtils, "convert" + format.upper())(img)
        except AttributeError as e:
           return "Unsupported format: " + format , 400
        except Exception as e:
           print("Server crash" + str(e))
           return "Server crash please report this error.", 400
    else:
        return "No image found", 400
   
@app.route("/imgd", methods=["POST"])
def image_detail():
    if request.json['image']:
        try:
            img = Image.open(BytesIO(base64.b64decode(request.json['image'])))
            return json.dumps({'msg': 'success', 'size': [img.width, img.height], 'mode': img.mode, 'format': img.format}) 
        except Exception as e:
            print("Server crash" + str(e))
            return "Server crash please report this error.", 400
    else:
        return "No image found", 400