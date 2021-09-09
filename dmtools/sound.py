import numpy as np
from scipy.io import wavfile

# https://en.wikipedia.org/wiki/44,100_Hz
SAMPLE_RATE = 44100


class WAV:
    """An object representing a WAV audio file.

    For more information about the audio file format, see
    `WAV <https://en.wikipedia.org/wiki/WAV>`_
    """
    def __init__(self, r: np.ndarray, l: np.ndarray,
                 sample_rate: int = SAMPLE_RATE):
        """Initialize a WAV sound.

        Args:
            r (np.ndarray): NumPy array of samples of the right channel.
            l (np.ndarray): NumPy array of samples of the left channel.
            sample_rate (int): Sample rate. Defaults to SAMPLE_RATE.
        """
        self.r = r
        self.l = l
        self.sample_rate = sample_rate

    def to_wav(self, path):
        """Write object to a WAV audio file (wav)

        Args:
            path (str): String file path.
        """
        wavfile.write(path, self.sample_rate, np.array([self.r, self.l]).T)


def wave(f: float, a: float, t: float) -> np.ndarray:
    """Generate the samples of a sound wave.

    Args:
        f (float): Frequency of the sound wave.
        a (float): Amplitude of the sound wave.
        t (float): Duration (seconds) of the sound wave.

    Returns:
        np.ndarray: NumPy array with sample points of wave.
    """
    sample_points = np.linspace(0, t*(2*np.pi), int(t*SAMPLE_RATE))
    return a*np.sin(sample_points*f)


def wave_sequence(frequencies: np.ndarray, t) -> WAV:
    """Return a Wav sound which iterates through the given frequencies.

    Args:
        frequencies (np.ndarray): frequencies to iterate through.
        t ([type]): duration of iteration.

    Returns:
        WAV: Wav file.
    """
    d = t / len(frequencies)
    w = np.array([list(wave(f,1,d)) for f in frequencies]).flatten()
    return WAV(r=w, l=w)
