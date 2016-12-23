# Convert images into a movie

## Installation

### Dependencies
- mencoder
- avconv (only for creating mp4 movies)

### Set up as command line program
1. Make script executable:
    ```chmod +x im2movie.py```
2. Create a link to `im2movie` in a folder in your `PATH`. For example, when you have a `bin` folder in your home
 that is in your `PATH`: `ln -s /path/to/VisGrid3D/im2movie.py /home/USERNAME/bin/im2movie`
3. Now you can run the script with `im2movie`

### Python library
1. Install dependencies (see above)
2. Place `im2movie` folder in the python path


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
