# ImpressionMovieMaker

## Installation

### Requirements:
- Python 3 (https://www.python.org/downloads/)
- Imagemagick (https://imagemagick.org/script/download.php) **/!\ Installer avec les options "Install FFMPEG" et "Install legacy utilities" selectionnées ! /!\**

### Installation
Après avoir installé Python3 et Imagemagick, télécharger "ImpressionMovieMaker.zip" et l'extraire. Dans l'invité de commande, naviguer dans le dossier et "*pip install -r requirements.txt*"

## Utilisation
Il est possible d'executer simplement ImpressionMovieMaker.py pour une utilisation "interactive".

Pour les plus avisés, une interface CLI existe ("*python ImpressionMovieMaker.py --help*" est votre ami).

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