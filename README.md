# ImpressionMovieMaker
<img src="/assets/logo.png" width=50% height=50%>

## Installation

### Requirements:
- Python 3 (https://www.python.org/downloads/)
- Imagemagick (https://imagemagick.org/script/download.php) /!\ **Install with options "Install FFMPEG" and "Install legacy utilities" checked o Windows!** /!\

### Installation
After installing Python3 and Imagemagick, download "ImpressionMovieMaker.zip" and extract it. In the command prompt, navigate to the folder and "*pip install -r requirements.txt*"

## Usage
Simply run ImpressionMovieMaker.py for a half-assed GUI experience.

For those who like it old-school (and nicer), a CLI interface exists ("*python ImpressionMovieMaker.py --help*" is your friend).

```
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
```
