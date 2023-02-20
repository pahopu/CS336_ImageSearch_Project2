
import os
import numpy as np
import cv2
import glob


from flask import Flask, render_template, request
from systems.image_search_system import ImageSearch_System as ISS

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    removing_files = glob.glob('static/query/*.jpg')
    for i in removing_files:
        os.remove(i)
    return render_template("upload.html", ALERT=0)


@app.route("/result", methods=["GET", "POST"])
def return_res():
    dst_dir = "static/query/"

    file = request.files.get("real_uploaded_img")

    K = request.form.get("K")
    K = int(K) if K != "" else 3

    dataset_name = request.form.get("dataset")
    x = request.form.get("x")
    if x == "":
        return render_template("upload.html", ALERT=1)
    x = int(x)
    y = int(request.form.get("y"))
    width = int(request.form.get("img_width"))
    height = int(request.form.get("img_height"))

    file.save(os.path.join(
        app.config['UPLOAD_FOLDER'],
        "query.jpg"
    ))

    method = "Xception"

    img_query = cv2.imread("query.jpg")[y:y+height, x:x+width]

    cv2.imwrite(dst_dir + "query.jpg", img_query)

    os.remove("query.jpg")

    IS = ISS(dataset_name, method)
    IS.indexing()

    res, time = IS.retrieve_image("static/query/query.jpg", K)

    paths = list(np.array(res)[:, 0])
    paths = [str(p) for p in paths]

    print(paths)

    return render_template("result_beautified.html", TIME=round(time, 2), PATHS=paths, METHOD=method,
                           QUERY=dst_dir + "query.jpg")