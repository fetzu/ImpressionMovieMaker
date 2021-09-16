# ImpressionMovieMaker

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
Usage: ImpressionMovieMaker.py [-dvzsph] [RUSHESFOLDER] [LOGODEBUT] [LOGOFIN] [MUSIQUE] [OUTFILE] [COMPAGNIE] [EXERCICE]

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
    -s                For hipsters: randomises the sequencing of the rushes.
    -d                Drone mode: rushes longer than 1 minute are used. Warning: memory consuming and possibly unstable.
    -v                Verbose mode.
    -z                "zen"/silent mode (almost nothing is logged to the terminal).
    -p                DEV: Shows the arguments passed to the program.
```