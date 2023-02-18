<<<<<<< HEAD
import os
import shutil
import numpy as np
import cv2
import glob
import time as t

from flask import Flask, render_template, request
from systems.image_search_system import ImageSearch_System as ISS

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    removing_files = glob.glob('static/*.jpg')
    for i in removing_files:
        # try:
        #     int(i[-5])
        #     os.remove(i)
        # except:
        #     continue
        os.remove(i)
    return render_template("upload.html")



@app.route("/result", methods=["GET", "POST"])
def return_res():
    dst_dir = "static/"
    p = []

    file = request.files.get("uploaded_img")

    K = request.form.get("K")
    K = int(K) if K != "" else 3

    method = request.form.get("methods")
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))
    width = int(request.form.get("img_width"))
    height = int(request.form.get("img_height"))

    file.save(os.path.join(
        app.config['UPLOAD_FOLDER'],
        "query.jpg"
    ))

    dataset_name = 'oxbuild'
    
    img_query = cv2.imread("query.jpg")[y:y+height, x:x+width]

    cv2.imwrite("query.jpg", img_query)
    shutil.copy("query.jpg", dst_dir + "query.jpg")

    IS = ISS(dataset_name, method)
    IS.indexing()

    res, time = IS.retrieve_image("query.jpg", K)

    paths = list(np.array(res)[:, 0])
    paths = [str(p) for p in paths]

    for i, jpgfile in enumerate(paths):
        shutil.copy(jpgfile, dst_dir + str(i) + ".jpg")
        p.append(dst_dir + str(i) + ".jpg")

    return render_template("result_beautified.html", TIME=round(time, 2), PATHS=p, METHOD=method, QUERY=dst_dir + "query.jpg")
=======
import os
import shutil
import numpy as np
import cv2
import glob
import time as t

from flask import Flask, render_template, request
from systems.image_search_system import ImageSearch_System as ISS

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    removing_files = glob.glob('static/*.jpg')
    for i in removing_files:
        try:
            int(i[-5])
            os.remove(i)
        except:
            continue
    return render_template("upload.html")


@app.route("/result", methods=["GET", "POST"])
def return_res():
    dst_dir = "static/"
    p = []

    file = request.files.get("uploaded_img")

    K = request.form.get("K")
    K = int(K) if K != "" else 3

    method = request.form.get("method")
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))
    width = int(request.form.get("img_width"))
    height = int(request.form.get("img_height"))

    file.save(os.path.join(
        app.config['UPLOAD_FOLDER'],
        "query.jpg"
    ))

    dataset_name = 'oxbuild'
    
    img_query = cv2.imread("query.jpg")[y:y+height, x:x+width]

    cv2.imwrite("query.jpg", img_query)
    shutil.copy("query.jpg", dst_dir + "query.jpg")

    IS = ISS(dataset_name, method)
    IS.indexing()

    res, time = IS.retrieve_image("query.jpg", K)

    paths = list(np.array(res)[:, 0])
    paths = [str(p) for p in paths]

    for i, jpgfile in enumerate(paths):
        shutil.copy(jpgfile, dst_dir + str(i) + ".jpg")
        p.append(dst_dir + str(i) + ".jpg")

    return render_template("result.html", TIME=round(time, 2), PATHS=p, METHOD=method, QUERY=dst_dir + "query.jpg")
>>>>>>> 980a0eea797939db785415859ede40acbc451f7c
