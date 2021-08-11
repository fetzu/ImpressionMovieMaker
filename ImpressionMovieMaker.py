### [   ImpressionMovieMaker v0.0.1-alpha || Made 'fo shits 'n giggles by bonj   ] ###
## [ IMPORTS be imports ]
import os
import random
from moviepy.editor import *
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfile, asksaveasfile


## [ CONSTANTS are the new vars ]
# Declare some constants | TODO/TOMODIFY: Comment/uncomment to make rushes folder user-selectable
#FOLDER = "C:\\Users\\bonj\\Desktop\\IMPRESSION\\20210728"
FOLDER = askdirectory(title='Choisir dossier des rushes') # Shows selection dialog for rushes folder
#LOGODEBUT = "C:\\Users\\bonj\\Desktop\IMPRESSION\\LOGOIN.mp4"
LOGODEBUT = askopenfile(title="Choisir logo d'intro (de troupe)") # Shows selection dialog for logo animation (intro)
#LOGOFIN = "C:\\Users\\bonj\\Desktop\IMPRESSION\\LOGOOUT.mp4"
LOGOFIN = askopenfile(title="Choisir logo de fin (AAR)") # Shows selection dialog for logo AAR (end)
#MUSIQUE = "C:\\Users\\bonj\\Desktop\IMPRESSION\\ZIK.mp3"
MUSIQUE = askopenfile(title="Choisir une musique") # Shows selection dialog for logo AAR (end)
#OUTPATH = "C:\\Users\\bonj\\Desktop\IMPRESSION\\OUT.mp4"
OUTPATH = asksaveasfile(title="Choisir ou sauvegarder l'impression")


## [ Main App logic ] ##
# List all the videos inside the FOLDER (and its subfolders) and push the paths into the clips array
clips = [os.path.join(r,file) for r,d,f in os.walk(FOLDER) for file in f]
print("Number of rushes provided: {}".format(len(clips)))

# From clips, select a random number of files to remove from list. Make sure that the total number of rushes does not exceed 40.
clipCutter = random.randint(int(len(clips)/4), int(len(clips)/2))
while (len(clips)-clipCutter) > 40:
    clipCutter = random.randint(clipCutter, clipCutter*2)
print("ClipCutter(tm) will chop down {} rushes !".format(clipCutter))
for i in range(int(clipCutter)):
    clips.pop(random.randint(0, len(clips)-1))

# Create a rushQueue array and populate it will all the clips from the clips array as VideoFileClip, selecting a random part of each clip to keep
rushQueue = []
for clip in clips:
    rushQueue.append(VideoFileClip(clip))

# Set rushList as the final list of clips to be kept and the index j to 0
rushList = []

# From rushQueue, keep a random part of each clip
for i in range(len(rushQueue)):
    # Set the "max" var as an intenger of the clip's duration
    max = int(rushQueue[i].duration)

    print("Working on clip #{} with a length of {}".format(i, max))

    # Check that the clip is not too short (ie shorter than 6 seconds), else remove said clip and break
    if max < 6 or max > 60:
        print("Clip #{} too short/long, skipping.".format(i))

    # Cut select a random part of the clip; do this until clip is less than 5 seconds
    else:
        while max > 5:
            cb = int(random.randint(2, int(max/2)))
            ce = -2 #int(random.randint(-2, int(-(max/2)))) #TODO: Replace with random value between -2 and -x !
            print("Clip #{}: duration {}s | Cut from {}s to {}s".format(i, max, cb, ce))
            rushQueue[i] = rushQueue[i].subclip(cb, ce)
            max = int(rushQueue[i].duration) 
            print("Clip #{} done with a new duration of {}s".format(i, max))
        # Append the result to rushList
        rushList.append(rushQueue[i])
        print("Clip #{} appended !".format(i))

# Randomize the clips order (uncomment to make things more fun)
#random.shuffle(rushList)

# Concatenate all the clips inside the rushList into impression array (will make it easier to change the soudtrack)
impression = concatenate_videoclips(rushList)

# TODO: handle the music here
# Reduce the overall volume to 0.3x
impression = impression.volumex(0.3)
# Load the selected music into an AudioFileClip, and set its duration to the impression's duration
music = AudioFileClip(MUSIQUE)
music = music.set_duration(impression.duration)
# Set the combination of both into soundTrack, and set soundTrack as the impression's soundtrack
soundTrack = CompositeAudioClip([impression.audio, music])
impression.audio = soundTrack

# Now that we have all our clips, let's put the final piece together by adding the intro logo, the title card and the outro logo
videoTimeLine = []
videoTimeLine.append(VideoFileClip(LOGODEBUT))
#videoTimeLine.append | TODO: Add title card here !
videoTimeLine.append(impression)
videoTimeLine.append(VideoFileClip(LOGOFIN))


# Concatenate all the clips inside the IMPRESSION array
#print(rushList)
impression = concatenate_videoclips(videoTimeLine)

# Let's render that shit !
impression.to_videofile(OUTPATH)