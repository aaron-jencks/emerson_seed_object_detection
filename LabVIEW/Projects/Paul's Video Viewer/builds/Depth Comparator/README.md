##Installation
If you don't already have a `.bag` file convertor, then you need to go into `./python_code` and follow the installation
instructions

#####Codec

You need to install the XVID codec, if you don't have it already, LabVIEW doesn't have access to it by default, you can 
find it [here](https://www.xvid.com/download/)

##Execution
Run the `depth_comparator.exe` file

###Controls
You need to select two different `.avi` files to compare, select `start` to begin playback.
You can use the `FPS` slider to control playback speed, `Averaging Type` determines whether to use normal average, or
RMS, `Depth Value Boundaries` determines the cutoff values for the depth values.
`Playback Boundaries` specifies the start and stop positions of the video, the program will automatically loop both
videos at the same time, using the shortest one as the control.

`Depth Scale` allows you to enter the depth scale used for each camera, on a per video basis.

###Indicators
There are several indicators on each video, they tell you the roughness factor of the terrain, the average depth, and
the current frame number.

If you select a `ROI` using the controls on the image display, then these indicators will adjust accordingly.