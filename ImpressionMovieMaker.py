### [   ImpressionMovieMaker || Made 'fo shits 'n giggles by Julien 'bonj' Bono   ] ###

## [ CLI is cooler with docopt ]
"""
Usage: ImpressionMovieMaker.py [-hvzpboxdrsmf] [--speed <seconds>] [RUSHESFOLDER] [LOGODEBUT] [LOGOFIN] [MUSIQUE] [OUTFILE] [COMPAGNIE] [EXERCICE]

  Arguments:
    RUSHESFOLDER      Path to folder containing the rushes.
    LOGODEBUT         Starting logo.
    LOGOFIN           Ending logo.
    MUSIQUE           Path to the impression's song track/music.
    OUTFILE           Path for the output file.
    COMPAGNIE         Name of the company.
    EXERCICE          Name of the exercice.

  Options:
    -h --help
    -v                Verbose mode.
    -z                Zen/silent mode (almost nothing is logged to the terminal).
    -p                DEV: Shows the arguments passed to the program and details of clipTrimmer™.
    -b                BeatMode: cuts to the beat of the song [default mode].
    -o                OnsetMode: cuts to the onsets of the song.
    -x                HybridMode: uses both beat tracking and onset detection.
    -d                Drone mode: rushes longer than 1 minute are used. Warning: memory consuming and possibly unstable.
    -r                For hipsters: randomises the sequencing of the rushes.
    -s --slow         Slow cut speeds (each clip will last at least somewhere between 3 and 5 seconds).
    -m --medium       Medium cut speeds (each clip will last at least somewhere between 1.75 and 3.25 seconds) [default mode].
    -f --fast         Fast cut speeds (each clip will last at least somewhere between 1 and 2 seconds).
    --speed <sec>     Specify the minimum duration of a cut in seconds (overrides pre-set cut speeds).
"""


## [ IMPORTS be imports ]
import os
import random
import datetime
import warnings
import librosa
from moviepy.editor import *
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from docopt import docopt
from colorama import init, Fore, Style


## [ Some INIT settings ]
# Gets read of those pesky Pysoundfile/audioread librosa warnings.
warnings.filterwarnings("ignore")

# Sets colorama to reset Fore/Style after each print
init(autoreset=True)

# "The time for us is now"
now = datetime.datetime.now()

# Needed to intitialize docopt (for CLI)
if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['-p'] is True: print(arguments)


## [ CONSTANTS are the new vars ]
VERSION = "1.0.2"

# Uh-oh, we might need the paths to FFMPEG and Imagemagick in some envs
#IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'C:\\convert.exe')
#os.environ['IMAGEIO_FFMPEG_EX'] = "C:\\ffmpeg.exe"

# Check if arguments were passed through the CLI. If they were: set the constants, if they weren't: promp the user !
# The names are pretty self explanatory (if they aren't read the docs!)
if arguments['RUSHESFOLDER'] is None: RUSHESFOLDER = askdirectory(title='Choisir dossier des rushes')
else: RUSHESFOLDER = arguments['RUSHESFOLDER']

if arguments['LOGODEBUT'] is None: LOGODEBUT = askopenfilename(title="Choisir logo d'intro (de troupe)")
else: LOGODEBUT = arguments['LOGODEBUT']

if arguments['LOGOFIN'] is None: LOGOFIN = askopenfilename(title="Choisir logo de fin (AAR)")
else: LOGOFIN = arguments['LOGOFIN']

if arguments['MUSIQUE'] is None: MUSIQUE = askopenfilename(title="Choisir une musique")
else: MUSIQUE = arguments['MUSIQUE']

if arguments['OUTFILE'] is None: OUTFILE = asksaveasfilename(title="Choisir ou sauvegarder le résultat")
else: OUTFILE = arguments['OUTFILE']

if arguments['COMPAGNIE'] is None: COMPAGNIE = input("Compagnie? ")
else: COMPAGNIE = arguments['COMPAGNIE']

if arguments['EXERCICE'] is None: EXERCICE = input("Nom de l'exercice? ")
else: EXERCICE = arguments['EXERCICE']

if arguments['--slow'] is True: CUTSPEED = random.uniform(3, 5)
elif arguments['--medium'] is True: CUTSPEED = random.uniform(1.75, 3.25)
elif arguments['--fast'] is True: CUTSPEED = random.uniform(1, 2)
else: CUTSPEED = random.uniform(1.75, 3.25)

if arguments['--speed'] is not None: 
    if arguments['--speed'].isdigit():
        CUTSPEED = arguments['--speed']
        print("Custom speed detected, all clips will have a minimum duration of {} seconds". format(CUTSPEED))
    else:
        print(Fore.RED + "Argument {} for --speed is not valid, defaulting to --medium".format(arguments['--speed']))


## [ Some custom FUNCTIONS ]
# clipTrimmer™ is a function to cut the clips in sync using our betterCutsArray 
def clipTrimmer(dur, k):
    cb = random.randint(1, int(dur/5))
    ce = cb + (betterCutsArray[i+1] - betterCutsArray[i])
    rushQueue[i] = rushQueue[i].subclip(cb, ce)
    if arguments['-p'] is True: print(Style.DIM + "Clip #{}: duration {}s | Cut from {}s to {}s".format(i, dur, cb, ce))
    if arguments['-p'] is True: print(Style.DIM +  "Clip #{} done with a new duration of {}s".format(i, rushQueue[i].duration))
    # Append the result to rushList
    rushList.append(rushQueue[i])
    if arguments['-v'] is True: print(Fore.GREEN + "Clip #{} appended !".format(i))

# arrayTrimmer™ is a function that looks at an array and makes sure the cuts are not too fast and returns the new (slower) cuts to a new array
def arrayTrimmer(cutsArray, nseq, offset, min):
    m = 0
    betterCutsArray = []
    betterCutsArray.append(cutsArray[offset])
    while m < nseq:
        l = 1
        while cutsArray[offset+l] - cutsArray[offset] < min:
            l = l + 1
        betterCutsArray.append(cutsArray[offset+l])
        offset = offset + l
        m = m + 1
    if arguments['-v'] is True: print(Fore.GREEN + "Array has been reduced to {} cuts with a minimum duration of {}s".format(len(betterCutsArray), min))
    return betterCutsArray

# onsetFinder™ is a function that leverages librosa to find the onsets in the selected song and returns an array of the timestamps
def onsetFinder(MUSIQUE):
    if arguments['-v'] is True: print("Detecting cuts using onsetFinder™...")
    x, sr = librosa.load(MUSIQUE)
    onset_frames = librosa.onset.onset_detect(x, sr=sr, units='frames')
    onset_times = list(librosa.frames_to_time(onset_frames, sr=sr))
    return onset_times

# beatFinder™ is a function that leverages librosa to find the beats in the selected song and returns an array of the timestamps
def beatFinder(MUSIQUE):
    if arguments['-v'] is True: print("Detecting cuts using beatFinder™...")
    x, sr = librosa.load(MUSIQUE)
    beat, beats = librosa.beat.beat_track(x, sr=sr, units='frames')
    beat_times = list(librosa.frames_to_time(beats, sr=sr))
    return beat_times

# findTitleCardLength™ is a function to sync the title card's length to the music (while keeping it longer than 2 seconds)
def findTitleCardLength():
    k = 1
    while cutsArray[k] < 2:
        k = k + 1
    titleCardDuration = cutsArray[k]
    if arguments['-v'] is True: print("Title card duration will be {}s".format(titleCardDuration))
    return titleCardDuration, k


## [ MAIN App logic ]
# I'm leaving my mark, just because I can
if arguments['-z'] is False: print(Fore.YELLOW + Style.BRIGHT + "'Yeah, but your scientists were so preoccupied with whether or not they could, they didn't stop to think if they should.' -Dr. Ian Malcolm, Jurassic Park")
if arguments['-z'] is False: print(Fore.YELLOW + Style.BRIGHT + "ImpressionMovieMaker version {} by Julien 'bonj' Bono.".format(VERSION))

# List all the videos inside the FOLDER (and its subfolders) and push the paths into the clips array
clips = [os.path.join(r,file) for r,d,f in os.walk(RUSHESFOLDER) for file in f]
if arguments['-v'] is True: print("Number of rushes provided: {}".format(len(clips)))

# From clips, select a random number of files to remove from list. Make sure that the total number of rushes does not exceed 40.
clipCutter = random.randint(int(len(clips)/8), int(len(clips)/5))
while (len(clips)-clipCutter) > 40:
    clipCutter = random.randint(clipCutter+5, clipCutter+10)
if arguments['-v'] is True: print("ClipCutter™ will chop down {} rushes !".format(clipCutter))
for i in range(clipCutter):
    clips.pop(random.randint(0, len(clips)-1))

# Create a rushQueue array and populate it will all the clips from the clips array as VideoFileClip, selecting a random part of each clip to keep
rushQueue = []
if arguments['-z'] is False: print("Preparing clips...")
for clip in clips:
    rushQueue.append(VideoFileClip(clip))

# Set rushList as the final list of clips to be kept
rushList = []

# According to the user's selected method, generate an array with the timestamps for the cuts in sync with audio
# NOTE: defaults to beat detection
if arguments['-o'] is True: cutsArray = onsetFinder(MUSIQUE)
elif arguments['-x']: 
    beatsArray = beatFinder(MUSIQUE)
    onsetArray = onsetFinder(MUSIQUE)
    cutsArray = sorted(beatsArray + onsetArray)
else: cutsArray = beatFinder(MUSIQUE)
if arguments['-v'] is True: print("Found {} possible cuts in soundtrack, will use {}".format(len(cutsArray), len(rushQueue)+1))
# Use findTitleCardLength() to find the length of the title card
titleCardDuration, k = findTitleCardLength()
# Make sure the cuts are not too fast using the arrayTrimmer™ function and passing the array to cut, the expected length, the offset (from the intro) and the minimum duration of a segment
betterCutsArray= arrayTrimmer(cutsArray, len(rushQueue), k, CUTSPEED)

# Randomize the clips order (uncomment to make things more fun)
if arguments['-v'] & arguments['-r'] is True: print("Randomizing clip order...")
if arguments['-r'] is True: random.shuffle(rushQueue)

# From rushQueue, keep a random part of each clip
for i in range(len(rushQueue)):
    # Set the "max" var as an intenger of the clip's duration
    dur = int(rushQueue[i].duration)
    if arguments['-v'] is True: print("Working on clip #{} with a length of {}s".format(i, dur))

    # Check the clip's length. If shorter than 7 or longer than 60, discard that clip
    if arguments['-d'] is False and (dur < 7 or dur > 60):
            if arguments['-v'] is True: print(Fore.RED + "Queue item #{} too short/long, skipping.".format(i))
    elif arguments['-d'] is True and  dur < 6:
            if arguments['-v'] is True: print(Fore.RED + "Queue item #{} too short, skipping.".format(i))

    # Call upon clipTrimmer™
    clipTrimmer(dur, k)

# Concatenate all the clips inside the rushList into impression array (will make it easier to change the soudtrack)
impression = concatenate_videoclips(rushList)

# Let's take care of that title card !
if arguments['-z'] is False: print("Generating title card...")
# Render the three parts (exercice, company and date) separately
exerciceCard = TextClip(EXERCICE, size = (1920,1080), fontsize = 125, kerning=5, color = 'white').set_duration(titleCardDuration).set_position((0, -75))
compagnieCard = TextClip(COMPAGNIE, size = (1920,1080), fontsize = 45, color = 'grey').set_duration(titleCardDuration).set_position((-500, 50))
dateCard = TextClip(now.strftime('%d/%m/%Y'), size = (1920,1080), fontsize = 45, color = 'grey').set_duration(titleCardDuration).set_position((450, 50))
# Put them all together into titleCard as a single image (greatly speeds up rendering)
titleCard = CompositeVideoClip([compagnieCard, exerciceCard, dateCard]).to_ImageClip(t='1').set_duration(titleCardDuration)
# Put the tileCard and the impression together and concatenate them
impressionPlayList = [titleCard, impression]
impressionWithTitle = concatenate_videoclips(impressionPlayList)

# Let's take care of that soundtrack !
if arguments['-z'] is False: print("Compositing the audio...")
# Reduce the overall volume to 10%
impressionWithTitle = impressionWithTitle.volumex(0.1)
# Load the selected music into an AudioFileClip, and set its duration to the impression's duration
music = AudioFileClip(MUSIQUE)
music = music.set_duration(impressionWithTitle.duration)
# Set the combination of both into soundTrack, add a fade-out at the end and set soundTrack as the impression's soundtrack
# Make sure to skip impressionWithTitle.audio in case it has no audio track (ie: drone clips only..)
soundTrack = CompositeAudioClip([impressionWithTitle.audio, music]).fx(afx.audio_fadeout, 3) if impressionWithTitle.audio is not None else music.fx(afx.audio_fadeout, 3)
impressionWithTitle.audio = soundTrack

# Now that we have all our clips, let's put the final piece together by adding the intro logo, the title card and the outro logo
if arguments['-z'] is False: print("Putting it all together...")
videoTimeLine = []
videoTimeLine.append(VideoFileClip(LOGODEBUT))
videoTimeLine.append(impressionWithTitle)
videoTimeLine.append(VideoFileClip(LOGOFIN))

# Concatenate all the clips inside the IMPRESSION array
#print(rushList)
impressionFinal = concatenate_videoclips(videoTimeLine)

# Let's render that shit !
if arguments['-z'] is True: 
    impressionFinal.to_videofile(OUTFILE, logger=None)
else:
    print("Starting final rendering...")
    impressionFinal.to_videofile(OUTFILE)
    print(Fore.GREEN + Style.BRIGHT + "Done ! See the results at {}".format(OUTFILE))
