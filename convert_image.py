import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

def convert_to_pixels(infile_name, num_stitches_wide, num_colors, in_folder, out_folder):
    pic = imageio.imread(f"static/{in_folder}/{infile_name}")
    box_size = pic.shape[1] // num_stitches_wide
    pic_fit = np.reshape(pic, (-1, pic.shape[-1]))
    kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(pic_fit)
    centers = np.rint(kmeans.cluster_centers_).astype('uint8')

    new_pic = np.asarray([centers[i] for i in kmeans.labels_])
    new_pic = np.reshape(new_pic, pic.shape)
    out_arr = []
    for row in range(0, new_pic.shape[0], box_size):
        out_arr.append([])
        for col in range(0, new_pic.shape[1], box_size):
            out_arr[-1].append([])
            for color in range(new_pic.shape[2]):
                slice = new_pic[row:row + box_size, col:col + box_size, color]
                c = Counter(slice.flatten())
                out_arr[-1][-1].append(c.most_common()[0][0])
    out_arr = np.asarray(out_arr)
    diff = (out_arr.shape[1] - num_stitches_wide) // 2
    out_arr = out_arr[:, diff:num_stitches_wide + diff, :]
    pic_arr = []
    for row in out_arr:
        pic_arr.append([])
        for i in row:
            pic_arr[-1].extend([i] * box_size)
        pic_arr.extend([pic_arr[-1]] * (box_size - 1))
    pic_arr = np.asarray(pic_arr)
    fname = infile_name[:infile_name.index('.')]
    out_fname = f'{fname}_out.png'
    plt.imsave(f'static/{out_folder}/{out_fname}', pic_arr)
    return out_arr, out_fname

def convert_to_instructions(infile_name, num_stitches_wide, num_colors, out_folder):
    # DEAL WITH LATER
    f = open(f'static/instructions_out/{fname}_instructions.txt', 'w')
    color_map = {}
    color_count = 0
    for row in range(out_arr.shape[0]):
        f.write(f'Row {row}:\t')
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
                f.write(f'{count + 1} st {color_map[tracking_color]}\n')
            elif curr_color != tracking_color:
                f.write(f'{count} st {color_map[tracking_color]}, ')
                tracking_color = curr_color
                count = 1
            else:
                count += 1

    f.write('\n')
    f.writelines([f"{name}: {color}\n" for color, name in color_map.items()])
    f.close()