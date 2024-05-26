# SHADED RELIEF HEATMAP VISUALIZATION
# Creates an animation with a light source that moves over time

from subprocess import run
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap
from PIL import Image
import os
import sys
import visuals_utils as vis

ALGORITHM = sys.argv[1]
ALGO_ARGS = vis.getAlgoArgs(ALGORITHM)
START_SEED = int(sys.argv[2])
SEED_INCREMENT = vis.DEFAULT_SEED_INCREMENT #default 
fig, ax = plt.subplots()
# GET "n" to create nxn array
numRowsCols = vis.getIntFromInput("Number of rows/cols: ")
# Get color map - get_cmap is necessary because it's a string by default and can't be used as an object
colorMap = vis.getColorMap()
isLoop = vis.getBoolFromInput("GIF Looping? (Y/N): ")
#colorMap = get_cmap(colorMap)

# create shadedrelief subfolder if not exists
if not os.path.exists('heatmaps/shadedrelief'):
    os.makedirs('heatmaps/shadedrelief')

NUM_FRAMES = 72
framePaths = []
frames = []
debug = False

# GENERATE data 
array = vis.nRandomScalars(ALGORITHM, START_SEED, numRowsCols*numRowsCols, ALGO_ARGS)
array = np.array(array)

# creates a 2d array
world = array.reshape(numRowsCols, numRowsCols)

# function to update plot for each frame
# def update(frame):
for frameNum in range(NUM_FRAMES):
    if (not debug): print("Generating GIF... " + str(round(100 * (frameNum / NUM_FRAMES))) + "%")
    # clear current plot
    ax.clear()
    # increment by 5 degrees for each frame
    altdeg = frameNum * 5
    if altdeg > 360:
        altdeg = -360 # keep angle between 0 and 360
        # update light source with new altitude angle
    ls = LightSource(azdeg= 0 , altdeg=altdeg)
    # shade the world array with new light source
    rgb = ls.shade(world, plt.colormaps.get_cmap(colorMap))
    # plot shaded world array
    ax.imshow(rgb)
    # shows current angle as a title 
    ax.set_title(f'Altitude Angle: {altdeg} degrees')
    # 72 frames to fully rotate 360 degs
    heatmapPath = 'heatmaps/shadedrelief/' + str(ALGORITHM) + '_' + str(numRowsCols) + '_shadedrelief_HM_frame' + str(frameNum) + '.png'
    framePaths.append(heatmapPath)
    plt.savefig(heatmapPath)

     # clear progress for next update
    if (not debug): os.system('clear')

# ani = FuncAnimation(fig, update, frames = range(NUM_FRAMES) ,interval = 200)

# ls and rgb redefined out of the animation function
# for the sake of generating a static image
ls = LightSource(azdeg= 0 , altdeg = 0)
rgb = ls.shade(world, plt.colormaps.get_cmap(colorMap))
# does the animation
# plt.show() 
# gets the static image
# plt.imshow(rgb, cmap =colorMap )

# sets the heatmap path
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(numRowsCols) + '_shadedrelief_heatmap.svg'
plt.savefig(heatmapPath)

# STEP 5: Open .png frames to generate .gif from numIterations 
for png_path in framePaths:
    # convert to .png and open
    img = Image.open(png_path)
    frames.append(img)
# generate .gif
gifPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(numRowsCols) + '_shadedrelief_heatmap.gif'
frames[0].save(gifPath, save_all=True, append_images=frames[1:], loop=(not isLoop)) # duration=gifDuration

# clean up pngs
for file in os.listdir('heatmaps/shadedrelief'):
    if file.endswith('.png'):
        os.remove('heatmaps/shadedrelief/' + file)

# open .gif file [OS SPECIFIC COMMAND]
# cmd = 'open ' + gifPath
# run(cmd, shell=True)
vis.openVisual(gifPath)

