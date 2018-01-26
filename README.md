# Convert images into a movie

## Installation

### Dependencies
- Python (2.7 or later)
- Python library future
- [mencoder](http://www.mplayerhq.hu/design7/news.html)
- [libav](https://libav.org/) (only for creating mp4 movies)
- [imagemagick](https://www.imagemagick.org/) (only when images are not png or jpg)

### Set up as command line program
1. Make script executable:
    ```chmod +x im2movie.py```
2. Create a link to `im2movie` in a folder in your `PATH`. For example, when you have a `bin` folder in your home
 that is in your `PATH`: `ln -s /path/to/im2movie/im2movie.py /home/USERNAME/bin/im2movie`
3. Now you can run the script with `im2movie`

### Python library
When the `im2movie` folder is in the python path, you can use the `makeMovie` function:

```
from im2movie import makeMovie
?im2movie

Signature: makeMovie(id, imtype, moviename, inputpath, outputpath, fps, nx=None, ny=None, bitrate=None, scale=1, quiet=True, win=False, vqscale=12, suffix='.avi', tomp4=False, postfix=None, maxres=(2000, 2000))
Docstring:
Creates movie of a series of images.

Creates a movie of a series of images using mencoder. The images are added to the movie in alphabetical order. If the png's are numbered, all numbers should contain the same number of digits, e.g.:
    - order of [im_1.png,im_10.png] = [im_10.png,im_1.png]
    - order of [im_01.png,im_10.png] = [im_01.png,im_10.png]
By defeault the mpeg4 codec is used for the movies, alternatively the msmpeg4v2 codec can be used (see Args).

Args:
    id: unique identifier for the images
    moviename: name of the generated movie (without suffix)
    inputpath: path to images
    outputpath: path were the movie will be saved
    fps: frames per second
    nx: number of horizontal pixels in the images, if omitted this will be extracted from the image
    ny: number of vertical pixels in the images, if omitted this will be extracted from the image
    bitrate: bitrate of the movie, if omitted this will be calucated based on the image size
    scale: scaling factor for the movie, recommended for large images
    quiet: print no extra information about the generated movie
    win: use msmpeg4v2 codec instead of mpeg4, this should work in Windows without installing any codecs
    vqscale: video quality (lower is better)
    suffix: video suffix
    tomp4: convert movie to mp4
    postifx: video postfix
    maxres: maximum movie resolution
```

## Usage

Example: combine `./im_*.png` into a movie `./movie.avi` showing 5 frames per second:

```im2movie -i ./ -t png -o ./ -p im -m movie -f 5```

More help:

```
im2movie -h
Usage: im2movie [options]

im2movie creates a small but decent movie from a set of images ussing
mencoder. Note that the images are added to the movie in the order they appear
in the directory, make sure they are ordered!

Options:
  -h, --help            show this help message and exit
  -q, --quiet           No output (mencoder output is always suppressed)
                        [False]
  -t IMTYPE, --type=IMTYPE
                        type of the images (currently supports png and jpg)
                        [png]
  -i INPUTPATH, --inputpath=INPUTPATH
                        folder with images [/home/mpalm/.python/im2movie]
  -o OUTPUTPATH, --outputpath=OUTPUTPATH
                        output folder [/home/mpalm/.python/im2movie]
  -p ID, --id=ID        first part of the filenames (should be unique to the
                        sequence that is to be converted)
  --postfix=POSTFIX     part of the filename that follow the image number
                        (only needed whed 'id' does not suffice to select the
                        right images
  -m MOVIENAME, --moviename=MOVIENAME
                        name of the video file (without extension) [id]
  -f FPS, --fps=FPS     frames per second [1]
  -x NX, --nx=NX        width, used to calculate the bitrate (nx obtained from
                        one of the images when omitted here)
  -y NY, --ny=NY        heigth, used to calculate the bitrate (ny obtained
                        from one of the images when omitted here)
  -b BITRATE, --bitrate=BITRATE
                        user specified bitrate, when omitted the bitrate is
                        calculated based on the image dimenstion
  -s SCALE, --scale=SCALE
                        scale movie (useful for large input images)
  -w, --windows         if you really really really want to use windows, this
                        may help (or not, i wouldn't know)
  -v VQSCALE, --vqscale=VQSCALE
                        quality, lower is better (but file size is larger)
                        [12]
  --mp4
```

## Acknowledgements

Thanks to [Gerhard Burger](https://github.com/burgerga) for adding several improvements.
