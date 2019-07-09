from cam_util.cam_ctrl_util import PMDCam
from pmd_dust_test.distribution import normal_distribution as nd
from dependencies.display_util.string_display_util import print_notification, print_warning
from dependencies.archive_util.data_recording import TabDelimText

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import time
from collections import deque

matplotlib.use('Qt5agg')
np.set_printoptions(threshold=np.inf)

duration = 30
# roi = [103, 75, 160, 168]
roi = [68, 66, 163, 157]

file_headers = ['Trial', 'Elapsed Time', 'Average Depth', 'Standard Deviation']

if __name__ == "__main__":
    cam = PMDCam(roi)
    cam.connect()

    fig, ax = plt.subplots()
    ax.axis('off')

    plot = fig.add_axes([0.1, 0.5, 0.7, 0.4])
    dist = fig.add_axes([0.1, 0.1, 0.7, 0.4])

    data_recorder = TabDelimText(input('Name of the file to save data into? '))
    data_recorder.add_headers(file_headers)

    trial = 1

    try:
        while True:
            errored = False

            print_notification("Starting trial #{}".format(trial))
            cam.start_capture()

            avgs = deque()
            devs = deque()
            time_axis = deque()
            start = time.time()
            elapsed = 0
            while elapsed < duration:
                frames = cam.get_frame()
                if frames is not None:
                    rgb, depth = frames
                    elapsed = time.time() - start

                    avg, std_dev = nd(depth)

                    avgs.append(avg)
                    devs.append(std_dev)
                    time_axis.append(elapsed)

                    plot.clear()
                    plot.imshow(depth)
                    plot.axis('off')

                    dist.clear()
                    dist.plot(list(time_axis), list(avgs), label='Average Depth')
                    dist.plot(list(time_axis), list(devs), label='Standard Deviation')
                    dist.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))

                    plt.draw()
                    plt.pause(0.001)

                    data_recorder.add_data([trial, elapsed, avg, std_dev])
                else:
                    print_warning("The camera shut off unexpectedly...")
                    break

            if not errored:
                cam.stop_capture()
                input("Press any key to continue")
                trial += 1
            else:
                break

    finally:
        data_recorder.dispose()
