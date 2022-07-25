from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from convert_image import convert_to_pixels

app = Flask(__name__)
IN_FOLDER = "imgs"
OUT_FOLDER = "imgs_out"

@app.route('/upload')
def upload():
    return render_template('upload.html')
	
@app.route('/convert', methods = ['POST'])
def convert():
    if request.method == 'POST':
        f = request.files['file']
        num_stitches = int(request.form.get('num_stitches'))
        num_colors = int(request.form.get('num_colors'))
        in_fname = secure_filename(f.filename)
        f.save(f"static/{IN_FOLDER}/{in_fname}")
        out_arr, out_fname = convert_to_pixels(in_fname, num_stitches, num_colors, IN_FOLDER, OUT_FOLDER)
        in_fname = f"{IN_FOLDER}/{in_fname}"
        out_fname = f"{OUT_FOLDER}/{out_fname}"
        return render_template('converted.html', in_fname=in_fname, out_fname=out_fname)

if __name__ == "__main__":
    app.run()