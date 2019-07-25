Ce script Python permet de convertir en masse des images TIFF ou JPEG vers le format JPEG2000. Il s'appuie sur la librairie [Image-processing](https://github.com/bodleian/image-processing) développée par la Bodleian Library (Oxford).

Son usage premier est de convertir des images source haute résolution dans un format permettant leur diffusion optimale sur le Web, conformément à [l'API Image de IIIF](https://iiif.io/api/image) (_International Image Interoperability Framework_).

## Caractéristiques

* prend un dossier en entrée (`input_dir`) et convertit toutes les images en JPEG2000 dans un dossier de sortie (`output_dir`).

* supporte à la fois les codecs [Kakadu](https://kakadusoftware.com/software/) (propriétaire) et [OpenJPEG](http://www.openjpeg.org/) (open source)

* le profil d'encodage utilisé pour la conversion est le même que celui utilisé par la Bodleian ("lossless" par défaut) :
https://image-processing.readthedocs.io/en/latest/jp2_profile.html

* valide avec [Jpylyzer](http://jpylyzer.openpreservation.org/) chaque image JPEG2000 créée

* conserve une partie des métadonnées embarquées (XMP, Dublin Core...). Il est possible d'extraire l'intégralité des métadonnées de l'image dans un fichier XML à part, car certaines métadonnées, notamment Exif, ne sont pas reportées dans le JPEG2000)

* s'efforce de conserver également dans le JPEG2000 le profil colorimétrique de l'image source

Pour plus de détails sur l'encodage en JPEG2000, lire la documentation de la librairie Image-processing : https://image-processing.readthedocs.io/en/latest/index.html

## Installation

### Dépendances

Ce script a été testé avec Python 3 (3.7.3).

Il repose sur la librairie Image-processing : https://github.com/bodleian/image-processing

Les autres dépendances sont aussi celles de Image-processing :

* [Kakadu](https://kakadusoftware.com/software/) ou [OpenJPEG](https://github.com/uclouvain/openjpeg) (**à installer séparément**)

* [Exiftool](http://owl.phy.queensu.ca/~phil/exiftool/) (**à installer séparément**)

* [Pillow](http://pillow.readthedocs.io/en/latest/) (installé automatiquement via `pip install`)

* [Jpylyzer](http://jpylyzer.openpreservation.org/) (installé automatiquement via `pip install`)

Voir le détail des dépendances de Image-processing : https://image-processing.readthedocs.io/en/latest/introduction.html#installation

### Procédure

**TODO :** 
* installer python 3 dans un virtualenv
* gérer le PYTHONPATH dans le script ?

```
$ which python3
$ mkvirtualenv --python=/usr/local/bin/python3 {VirtualEnvName}
$ source activate {VirtualEnvName} ?
$ git clone https://regisrob@bitbucket.org/regisrob/convert_jp2.git

// Before pip install :
apt install exiftool
apt install lcms2 lcms2-devel libtiff libtiff-devel libjpeg libjpeg-devel
// + compilation OpenJPEG
// + compilation Kakadu

$ cd convert_jp2
$ pip install -r requirements.txt
```

### Usage

```
usage: convert.py [-h] -i INPUT_DIR -o OUTPUT_DIR [--with-openjpeg]
                  [--with-kakadu] [-b BINARY_PATH] [--validate-jp2]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        Choose input directory
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Choose output directory
  --with-openjpeg       Select OpenJPEG encoder
  --with-kakadu         Select Kakadu encoder (default)
  -b BINARY_PATH, --binary-path BINARY_PATH
                        Base path to openjpeg or kakadu executables (default:
                        /usr/local/bin
  --validate-jp2        Validate generated JP2 files?
```



