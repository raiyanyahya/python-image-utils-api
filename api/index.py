from bottle import Bottle, request, response
from PIL import Image
from io import BytesIO
import base64
import json

app = Bottle()
response.content_type = 'application/json'
# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

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
    return json.dumps({"message": msg})

@app.route("/imgcnv", methods=["POST","GET"])
@enable_cors
def convert_image():
    if request.json['image'] and request.json['to']:
        iformat = request.json['to'].upper()
        if iformat not in ["JPG","PNG"]:
            return return_response("Unsupported format: " + iformat, 400)
        try:
            img = Image.open(BytesIO(base64.b64decode(request.json['image'])))
            response.status = 200
            return json.dumps({"image": getattr(ImageUtils, "convert" + iformat)(img)})
        except Exception as e:
           print("Server crash " + str(e))
           return  return_response("Server crash please report this error", 400)
    else:
        response.status = 400
        return json.dumps({"message": "No image found"})
   
@app.route("/imgd", methods=["POST","GET"])
def image_detail():
    if request.json['image']:
        try:
            img = Image.open(BytesIO(base64.b64decode(request.json['image'])))
            response.status = 200
            return json.dumps({'msg': 'success', 'size': [img.width, img.height], 'mode': img.mode, 'format': img.format}) 
        except Exception as e:
            print("Server crash" + str(e))
            return return_response("Server crash please report this error",400)
    else:
        return return_response("[image] key missing",400)