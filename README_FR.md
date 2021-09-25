# ImpressionMovieMaker

## Installation

### Requirements:
- Python 3 (https://www.python.org/downloads/)
- Imagemagick (https://imagemagick.org/script/download.php) /!\ **Installer avec les options "Install FFMPEG" et "Install legacy utilities" selectionnées !** /!\

### Installation
Après avoir installé Python3 et Imagemagick, télécharger "ImpressionMovieMaker.zip" et l'extraire. Dans l'invité de commande, naviguer dans le dossier et "*pip install -r requirements.txt*"

## Utilisation
Il est possible d'executer simplement ImpressionMovieMaker.py pour une utilisation "interactive".

Pour les plus avisés, une interface CLI existe ("*python ImpressionMovieMaker.py --help*" est votre ami).

```
Usage: ImpressionMovieMaker.py [-hvzpboxdrsmf] [--speed <secondes>] [--gui] [RUSHESFOLDER] [LOGODEBUT] [LOGOFIN] [MUSIQUE] [OUTFILE] [COMPAGNIE] [EXERCICE]

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
    -v                Mode verbose (montre les étapes de travail en détail, en anglais dans le texte).
    -z                Mode "zen"/silencieux (rien dans la console).
    -p                DEV: Montre les arguments passés au programme et les details de clipTrimmer™.
    -b                BeatMode: utilise la détéction de rythme pour les coupes [par défaut].
    -o                OnsetMode: utilise la détéction des "onsets" pour les coupes.
    -x                HybridMode: combine la détéction de rythme et des "onsets".
    -d                Mode drone: les clips de drones de plus de 1 minute sont pris en compte. Attention: possiblement instable.
    -r                Pour les hipster: ordre des séquences aléatoire.
    -s --slow         Vitesse de montage lente (chaque séquence dure au moins entre 3 et 5 secondes).
    -m --medium       Vitesse de montage moyenne (chaque séquence dure au moins entre 1.75 et 3.25 secondes) [par défaut].
    -f --fast         Vitesse de montage rapide (chaque séquence dure au moins entre 1 et 2 secondes).
    --speed <sec>     Specifier la durée minimale de chaque séquence (remplace les vitesses de montage pré-spécifiées).
    --gui             Pour utiliser l'interface graphique.
```
