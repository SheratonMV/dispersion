import cv2
import numpy as np

manualcolors = np.loadtxt("colors.dat", unpack=True, delimiter=',').transpose().astype(np.uint8)
rows = 12
cols = int(len(manualcolors) / rows)
scale = 2
rowsize = 140
colsize = 60
offset = 30
textoffset = offset + 20
if len(manualcolors) % rows != 0:
    cols += 1

main_array = np.zeros((cols * colsize, rows * rowsize, 3)).astype(np.uint8)
main_array[:] = 255
start_row = 0
start_col = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
thickness = 1
for color in manualcolors:
    if np.sum(color) != 0:
        c = (int(color[0]), int(color[1]), int(color[2]))
        print(color, start_row * rowsize, start_col * colsize, start_row * rowsize + rowsize, start_col * colsize + colsize)
        cv2.rectangle(main_array, (start_row * rowsize, start_col * colsize), (start_row * rowsize + rowsize, start_col * colsize + colsize - offset), c,
                      thickness=-1)
        image = cv2.putText(main_array, str(c), (start_row * rowsize + int(rowsize/7), start_col * colsize + textoffset), font, fontScale, (0,0,0), thickness, cv2.LINE_AA)

        start_row += 1
        if start_row == rows:
            start_row = 0
            start_col += 1
main_array = cv2.cvtColor(main_array, cv2.COLOR_BGR2RGB)
cv2.imshow("outputs/colorpallete.tif", main_array)
cv2.waitKey(0)
print(len(manualcolors))
