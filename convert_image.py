import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

NUM_STITCHES_WIDE = 50
NUM_COLORS = 4
INFILE_NAME = 'ariel.png'
fname = INFILE_NAME[:INFILE_NAME.index('.')]

pic = imageio.imread(INFILE_NAME)
box_size = pic.shape[1] // NUM_STITCHES_WIDE
pic_fit = np.reshape(pic, (-1, pic.shape[-1]))
kmeans = KMeans(n_clusters=NUM_COLORS, random_state=0).fit(pic_fit)
centers = np.rint(kmeans.cluster_centers_).astype('uint8')

new_pic = np.asarray([centers[i] for i in kmeans.labels_])
new_pic = np.reshape(new_pic, pic.shape)
block_pic = []
for row in range(0, new_pic.shape[0], box_size):
    block_pic.append([])
    for col in range(0, new_pic.shape[1], box_size):
        block_pic[-1].append([])
        for color in range(new_pic.shape[2]):
            slice = new_pic[row:row + box_size, col:col + box_size, color]
            c = Counter(slice.flatten())
            block_pic[-1][-1].append(c.most_common()[0][0])
block_pic = np.asarray(block_pic)
diff = (block_pic.shape[1] - NUM_STITCHES_WIDE) // 2
block_pic = block_pic[:, diff:NUM_STITCHES_WIDE + diff, :]
plt.imsave(f'{fname}_out.png', block_pic)

f = open(f'{fname}_instructions.txt', 'w')
labels = np.reshape(kmeans.labels_, pic.shape[:-1])
color_map = {}
color_count = 0
for row in range(block_pic.shape[0]):
    f.write(f'Row {row}:\t')
    tracking_color = None
    count = 0
    for col in range(block_pic.shape[1]):
        curr_color = tuple(block_pic[row, col, :])

        if curr_color not in color_map:
            color_map[curr_color] = chr(ord('A') + color_count)
            color_count += 1

        if tracking_color is None:
            tracking_color = curr_color
            count = 1
        elif col == block_pic.shape[1] - 1:
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