#-*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| File contributors :                                                       |
#|       - Georges Bossert <georges.bossert (a) supelec.fr>                  |
#|       - Frédéric Guihéry <frederic.guihery (a) amossys.fr>                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports                                                  |
#+---------------------------------------------------------------------------+
from bitarray import bitarray

#+---------------------------------------------------------------------------+
#| Related third party imports                                               |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Local application imports                                                 |
#+---------------------------------------------------------------------------+
from netzob.Common.Utils.Decorators import typeCheck, NetzobLogger
from netzob.Inference.Vocabulary.Search.SearchTask import SearchTask


class SearchResults(list):

    def __str__(self):
        return "{0} occurence(s) found.".format(len(self))


@NetzobLogger
class SearchResult(object):
    """A Search result describes a found match between a specific SearchTask
    and a target. It describes at which position and why the search task matches
    the target.

    >>> from netzob.all import *
    >>> from netzob.Inference.Vocabulary.Search.SearchTask import SearchTask
    >>> target = TypeConverter.convert("Hello world, that is just a test of netzob.", Raw, BitArray)
    >>> searchTask = SearchTask(TypeConverter.convert("o", Raw, BitArray), "letter-o-original")
    >>> ranges = [(4,5), (7,8), (33,34), (40,41)]
    >>> sr = SearchResult(target, searchTask, ranges)
    >>> print sr.ranges
    [(4, 5), (7, 8), (33, 34), (40, 41)]
    >>> print sr.target
    bitarray('00010010101001100011011000110110111101100000010011101110111101100100111000110110001001100011010000000100001011100001011010000110001011100000010010010110110011100000010001010110101011101100111000101110000001001000011000000100001011101010011011001110001011100000010011110110011001100000010001110110101001100010111001011110111101100100011001110100')
    >>> print sr.searchTask.description
    letter-o-original

    """

    def __init__(self, target, searchTask, ranges):
        self.target = target
        self.searchTask = searchTask
        self.ranges = ranges

    @property
    def target(self):
        return self.__target

    @target.setter
    @typeCheck(bitarray)
    def target(self, target):
        if target is None:
            raise TypeError("Target bitarray cannot be None")
        self.__target = target

    @property
    def searchTask(self):
        return self.__searchTask

    @searchTask.setter
    @typeCheck(SearchTask)
    def searchTask(self, searchTask):
        if searchTask is None:
            raise TypeError("Search task cannot be None")
        self.__searchTask = searchTask

    @property
    def ranges(self):
        return self.__ranges

    @ranges.setter
    @typeCheck(list)
    def ranges(self, ranges):
        if ranges is None:
            raise TypeError("Ranges cannot be None")

        for (start, end) in ranges:
            if not isinstance(start, (int, long)) or not isinstance(end, (int, long)) or end <= start:
                raise TypeError("Start and end range must be integers and end > start (start={0}, end={1})".format(start, end))
        self.__ranges = ranges