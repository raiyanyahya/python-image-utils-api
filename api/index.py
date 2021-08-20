from bottle import Bottle, request, response, BaseRequest
from PIL import Image
from io import BytesIO
import base64
import json
import os

app = Bottle()
BaseRequest.MEMFILE_MAX = 1024 * 1024 * 10

class ImageUtils:

    @staticmethod
    def convertJPG(im):
        with BytesIO() as f:
           im = im.convert("RGB")
           im.save(f, format='JPEG')
           return base64.encodebytes(f.getvalue()).decode("utf-8")

    @staticmethod
    def convertPNG(im):
        with BytesIO() as f:
           im.save(f, format='PNG')
           return base64.encodebytes(f.getvalue()).decode("utf-8")

def return_response(msg, code):
    response.status = code
    return json.dumps(str({"message": msg}))

def require_header(fn):
    def check_key(**kwargs):   
        header_value = request.headers.get("x-rapidapi-key")

        if header_value ==  os.getenv('KEY'):
            return fn(**kwargs)
        else:
            return return_response("Please authorize",403)

    return check_key

@app.get('/')
def ping():
    return {}

@app.post("/imgcnv")
@require_header
def convert_image():
    if request.json['image'] and request.json['to']:
        iformat = request.json['to'].upper()
        if iformat not in ["JPG","PNG"]:
            return return_response("Unsupported format: " + iformat, 400)
        try:
            img = Image.open(BytesIO(base64.b64decode(request.json['image'])))
            response.status = 200
            return json.dumps(str({"image": getattr(ImageUtils, "convert" + iformat)(img)}))
        except Exception as e:
           print("Server crash " + str(e))
           return  return_response("Server crash please report this error", 400)
    else:
        return return_response("No image found",400)
   
@app.post("/imgd")
@require_header
def image_detail():
    
    if request.json['image']:
        try:
            print("here")
            img = Image.open(BytesIO(base64.b64decode(request.json['image'])))
            response.status = 200
            
            return json.dumps(str({'msg': 'success', 'size': [img.width, img.height], 'mode': img.mode, 'format': img.format}) )
        except Exception as e:
            print("Server crash" + str(e))
            return return_response("Server crash please report this error",400)
    else:
        return return_response("[image] key missing",400)