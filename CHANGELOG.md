# Changelog
Hi there, this is a changelog.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project *somewhat* adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
*nothing*

## [1.0.0] - 2021-09-19
**The "I think I'm done with this" release !** 

### Added
- Hybrid mode that combines both beatFinder™ and onsetFinder™.
- Ability to toggle between three pre-set cutting speeds (--slow, --medium, --fast) which are generated a random at each start.
- Ability to set a minimum cutting speed by the user (with --speed <seconds>)

### Changed
- Revamped CLI (docopt and README[_FR]) to reflect new changes.
- **!Random sequence order argument has been changed from "-s" to "-r".**

## [0.2.1] - 2021-09-19
**The stupid mistake hotfix !** 

### Changed
- Fixed typo in console output code which caused program to crash under certain conditions...

## [0.2.0] - 2021-09-18
**The music sync update !** 
ImpressionMovieMaker is now smarter and syncs to the soundtrack !

### Added
- onsetFinder™ and beatFinder™ using librosa to find onsets or beats (respectively) to sync the song and the cuts.
- findTitleCardLength™ and arrayTrimmer™ make the syncing to the beat/onset possible.
- librosa added to *requirements.txt*.
- Translated/created a README in English.
- Added a CHANGELOG and created (pre-)releases from v0.0.1 retroactively.

### Changed
- Revamped CLI (docopt and README).
- clipTrimmer™ has been updated to use song syncing capabilities.
- clipCutter™ values have been tweaked.
- Title Card duration is no longer static, it is now synced to the onset/beat with a minimum duration of 2 seconds.
- Moved some stuff around in *ImpressionMovieMaker.py*.
- Moved the old README (in French) to *README_FR.md*.
- Some console outputs have been moved to DEV mode (*-p*).

## [0.1.4] - 2021-08-13
### Added
- * Implements clipTrimmer™, a proprietary and extremely complex algorithm that trims down the clips (..not really, just refactored the clip trimming into its own function to fix an issue).

## [0.1.3] - 2021-08-13
### Changed
- Fixed file import through GUI.

## [0.1.2] - 2021-08-13
### Added
- Added missing docopt to the requirements.
- Now checks for a "minimum" duration value (clip must be at least 2 seconds after cutting).

### Changed
- Corrected some logic mistakes at the video shortening stage.
- Tweaked the clipCutter™ and max values.

## [0.1.1] - 2021-08-13
### Added
- Added a fade out of 3 seconds to the soundtrack.

### Changed
- Fixed formatting in the README.

## [0.1.0] - 2021-08-12
### Added
- Title card generation.
- Console output are now in color (thanks to colorama).
- Various console outputs.
- *README.md* file with some basic guidance (in French).

### Changed
- Dev mode CLI from '-d' to '-p'.
- Fixed console output appearing in some conditions.

## [0.0.2] - 2021-08-12
### Added
- CLI (using docopts).
- .gitignore with some stuff.

### Changed
- Minor text fixes.

## [0.0.1] - 2021-08-11
### Added
- Created *ImpressionMovieMaker.py* as  bare-bones python application (takes a rush folder, IN and OUT logo files (video) and music (audio) and makes a passable impression).
- Created *requirements.txt* for required python libraries (*pip install -r requirements.txt* is your friend.).

[Unreleased]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.2.1...v1.0.0
[0.2.1]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/fetzu/ImpressionMovieMaker/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/fetzu/ImpressionMovieMaker/releases/tag/v0.0.1