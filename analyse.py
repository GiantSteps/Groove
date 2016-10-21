#!/usr/bin/env python

# Copyright (C) 2006-2016  Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Essentia
#
# Essentia is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the Affero GNU General Public License
# version 3 along with this program. If not, see http://www.gnu.org/licenses/



from essentia import *
from essentia.standard import *

import numpy as np
import matplotlib.pyplot as plt

def nearestNeighbour(targetValue, vector):
    minIndex = 0
    minDiff = targetValue - vector[0]
    minAbsDiff = abs(minDiff)

    for index, value in enumerate(vector):
        diff = targetValue - value
        absDiff = abs(diff)
        if absDiff < minAbsDiff:
            minIndex = index
            minDiff = diff
            minAbsDiff = absDiff

    return minIndex, minDiff


def extractor(filename):
    # load our audio into an array
    audio = MonoLoader(filename = filename)()

    # get onsets
    onsetRateExtractor = OnsetRate()
    onsets, onsetRate = onsetRateExtractor(audio)

    # get duration
    durationExtractor = Duration()
    dur = durationExtractor(audio)

    # Our metronome 16ths
    idealSixteenths = np.linspace(0, dur, 17)

    #Time deviations
    devs = []

    for onset in onsets:
        devs.append(nearestNeighbour(onset, idealSixteenths))

    print devs

    # Plot

    plt.plot(audio)        

    for loc in idealSixteenths:
        posInSamples = loc * 44100
        plt.axvline(x=posInSamples, color='r')

    for onset in onsets:
        posInSamples = onset * 44100
        plt.axvline(x=posInSamples, color='g')                

    plt.show()


# some python magic so that this file works as a script as well as a module
# if you do not understand what that means, you don't need to care
if __name__ == '__main__':
    import sys
    print 'Script %s called with arguments: %s' % (sys.argv[0], sys.argv[1:])

    try:
        extractor(sys.argv[1])
        print 'Success!'

    except KeyError:
        print 'ERROR: You need to call this script with a filename argument...'