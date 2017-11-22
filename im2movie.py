#!/usr/bin/env python
"""Create movie from a series of images using mencoder"""

from optparse import OptionParser
import sys
import os
import glob
import future

__author__ = "Margriet Palm"
__copyright__ = "Copyright 2009"
__credits__ = "Margriet Palm"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Margriet Palm"

def parse_args():
    # read arguments
    args = sys.argv
    # create option parser
    # used: q,i,o,p,m,f,w
    usage = "usage: %prog [options]"
    description = "im2movie creates a small but decent movie from a set of images ussing mencoder. " \
                  "Note that the images are added to the movie in the order they appear in the directory, " \
                  "make sure they are ordered!"
    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                      help="No output (mencoder output is always suppressed) [%default]", default=False)
    parser.add_option("-t", "--type", type="string", dest="imtype", default="png",
                      help="type of the images (currently supports png and jpg) [%default]")
    parser.add_option("-i", "--inputpath", type="string", dest="inputpath", default=os.getcwd(),
                      help="folder with images [%default]")
    parser.add_option("-o", "--outputpath", type="string", dest="outputpath", default=os.getcwd(),
                      help="output folder [%default]")
    parser.add_option("-p", "--id", type="string", dest="id", default="",
                      help="first part of the filenames (should be unique to the sequence that is to be converted)")
    parser.add_option("--postfix", type="string", dest="postfix",
                      help="part of the filename that follow the image number (only needed whed 'id' "
                           "does not suffice to select the right images")
    parser.add_option("-m", "--moviename", type="string", dest="moviename",
                      help="name of the video file (without extension) [id]")
    parser.add_option("-f", "--fps", type="float", dest="fps", default=1, help="frames per second [%default]")
    parser.add_option("-x", "--nx", type="int", dest="nx",
                      help="width, used to calculate the bitrate (nx obtained from one "
                           "of the images when omitted here)")
    parser.add_option("-y", "--ny", type="int", dest="ny",
                      help="heigth, used to calculate the bitrate (ny obtained from one "
                           "of the images when omitted here)")
    parser.add_option("-b", "--bitrate", type="int", dest="bitrate",
                      help="user specified bitrate, when omitted the bitrate is calculated "
                           "based on the image dimenstion")
    parser.add_option("-s", "--scale", type="float", dest="scale", default=1,
                      help="scale movie (useful for large input images)")
    parser.add_option("-w", "--windows", action="store_true", dest="win",
                      help="if you really really really want to use windows, this may "
                           "help (or not, i wouldn't know)")
    parser.add_option("-v", "--vqscale", type="int", dest="vqscale", default=12,
                      help="quality, lower is better (but file size is larger) [%default]")
    parser.add_option("--mp4", action="store_true", dest="mp4")
    (options, args) = parser.parse_args(args)
    if not options.moviename:
        options.moviename = options.id
    return options

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def makeMovie(id, imtype, moviename, inputpath, outputpath, fps, nx=None, ny=None, bitrate=None, scale=1, quiet=True,
              win=False,vqscale=12, suffix='.avi', tomp4=False, postfix=None, maxres=(2000, 2000)):
    """ Creates movie of a series of images.

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
    """
    if imtype not in ['png', 'jpg']:
        imtype = 'png'
        if not quiet:
            print('unsuported image type -> im2movie will convert all images to png')
        os.system('mogrify -format png -depth 8 ' + shellquote(inputpath + id + '*' + postfix + '.' + imtype))
    if not inputpath.endswith('/'):
        inputpath += '/'
    if not outputpath.endswith('/'):
        outputpath += '/'
    if not suffix.startswith('.'):
        suffix = '.' + suffix
    if postfix is None:
        postfix = ''
    else:
        moviename += '_' + postfix
    if bitrate is None:
        if (nx is None) or (ny is None):
            sample = glob.glob(inputpath+id+'*'+postfix+'.'+imtype)[0]
            try:
                from PIL import Image
            except:
                sys.exit("Could not calculate image size with PIL")
            (nx, ny) = Image.open(sample).size
        bitrate = nx * ny * 25 * 50 / 256
    if bitrate > 24000000:
        bitrate = 24000000
    # print some info
    snx = int(nx * scale)
    sny = int(ny * scale)
    if (snx > maxres[0]) or (sny > maxres[1]):
        extra_scale = min([maxres[0] / float(snx), maxres[1] / float(sny)])
        snx = int(extra_scale * snx)
        sny = int(extra_scale * sny)
    codec = 'mpeg4'
    if win:
        codec = 'msmpeg4v2'
    if not quiet:
        print("movie bitrate:\t\t" + str(bitrate))
        print("movie dimensions:\t\t" + str(snx) + 'x' + str(sny))
        print("use image files in:\t" + inputpath + id + "*" + postfix + "." + imtype)
        print("save movie to:\t\t" + outputpath + moviename + suffix)
    # command to run mencoder
    command = ["mencoder", "-really-quiet", shellquote("mf://"+inputpath+id+"*"+postfix+"."+imtype), "-mf",
               "w=" + str(nx) + ":h=" + str(ny) + ":fps="+str(fps)+":type="+str(imtype), "-ovc", "lavc",
               "-lavcopts", "vcodec="+str(codec)+":vqscale="+str(vqscale)+":mbd=2:vbitrate="+str(bitrate)+":trell",
               "-oac", "copy", "-vf", "scale="+str(snx)+":"+str(sny), "-o", shellquote(outputpath+moviename+suffix)]
    # print ' '.join(command)
    # ~ print command.
    # run mencoder
    os.system(' '.join(command))
    if tomp4:
        os.system('avconv -i ' + shellquote(outputpath + moviename + suffix) + ' -y -c:v libx264 ' +
                  shellquote(outputpath + moviename + '.mp4'))

def main():
    # get command-line arguments
    opt = parse_args()
    # check arguments
    if not opt.inputpath.endswith('/'):
        opt.inputpath += '/'
    if not opt.outputpath.endswith('/'):
        opt.outputpath += '/'
    makeMovie(opt.id, opt.imtype, opt.moviename, opt.inputpath, opt.outputpath, opt.fps, nx=opt.nx, ny=opt.ny,
              bitrate=opt.bitrate, scale=opt.scale, quiet=opt.quiet, win=opt.win, vqscale=opt.vqscale, tomp4=opt.mp4,
              postfix=opt.postfix)


if __name__ == "__main__":
    main()
