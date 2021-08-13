### [   ImpressionMovieMaker || Made 'fo shits 'n giggles by Julien 'bonj' Bono   ] ###

## [ CLI is cooler with docopt ]
"""
Usage: ImpressionMovieMaker.py [-dvzsph] [RUSHESFOLDER] [LOGODEBUT] [LOGOFIN] [MUSIQUE] [OUTFILE] [COMPAGNIE] [EXERCICE]

Arguments:
  RUSHESFOLDER      Dossier contenant les rushes.
  LOGODEBUT         Logo de début (troupe).
  LOGOFIN           Logo de fin (AAR).
  MUSIQUE           Musique pour l'impression.
  OUTFILE           Chemin vers le fichier de sortie.
  COMPAGNIE         Nom de la compagnie.
  EXERCICE          Nom de l'exercice.

Options:
  -h --help
  -s                Pour les hipster: ordre des séquences aléatoire.
  -d                Mode drone: les clips de drones de plus de 1 minute sont pris en compte. Attention: possiblement instable.
  -v                Mode verbose (montre les étapes de travail en détail, en anglais dans le texte).
  -z                Mode "zen"/silencieux (rien dans la console).
  -p                DEV: Montre les arguments passés au programme. 
"""


## [ IMPORTS be imports ]
import os
import random
import datetime
from moviepy.editor import *
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfile, asksaveasfile
from tkinter.simpledialog import askstring
from docopt import docopt
from colorama import init, Fore, Style

# Sets colorama to reset Fore/Style after each print
init(autoreset=True)

# "The time for us is now"
now = datetime.datetime.now()

# Needed to intitialize docopt (for CLI)
if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['-p'] is True: print(arguments)


## [ CONSTANTS are the new vars ]
VERSION = "0.1.1"

# Uh-oh, we might need the paths to FFMPEG and Imagemagick in some envs
#IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'C:\\convert.exe')
#os.environ['IMAGEIO_FFMPEG_EX'] = "C:\\ffmpeg.exe"

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

if arguments['OUTFILE'] is None: OUTFILE = asksaveasfile(title="Choisir ou sauvegarder le résultat")
else: OUTFILE = arguments['OUTFILE']

if arguments['COMPAGNIE'] is None: COMPAGNIE = input("Compagnie? ")
else: COMPAGNIE = arguments['COMPAGNIE']

if arguments['EXERCICE'] is None: EXERCICE = input("Nom de l'exercice? ")
else: EXERCICE = arguments['EXERCICE']


## [ Main App logic ] ##
# I'm leaving my mark, just because I can
if arguments['-z'] is False: print(Fore.YELLOW + Style.BRIGHT + "'Yeah, but your scientists were so preoccupied with whether or not they could, they didn't stop to think if they should.' -Dr. Ian Malcolm, Jurassic Park")
if arguments['-z'] is False: print(Fore.YELLOW + Style.BRIGHT + "ImpressionMovieMaker version {} by Julien 'bonj' Bono.".format(VERSION))

# List all the videos inside the FOLDER (and its subfolders) and push the paths into the clips array
clips = [os.path.join(r,file) for r,d,f in os.walk(RUSHESFOLDER) for file in f]
if arguments['-v'] is True: print("Number of rushes provided: {}".format(len(clips)))

# From clips, select a random number of files to remove from list. Make sure that the total number of rushes does not exceed 35.
clipCutter = random.randint(int(len(clips)/4), int(len(clips)/2))
while (len(clips)-clipCutter) > 35:
    clipCutter = random.randint(clipCutter+5, clipCutter+10)
if arguments['-v'] is True: print("ClipCutter™ will chop down {} rushes !".format(clipCutter))
for i in range(clipCutter):
    clips.pop(random.randint(0, len(clips)-1))

# Create a rushQueue array and populate it will all the clips from the clips array as VideoFileClip, selecting a random part of each clip to keep
rushQueue = []
if arguments['-z'] is False: print("Preparing clips...")
for clip in clips:
    rushQueue.append(VideoFileClip(clip))

# Set rushList as the final list of clips to be kept and the index j to 0
rushList = []

# From rushQueue, keep a random part of each clip
for i in range(len(rushQueue)):
    # Set the "max" var as an intenger of the clip's duration
    max = int(rushQueue[i].duration)

    if arguments['-v'] is True: print("Working on clip #{} with a length of {}".format(i, max))

    # Check the clip's length. If shorter than 6 or longer than 60, discard that clip.
    if arguments['-d'] is False and (max < 6 or max > 60):
            if arguments['-v'] is True: print(Fore.RED + "Clip #{} too short/long, skipping.".format(i))
    if arguments['-d'] is True and  max < 6:
            if arguments['-v'] is True: print(Fore.RED + "Clip #{} too short, skipping.".format(i))

    # Cut select a random part of the clip; do this until clip is less than 5 seconds
    else:
        while max > 5:
            cb = int(random.randint(2, int(max/2)))
            ce = -2 #int(random.randint(-2, int(-(max/2)))) #TODO: Replace with random value between -2 and -x !
            if arguments['-v'] is True: print(Style.DIM + "Clip #{}: duration {}s | Cut from {}s to {}s".format(i, max, cb, ce))
            rushQueue[i] = rushQueue[i].subclip(cb, ce)
            max = int(rushQueue[i].duration) 
            if arguments['-v'] is True: print(Style.DIM +  "Clip #{} done with a new duration of {}s".format(i, max))
        # Append the result to rushList
        rushList.append(rushQueue[i])
        if arguments['-v'] is True: print(Fore.GREEN + "Clip #{} appended !".format(i))

# Randomize the clips order (uncomment to make things more fun)
if arguments['-v'] & arguments['-s'] is True: print("Randomizing clip order...")
if arguments['-s'] is True: random.shuffle(rushList)

# Concatenate all the clips inside the rushList into impression array (will make it easier to change the soudtrack)
impression = concatenate_videoclips(rushList)

# Let's take care of that title card !
if arguments['-z'] is False: print("Generating title card...")
# Render the three parts (exercice, company and date) separately
exerciceCard = TextClip(EXERCICE, size = (1920,1080), fontsize = 125, kerning=5, color = 'white').set_duration(3).set_position((0, -75))
compagnieCard = TextClip(COMPAGNIE, size = (1920,1080), fontsize = 45, color = 'grey').set_duration(3).set_position((-500, 50))
dateCard = TextClip(now.strftime('%d/%m/%Y'), size = (1920,1080), fontsize = 45, color = 'grey').set_duration(3).set_position((450, 50))
# Put them all together into titleCard as a single image (greatly speeds up rendering)
titleCard = CompositeVideoClip([compagnieCard, exerciceCard, dateCard]).to_ImageClip(t='1').set_duration(3)
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
soundTrack = CompositeAudioClip([impressionWithTitle.audio, music]).fx(afx.audio_fadeout, 3)
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
if arguments['-z'] is False: print("Starting final rendering...")
impressionFinal.to_videofile(OUTFILE)
if arguments['-z'] is False: print(Fore.GREEN + Style.BRIGHT + "Done ! See the results at {}".format(OUTFILE))