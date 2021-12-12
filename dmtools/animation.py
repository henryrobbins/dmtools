import imageio
import numpy as np
from math import ceil
from typing import List
import logging
from .io import read, _discretize
from . import sound
from ._log import _log_msg
import os


def clip(path: str, start: int = 0, end: int = -1) -> List[np.ndarray]:
    """Return a list of images in the given directory.

    Images are ordered according to their name. Hence, the following naming
    convention is recommend.

    name0000.png, name0001.png, ...

    Args:
        path (str): String directory path.
        start (int, optional): Starting frame. Defaults to 0.
        end (int, optional): Ending frame. Defaults to -1.

    Returns:
        List[np.ndarray]: List of NumPy arrays representing images.
    """
    def listdir_nohidden(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                yield f

    files = sorted(listdir_nohidden(path))
    files = files[start:end]
    paths = ["%s/%s" % (path, f) for f in files]
    frames = [read(path) for path in paths]
    return frames


def _pad_to_16(M: np.ndarray) -> np.ndarray:
    # TODO: Get a better understanding why image demensions need to be
    # multiplies of 16. It appears this requirement is no longer from ffmpeg.
    # Adapted from code by: https://stackoverflow.com/users/9698684/yatu
    m,n,*_ = M.shape
    y_pad = (ceil(m/16)*16-m)
    y_pad_split = (y_pad // 2, y_pad // 2 + y_pad % 2)
    x_pad = (ceil(n/16)*16-n)
    x_pad_split = (x_pad // 2, x_pad // 2 + x_pad % 2)
    if len(M.shape) == 3:
        return np.pad(M, (y_pad_split, x_pad_split, (0, 0)))
    else:
        return np.pad(M, (y_pad_split, x_pad_split))


def to_mp4(frames: List[np.ndarray], path: str, fps: int, s: int = 1,
           audio: sound.WAV = None):
    """Write an animation as a .mp4 file using ffmpeg through imageio.mp4

    Args:
        frames (List[np.ndarray]): List of frames in the animation.
        audio (sound.WAV): Audio for the animation (None if no audio).
        path (str): String file path.
        fps (int): Frames per second.
        s (int, optional): Multiplier for scaling. Defaults to 1.
    """
    frames = [_discretize(f, 255).astype(np.uint8) for f in frames]
    frames = [_pad_to_16(f) for f in frames]
    imageio.mimwrite(uri="tmp.mp4" if audio is not None else path,
                     ims=frames,
                     format='FFMPEG',
                     fps=fps,
                     output_params=["-vf", "scale=iw*%d:ih*%d" % (s, s),
                                    "-sws_flags", "neighbor"])
    if audio is not None:
        audio.to_wav("tmp.wav")
        os.system("ffmpeg -i %s -i %s -c:v copy -c:a aac -y %s"
                  % ("tmp.mp4", "tmp.wav", path))
        os.system("rm tmp.mp4")
        os.system("rm tmp.wav")
    name = path.split('/')[-1]
    logging.info(_log_msg(name, os.stat(path).st_size))
