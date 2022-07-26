import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

def convert_to_pixels(infile_name, stitch_width, stitch_height, proj_width, colors, in_folder, out_folder):
    pic = imageio.imread(f"static/{in_folder}/{infile_name}")
    pic_fit = np.reshape(pic, (-1, pic.shape[-1]))
    kmeans = KMeans(n_clusters=colors, random_state=0).fit(pic_fit)
    centers = np.rint(kmeans.cluster_centers_).astype('uint8')
    new_pic = np.asarray([centers[i] for i in kmeans.labels_])
    new_pic = np.reshape(new_pic, pic.shape)
    block_width = round(pic.shape[1] / (proj_width / stitch_width))
    block_height = round(pic.shape[0] / (proj_width * pic.shape[1] / pic.shape[0] / stitch_height))
    for row in range(0, new_pic.shape[0], block_height):
        for col in range(0, new_pic.shape[1], block_width):
            slice = new_pic[row:row + block_height, col:col + block_width, :]
            old_shape = slice.shape
            slice = np.reshape(slice, (-1, slice.shape[-1]))
            c = Counter(map(tuple, slice))
            new_slice = np.full(old_shape, np.asarray(c.most_common()[0][0]))
            new_pic[row:row + block_height, col:col + block_width, :] = new_slice
    fname = infile_name[:infile_name.index('.')]
    out_fname = f'{fname}_out.png'
    plt.imsave(f'static/{out_folder}/{out_fname}', new_pic)
    return new_pic[::block_height, ::block_width, :], out_fname

def convert_to_instructions(out_arr):
    instructions = ""
    color_map = {}
    color_count = 0
    for row in range(out_arr.shape[0]):
        instructions += f'Row {row}:\t'
        tracking_color = None
        count = 0
        for col in range(out_arr.shape[1]):
            curr_color = tuple(out_arr[row, col, :])

            if curr_color not in color_map:
                color_map[curr_color] = chr(ord('A') + color_count)
                color_count += 1

            if tracking_color is None:
                tracking_color = curr_color
                count = 1
            elif col == out_arr.shape[1] - 1:
                instructions += f'{count + 1} st {color_map[tracking_color]}<br>'
            elif curr_color != tracking_color:
                instructions += f'{count} st {color_map[tracking_color]}, '
                tracking_color = curr_color
                count = 1
            else:
                count += 1

    instructions += "<br>"
    instructions += '<br>'.join([f"Color {name}: {color}" for color, name in color_map.items()])
    return instructions