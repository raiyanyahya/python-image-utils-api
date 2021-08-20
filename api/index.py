from bottle import Bottle, request, response, post , BaseRequest
BaseRequest.MEMFILE_MAX = 1024 * 1024 * 10


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
           return base64.encodebytes(f.getvalue()).decode("utf-8")

    @staticmethod
    def convertPNG(im):
        with BytesIO() as f:
           im.save(f, format='PNG')
           return base64.encodebytes(f.getvalue()).decode("utf-8")

def return_response(msg, code):
    response.status = code
    return json.dumps(str({"message": msg}))


@app.post('/')
def ping():
    return {}

@app.post("/imgcnv")
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