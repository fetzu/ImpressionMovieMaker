### [   ImpressionMovieMaker v0.0.1-alpha || Made 'fo shits 'n giggles by bonj   ] ###

## [ CLI is cooler with docopt ]
"""
Usage: ImpressionMovieMaker.py [-vzsdh] [RUSHESFOLDER] [LOGODEBUT] [LOGOFIN] [MUSIQUE] [OUTPATH]

Arguments:
  RUSHESFOLDER      Dossier contenant les rushes.
  LOGODEBUT         Logo de début (troupe).
  LOGOFIN           Logo de fin (AAR).
  MUSIQUE           Musique pour l'impression.
  OUTPATH           Chemin vers le fichier de sortie.

Options:
  -h --help
  -s                Pour les hipster: ordre des séquences aléatoire.
  -v                Mode verbose (montre les étapes de travail en détail, en anglais dans le texte).
  -z                Mode "zen"/silencieux (rien dans la console).
  -d                DEV: Montre les arguments passés au programme. 
"""


## [ IMPORTS be imports ]
import os
import random
from moviepy.editor import *
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfile, asksaveasfile
from docopt import docopt

# Needed to intitialize docopt (for CLI)
if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['-d'] is True: print(arguments)


## [ CONSTANTS are the new vars ]
VERSION = "0.0.2-alpha"

# Uh-oh, we might need FFMPEG for dist/packaging with pyinstaller
#os.environ["IMAGEIO_FFMPEG_EXE"] = "C:\\ffmpeg.exe"

# Check if arguments were passed through the CLI. If they were: set the constants, if they weren't: promp the user !
# The names are pretty self explanatory (if they aren't read the docs!)
if arguments['RUSHESFOLDER'] is None: RUSHESFOLDER = askdirectory(title='Choisir dossier des rushes')
else: RUSHESFOLDER = arguments['RUSHESFOLDER']

if arguments['LOGODEBUT'] is None: LOGODEBUT = askopenfile(title="Choisir logo d'intro (de troupe)")
else: LOGODEBUT = arguments['LOGODEBUT']

if arguments['LOGOFIN'] is None: LOGOFIN = askopenfile(title="Choisir logo de fin (AAR)")
else: LOGOFIN = arguments['LOGOFIN']

if arguments['MUSIQUE'] is None: MUSIQUE = askopenfile(title="Choisir une musique")
else: MUSIQUE = arguments['MUSIQUE']

if arguments['OUTPATH'] is None: OUTPATH = asksaveasfile(title="Choisir ou sauvegarder le résultat")
else: OUTPATH = arguments['OUTPATH']


## [ Main App logic ] ##
# I'm leaving my mark, just because I can
if arguments['-z'] is False: print("'Yeah, but your scientists were so preoccupied with whether or not they could, they didn't stop to think if they should.' -Dr. Ian Malcolm, Jurassic Park")
if arguments['-z'] is False: print("ImpressionMovieMaker version {} by Julien 'bonj' Bono.".format(VERSION))

# List all the videos inside the FOLDER (and its subfolders) and push the paths into the clips array
clips = [os.path.join(r,file) for r,d,f in os.walk(RUSHESFOLDER) for file in f]
if arguments['-z'] is False: print("Number of rushes provided: {}".format(len(clips)))

# From clips, select a random number of files to remove from list. Make sure that the total number of rushes does not exceed 40.
clipCutter = random.randint(int(len(clips)/4), int(len(clips)/2))
while (len(clips)-clipCutter) > 40:
    clipCutter = random.randint(clipCutter, clipCutter*2)
if arguments['-z'] is False: print("ClipCutter(tm) will chop down {} rushes !".format(clipCutter))
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

    if arguments['-v'] is True: print("Working on clip #{} with a length of {}".format(i, max))

    # Check that the clip is not too short (ie shorter than 6 seconds), else remove said clip and break
    if max < 6 or max > 60:
        if arguments['-v'] is True: print("Clip #{} too short/long, skipping.".format(i))

    # Cut select a random part of the clip; do this until clip is less than 5 seconds
    else:
        while max > 5:
            cb = int(random.randint(2, int(max/2)))
            ce = -2 #int(random.randint(-2, int(-(max/2)))) #TODO: Replace with random value between -2 and -x !
            if arguments['-v'] is True: print("Clip #{}: duration {}s | Cut from {}s to {}s".format(i, max, cb, ce))
            rushQueue[i] = rushQueue[i].subclip(cb, ce)
            max = int(rushQueue[i].duration) 
            if arguments['-v'] is True: print("Clip #{} done with a new duration of {}s".format(i, max))
        # Append the result to rushList
        rushList.append(rushQueue[i])
        if arguments['-v'] is True: print("Clip #{} appended !".format(i))

# Randomize the clips order (uncomment to make things more fun)
if arguments['-v'] & arguments['-s'] is True: print("Randomizing clip order.")
if arguments['-s'] is True: random.shuffle(rushList)

# Concatenate all the clips inside the rushList into impression array (will make it easier to change the soudtrack)
impression = concatenate_videoclips(rushList)

# Let's take care of that soundtrack !
# Reduce the overall volume to 0.3x
impression = impression.volumex(0.3)
# Load the selected music into an AudioFileClip, and set its duration to the impression's duration
music = AudioFileClip(MUSIQUE)
music = music.set_duration(impression.duration)
# Set the combination of both into soundTrack, and set soundTrack as the impression's soundtrack
soundTrack = CompositeAudioClip([impression.audio, music])
impression.audio = soundTrack

# Now that we have all our clips, let's put the final piece together by adding the intro logo, the title card and the outro logo
if arguments['-v'] is True: print("Putting it all together...")
videoTimeLine = []
videoTimeLine.append(VideoFileClip(LOGODEBUT))
#videoTimeLine.append | TODO: Add title card here !
videoTimeLine.append(impression)
videoTimeLine.append(VideoFileClip(LOGOFIN))


# Concatenate all the clips inside the IMPRESSION array
#print(rushList)
impression = concatenate_videoclips(videoTimeLine)

# Let's render that shit !
if arguments['-v'] is True: print("Starting final rendering...")
impression.to_videofile(OUTPATH)
if arguments['-v'] is True: print("Done ! See the results at {}".format(OUTPATH))