from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from static.convert_image import convert_to_pixels, convert_to_instructions

app = Flask(__name__)
IN_FOLDER = "imgs"
OUT_FOLDER = "imgs_out"

@app.route('/')
def home():
    return redirect(url_for('upload'))

@app.route('/upload')
def upload():
    return render_template('upload.html')
	
@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        if request.form.get('file_name'):
            in_fname = request.form.get('file_name')
        else:
            f = request.files['file']
            in_fname = secure_filename(f.filename)
            f.save(f"static/{IN_FOLDER}/{in_fname}")
        stitch_width = float(request.form.get('stitch_width'))
        stitch_height = float(request.form.get('stitch_height'))
        proj_width = float(request.form.get('proj_width'))
        num_colors = int(request.form.get('num_colors'))
        out_arr, out_fname = convert_to_pixels(in_fname, stitch_width, stitch_height, proj_width, num_colors, IN_FOLDER, OUT_FOLDER)
        instructions = convert_to_instructions(out_arr)
        return render_template('converted.html',
                                in_fname=f"{IN_FOLDER}/{in_fname}",
                                out_fname=f"{OUT_FOLDER}/{out_fname}",
                                instructions=instructions,
                                fname=in_fname,
                                stitch_width=stitch_width,
                                stitch_height=stitch_height,
                                proj_width=proj_width,
                                num_colors=num_colors)
    else:
        return redirect(url_for('upload'))

if __name__ == "__main__":
    app.run()