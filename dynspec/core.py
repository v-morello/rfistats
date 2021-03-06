from __future__ import print_function
import numpy
from numpy import log2

def num_block_samples(tblock, tsamp):
    """ Determine the number of samples in a block, making sure it is a power
    of two. """
    n = int(tblock / tsamp)

    # Round down to lower power-of-two
    n = 2 ** int(log2(n))
    return n


def dynamic_spectrum(data, tsamp, tblock=10.0, tskip=0.0):
    # Ignore start of the file
    nskip = int(tskip / tsamp)
    data = data[nskip:]
    print("Skipping {:d} samples at the beginning of the observation".format(nskip))

    # Determine block size. Each blocks gets FFT'ed independently
    tobs = data.size * tsamp
    bsamp = num_block_samples(min(tobs, tblock), tsamp)
    nblocks = data.size // bsamp

    nsamp_eff = nblocks * bsamp
    tblock_eff = bsamp * tsamp
    print("Cutting data ({0:d} samples) into {1:d} blocks of {2:d} samples, tblock = {3:.6f} s".format(data.size, nblocks, bsamp, tblock_eff))

    data = data[:nsamp_eff].reshape(nblocks, bsamp)
    ft = numpy.fft.rfft(data)

    # Center times of every block
    times = numpy.arange(nblocks) * tblock_eff + 0.5 * tblock_eff + nskip * tsamp

    # Frequencies of every Fourier bin
    freqs = numpy.fft.rfftfreq(bsamp, tsamp)
    return times, freqs, ft
