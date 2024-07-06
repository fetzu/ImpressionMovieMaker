### [   ImpressionMovieMaker || Made 'fo shits 'n giggles by Julien 'bonj' Bono   ] ###

## [ CLI is cooler with docopt ]
"""
Usage: ImpressionMovieMaker.py [-hvzpboxdrtsmf] [--troupe=<type>] [--slow|--medium|--fast] [--speed <seconds>] [--gui] [RUSHESFOLDER] [LOGODEBUT] [LOGOFIN] [MUSIQUE] [OUTFILE] [COMPAGNIE] [EXERCICE]

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
    -t --troupe <art|mec|inf|neutre>
                      Selects the kind of troop ("art", "mec", "inf" or "neutre").
    -s --slow         Slow cut speeds (each clip will last at least somewhere between 3 and 5 seconds).
    -m --medium       Medium cut speeds (each clip will last at least somewhere between 1.75 and 3.25 seconds) [default].
    -f --fast         Fast cut speeds (each clip will last at least somewhere between 1 and 2 seconds).
    --speed <sec>     Specify the minimum duration of a cut in seconds (overrides pre-set cut speeds).
    --gui             If you'd rather use the GUI.
"""


## [ IMPORTS be imports ]
import os
import sys
import random
import datetime
import warnings
import librosa
import PySimpleGUI as gui
# NOTE: This fixes the build for windows by only importing the necessary modules from MoviePy
#from moviepy.editor import *
from moviepy.video.VideoClip import TextClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.fx import volumex as xfa, audio_fadeout as afx
from docopt import docopt
from colorama import init, Fore, Style
from IMMAssets import LoadAssets


## [ Some INIT settings ]
# Gets read of those pesky Pysoundfile/audioread librosa warnings.
warnings.filterwarnings("ignore")

# Sets colorama to reset Fore/Style after each print
init(autoreset=True)

# "The time for us is now"
NOW = datetime.datetime.now()

# This bit gets the taskbar icon working properly in Windows (thanks to unexpectedpanda @ https://github.com/PySimpleGUI/PySimpleGUI/issues/2722)
if sys.platform.startswith('win'):
    import ctypes
    # Make sure Pyinstaller icons are still grouped
    if sys.argv[0].endswith('.exe') is False:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('BonoProd.ImpressionMovieMaker.GUImpressionMovieMaker.2')

# Needed to intitialize docopt (for CLI)
if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['-p'] is True: print(arguments)


## [ CONSTANTS are the new vars ]
VERSION = "2.1.8"
USEGUI = False
DISTROMODE = False

# Uh-oh, we might need the paths to FFMPEG and Imagemagick in some envs
#IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'C:\\convert.exe')
#os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\ffmpeg.exe"

# If the user started with the --gui argument, use the gui...
if arguments['--gui'] is not False:
    USEGUI = True
else:
    # If not, check if (all) arguments were passed through the CLI. If they were: set the constants, if they weren't: force the user to use the GUI !
    # The names are pretty self explanatory (if they aren't read the docs!)
    if arguments['RUSHESFOLDER'] is None: USEGUI = True
    else: RUSHESFOLDER = arguments['RUSHESFOLDER']

    if arguments['LOGODEBUT'] is None: USEGUI = True
    else: LOGODEBUT = arguments['LOGODEBUT']

    if arguments['LOGOFIN'] is None: USEGUI = True
    else: LOGOFIN = arguments['LOGOFIN']

    if arguments['MUSIQUE'] is None: USEGUI = True
    else: MUSIQUE = arguments['MUSIQUE']

    if arguments['OUTFILE'] is None: USEGUI = True
    else: OUTFILE = arguments['OUTFILE']

    if arguments['COMPAGNIE'] is None: USEGUI = True
    else: COMPAGNIE = arguments['COMPAGNIE']

    if arguments['EXERCICE'] is None: USEGUI = True
    else: EXERCICE = arguments['EXERCICE']

    if arguments['--slow'] is True: CUTSPEED = random.uniform(3, 5)
    elif arguments['--medium'] is True: CUTSPEED = random.uniform(1.75, 3.25)
    elif arguments['--fast'] is True: CUTSPEED = random.uniform(1, 2)
    else: CUTSPEED = random.uniform(1.75, 3.25)

    if "art" in arguments['--troupe']: TROOPCOLOR = "red"
    elif"mec" in arguments['--troupe']: TROOPCOLOR = "yellow"
    elif "inf" in arguments['--troupe']: TROOPCOLOR = "green"
    else: TROOPCOLOR = "grey"

    if arguments['--speed'] is not None:
        if arguments['--speed'].isdigit():
            CUTSPEED = arguments['--speed']
            print(f"Custom speed detected, all clips will have a minimum duration of {CUTSPEED} seconds")
        else:
            print(Fore.RED + f"Argument {arguments['--speed']} for --speed is not valid, defaulting to --medium")


## [ Some custom FUNCTIONS ]
def clipTrimmer(clipsArray, toCutArray, maxduration):
    """
    clipTrimmer™ is a function to cut the clips in sync using our betterCutsArray.
    It takes an array of clip objects, an array of cuts and maximum duration (maxdur)
    and proceeds to cut down every clip's duration under the defined duration.
    """
    cb = random.randint(1, int(maxduration/5))
    ce = cb + (toCutArray[i+1] - toCutArray[i])
    clipsArray[i] = clipsArray[i].subclip(cb, ce)
    if arguments['-p'] is True: print(Style.DIM + f"Clip #{i}: duration {maxduration}s | Cut from {cb}s to {ce}s")
    if arguments['-p'] is True: print(Style.DIM + f"Clip #{i} done with a new duration of {clipsArray[i].duration}s")
    # Append the result to rushList
    rushList.append(clipsArray[i])
    if arguments['-v'] is True: print(Fore.GREEN + f"Clip #{i} appended !")

def arrayTrimmer(toCutArray, nseq, offset, minduration):
    """
    arrayTrimmer™ is a function that looks at an array and makes sure the cuts
    are not too fast and returns the new (slower) cuts to a new array.
    It takes and array to cut, the expected length in seconds,
    the offset (from the intro/first cut) and the minimum duration of a segment.
    """
    m = 0
    betterCutsArray = []
    betterCutsArray.append(toCutArray[offset])
    while m < nseq:
        l = 1
        while cutsArray[offset+l] - toCutArray[offset] < minduration:
            l = l + 1
        betterCutsArray.append(toCutArray[offset+l])
        offset = offset + l
        m = m + 1
    if arguments['-v'] is True: print(Fore.GREEN + f"Array has been reduced to {len(betterCutsArray)} cuts with a minimum duration of {minduration}s")
    return betterCutsArray

def onsetFinder(MUSIC):
    """
    onsetFinder™ is a function that leverages librosa to find the onsets
    in the selected song and returns an array of the timestamps.
    It takes a clip object as input and returns an array with onset timestamps.
    """
    if arguments['-v'] is True: print("Detecting cuts using onsetFinder™...")
    x, sr = librosa.load(MUSIC)
    onset_frames = librosa.onset.onset_detect(x, sr=sr, units='frames')
    onset_times = list(librosa.frames_to_time(onset_frames, sr=sr))
    return onset_times

def beatFinder(MUSIC):
    """
    beatFinder™ is a function that leverages librosa to find the beats/tempo
    in the selected song and returns an array of the timestamps.
    It takes a clip object as input and returns an array with onset timestamps.
    """
    if arguments['-v'] is True: print("Detecting cuts using beatFinder™...")
    x, sr = librosa.load(MUSIC)
    beat, beats = librosa.beat.beat_track(x, sr=sr, units='frames')
    if arguments['-v'] is True: print(f"beatFinder™ detected a beat of {beat} beats-per-second...")
    beat_times = list(librosa.frames_to_time(beats, sr=sr))
    return beat_times

# findTitleCardLength™ is a function to sync the title card's length to the music (while keeping it longer than 2 seconds)
def findTitleCardLength(myCutsArray):
    """
    findTitleCardLength™ is a function to sync the title card's length to the music
    (while keeping it longer than 2 seconds).
    """
    k = 1
    while myCutsArray[k] < 2:
        k = k + 1
    cardDuration = myCutsArray[k]
    if arguments['-v'] is True: print(f"Title card duration will be {cardDuration}s")
    return cardDuration, k

## [ The GUI lies here ]
def GUI():
    """
    Defines the GUI layout
    """
    gui.theme('Black') #"Default1" is gray (and a little sadder)

    frame_files = [[gui.Text("Dossier de rushes", size=(20, 1)),
                    gui.InputText(key="RUSHESFOLDER"), gui.FolderBrowse("Choisir ")],
                    [gui.Text("Logo d'intro / de troupe", size=(20, 1)),
                    gui.InputText(key="LOGODEBUT"), gui.FileBrowse("Choisir ", file_types = (('Video MP4', '*.mp4'),('TOUS','*.*')))],
                    [gui.Text("Logo de fin / AAR", size=(20, 1)),
                    gui.InputText(key="LOGOFIN"), gui.FileBrowse("Choisir ", file_types = (('Video MP4', '*.mp4'),('TOUS','*.*')))],
                    [gui.Text("Musique", size=(20, 1)),
                    gui.InputText(key="MUSIQUE"), gui.FileBrowse("Choisir ", file_types = (('Fichier MP3', '*.mp3'),('Fichier WAV', '*.wav'),('Fichier FLAC', '*.flac'),('TOUS','*.*')))]]

    frame_infos = [[gui.Text("Date de l'exercice", size=(17, 1)),
                    gui.Input(NOW.strftime('%d/%m/%Y'), key="CUSTOMDATE", size=(25, 1)),
                    gui.CalendarButton('Choisir', target="CUSTOMDATE", format="%d/%m/%Y")],
                    [gui.Text("Compagnie", size=(17, 1)),
                    gui.Input(key="COMPAGNIE", size=(33, 1))],
                    [gui.Text("Nom de l'exercice", size=(17, 1)),
                    gui.Input(key="EXERCICE", size=(33, 1))],
                    [gui.Text("Type de troupe", size=(17, 1)),
                    gui.Radio("Artillerie", 2, False, size=(10, 1), text_color="red", key="ART"),
                    gui.Radio("Mécanisée", 2, False, size=(10, 1), text_color="yellow", key="MEC")],
                    [gui.Text("", size=(17, 1)),
                    gui.Radio("Infanterie", 2, False, size=(10, 1), text_color="green", key="INF"),
                    gui.Radio("Neutre", 2, True, size=(10, 1), key="NEUTRE")]]

    frame_cutting = [[gui.Text("Vitesse du montage: ", size=(20, 1)), gui.Radio("Lente", 0, False, size=(7, 1), key="SLOW"),
                    gui.Radio("Moyenne", 0, True, size=(7, 1), key="MEDIUM"),
                    gui.Radio("Rapide", 0, False, size=(7, 1), key="FAST")],
                    [gui.Text("Détection des coupes: ", size=(20, 1)), gui.Radio("Détection du rythme", 1, True, size=(14, 1), key="BEATMODE"),
                    gui.Radio("Détection des variations", 1, False, size=(17, 1), key="ONSETMODE"),
                    gui.Radio("Mixte", 1, False, size=(4, 1), key="HYBRIDMODE")]]
    frame_extra = [[gui.Checkbox("Utiliser plans drones / de plus de 60 secondes", key="DRONEMODE", size=(45, 1))],
                    [gui.Checkbox("Ordre des rushes aléatoire", key="SHUFFLEMODE", size=(45, 1))]]

    bloc1 = [gui.Frame('Fichiers source', frame_files, vertical_alignment="top"), gui.Frame('Données pour le titrage', frame_infos, vertical_alignment="top")]

    bloc2 = [gui.Frame('Options du montage', frame_cutting, vertical_alignment="top"), gui.Frame('Options supplémentaires', frame_extra, vertical_alignment="top")]

    layout =    [[gui.Text("", size=(0, 1))],
                [gui.Image(data=IMMLOGO, size=(500, 250), expand_x=True)],
                [gui.Text("", size=(0, 1))],
                [bloc1],
                [gui.Text("", size=(0, 1))],
                [bloc2],
                [gui.Text("", size=(0, 1))],
                [gui.Text("Sauver l'impression sous...", size=(20, 1)),
                gui.InputText(key="OUTFILE", size=(106, 1)),
                gui.FileSaveAs("Choisir ", file_types = (('MP4', '*.mp4'),))],
                [gui.Text("", size=(0, 1))],
                [gui.Multiline(autoscroll=True, enter_submits=False, background_color="black", text_color="white", auto_refresh=True, reroute_stdout=True, reroute_stderr=False, no_scrollbar=True, size=(100, 9), font='Courier 10'),
                gui.Submit("Go", button_color="green", font="bold", size=(15, 5))]]

    # Create the window
    window = gui.Window(f'ImpressionMovieMaker v{VERSION}', layout, icon=IMMICON)
    event, guivalues = window.read()
    return event, guivalues

# If USEGUI is true.. bring the GUI to life
if USEGUI is True:
    IMMICON, IMMLOGO = LoadAssets()
    button, guivalues = GUI()
    RUSHESFOLDER, LOGODEBUT, LOGOFIN, MUSIQUE, OUTFILE, COMPAGNIE, EXERCICE, CUSTOMDATE, SLOW, MEDIUM, FAST, BEATMODE, ONSETMODE, HYBRIDMODE, DRONEMODE, SHUFFLEMODE, ART, MEC, INF, NEUTRE = guivalues['RUSHESFOLDER'], guivalues['LOGODEBUT'], guivalues['LOGOFIN'], guivalues['MUSIQUE'], guivalues['OUTFILE'], guivalues['COMPAGNIE'], guivalues['EXERCICE'], guivalues['CUSTOMDATE'], guivalues['SLOW'], guivalues['MEDIUM'], guivalues['FAST'], guivalues['BEATMODE'], guivalues['ONSETMODE'], guivalues['HYBRIDMODE'], guivalues['DRONEMODE'], guivalues['SHUFFLEMODE'], guivalues['ART'], guivalues['MEC'], guivalues['INF'], guivalues['NEUTRE']

    # Translate GUI aguments to CLI arguments
    if SLOW is True: CUTSPEED = random.uniform(3, 5)
    if MEDIUM is True: CUTSPEED = random.uniform(1.75, 3.25)
    if FAST is True: CUTSPEED = random.uniform(1, 2)

    if BEATMODE is True: arguments['-b'] = True
    if ONSETMODE is True: arguments['-o'] = True
    if HYBRIDMODE is True: arguments['-x'] = True

    if DRONEMODE is True: arguments['-d'] = True
    if SHUFFLEMODE is True: arguments['-r'] = True

    if ART is True: TROOPCOLOR = "red"
    if MEC is True: TROOPCOLOR = "yellow"
    if INF is True: TROOPCOLOR = "green"
    if NEUTRE is True: TROOPCOLOR = "grey"

## [ MAIN App logic ]
# I'm leaving my mark, just because I can
if arguments['-z'] is False and USEGUI is False:
    print(Fore.YELLOW + Style.BRIGHT + "'Yeah, but your scientists were so preoccupied with whether or not they could, they didn't stop to think if they should.' -Dr. Ian Malcolm, Jurassic Park")
if arguments['-z'] is False:
    if USEGUI is True: print(f"ImpressionMovieMaker version {VERSION} by Julien 'bonj' Bono.")
    else: print(Fore.YELLOW + Style.BRIGHT + f"ImpressionMovieMaker version {VERSION} by Julien 'bonj' Bono.")

# List all the videos inside the FOLDER (and its subfolders) and push the paths into the clips array
clips = [os.path.join(r,file) for r,d,f in os.walk(RUSHESFOLDER) for file in f]
if arguments['-v'] is True: print(f"Number of rushes provided: {len(clips)}")

# From clips, select a random number of files to remove from list. Make sure that the total number of rushes does not exceed 40.
clipCutter = random.randint(int(len(clips)/8), int(len(clips)/5))
while (len(clips)-clipCutter) > 40:
    clipCutter = random.randint(clipCutter+5, clipCutter+10)
if arguments['-v'] is True: print(f"ClipCutter™ will chop down {clipCutter} rushes !")
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
if arguments['-v'] is True: print(f"Found {len(cutsArray)} possible cuts in soundtrack, will use {len(rushQueue)+1}")
# Use findTitleCardLength() to find the length of the title card
titleCardDuration, titleCardOffset = findTitleCardLength(cutsArray)
# Make sure the cuts are not too fast using the arrayTrimmer™ function and passing the array to cut, the expected length, the offset (from the intro) and the minimum duration of a segment
finalCutsArray= arrayTrimmer(cutsArray, len(rushQueue), titleCardOffset, CUTSPEED)

# Randomize the clips order (uncomment to make things more fun)
if arguments['-v'] & arguments['-r'] is True: print("Randomizing clip order...")
if arguments['-r'] is True: random.shuffle(rushQueue)

# From rushQueue, keep a random part of each clip
for i in range(len(rushQueue)):
    # Set the "max" var as an intenger of the clip's duration
    dur = int(rushQueue[i].duration)
    if arguments['-v'] is True: print(f"Working on clip #{i} with a length of {dur}s")

    # Check the clip's length. If shorter than 7 or longer than 60, discard that clip
    if arguments['-d'] is False and (dur < 7 or dur > 60):
        if arguments['-v'] is True:
            print(Fore.RED + f"Queue item #{i} too short/long, skipping.")
            continue
    elif arguments['-d'] is True and  dur < 6:
        if arguments['-v'] is True:
            print(Fore.RED + f"Queue item #{i} too short, skipping.")
            continue

    # Call upon clipTrimmer™
    clipTrimmer(rushQueue, finalCutsArray, dur)

# Concatenate all the clips inside the rushList into impression array (will make it easier to change the soudtrack)
impression = concatenate_videoclips(rushList)

# Let's take care of that title card !
if arguments['-z'] is False: print("Generating title card...")
# Render the three parts (exercice, company and date) separately
exerciceCard = TextClip(EXERCICE, size = (1920,1080), fontsize = 125, kerning=5, color = 'white').set_duration(titleCardDuration).set_position((0, -75))
compagnieCard = TextClip(COMPAGNIE, size = (1920,1080), fontsize = 45, color = TROOPCOLOR).set_duration(titleCardDuration).set_position((-500, 50))
if USEGUI is True: dateCard = TextClip(CUSTOMDATE, size = (1920,1080), fontsize = 45, color = 'grey').set_duration(titleCardDuration).set_position((450, 50))
if USEGUI is False: dateCard = TextClip(NOW.strftime('%d/%m/%Y'), size = (1920,1080), fontsize = 45, color = 'grey').set_duration(titleCardDuration).set_position((450, 50))
# Put them all together into titleCard as a single image (greatly speeds up rendering)
titleCard = CompositeVideoClip([compagnieCard, exerciceCard, dateCard]).to_ImageClip(t='1').set_duration(titleCardDuration)
# Put the tileCard and the impression together and concatenate them
impressionPlayList = [titleCard, impression]
impressionWithTitle = concatenate_videoclips(impressionPlayList)

# Let's take care of that soundtrack !
if arguments['-z'] is False: print("Compositing the audio...")
# Reduce the overall volume to 10%
impressionWithTitle = impressionWithTitle.fx(xfa.volumex, 0.1)
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
elif DISTROMODE is True: # This is done because the logger crashes the distributed software
    print("Starting final rendering...")
    impressionFinal.to_videofile(OUTFILE, logger=None)
    if USEGUI is True: print(f"Done ! See the results at {OUTFILE}")
    else: print(Fore.GREEN + Style.BRIGHT + f"Done ! See the results at {OUTFILE}")
else:
    print("Starting final rendering...")
    impressionFinal.to_videofile(OUTFILE)
    if USEGUI is True: print(f"Done ! See the results at {OUTFILE}")
    else: print(Fore.GREEN + Style.BRIGHT + f"Done ! See the results at {OUTFILE}")

# Show a popup with success message
if USEGUI is True: gui.popup_auto_close(f"Terminé ! Le résultat se trouve ici: {OUTFILE}", title="Terminé !", auto_close_duration=10)

# Show the result (using the OS's default video file player)
os.startfile(OUTFILE)
