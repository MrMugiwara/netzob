# -*- coding: utf-8 -*-

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
#| Standard library imports
#+---------------------------------------------------------------------------+
from gettext import gettext as _
import os
import uuid

#+---------------------------------------------------------------------------+
#| Related third party imports
#+---------------------------------------------------------------------------+
from gi.repository import Gtk, Gdk
import gi
from netzob.Simulator.XDotWidget import XDotWidget
from netzob.Common.MMSTD.Dictionary.Variables.AggregateVariable import AggregateVariable
from netzob.Common.MMSTD.Dictionary.Variables.AlternateVariable import AlternateVariable
from netzob.Common.MMSTD.Dictionary.Variables.BinaryVariable import BinaryVariable
gi.require_version('Gtk', '3.0')
from gi.repository import GObject

#+---------------------------------------------------------------------------+
#| Local application imports
#+---------------------------------------------------------------------------+
from netzob.Common.ResourcesConfiguration import ResourcesConfiguration


class VariableDisplayerView(object):

    def __init__(self, controller):
        """Displays the symbol's variable tree"""
        self.controller = controller
        self.idAg = 0
        self.idAl = 0
        self.idBin = 0

    def run(self, panel):
        xdotWidget = XDotWidget()
        panel.add(xdotWidget)
        if self.controller.symbol is None:
            return
        # We retrieve all the fields and there associated variables
        fields = dict()
        for field in self.controller.symbol.getFields():
            var = field.getVariable()
            if var is None:
                var = field.getDefaultVariable(self.controller.symbol)
            fields["F{0}".format(field.getIndex())] = var

        dotCode = ["digraph G {"]
        dotCode.extend(self.addDotCodeForFields(fields))
        dotCode.append("}")

        xdotWidget.drawDotCode('\n'.join(dotCode))
        xdotWidget.show_all()

    def addDotCodeForFields(self, fields):
        dotCode = []

        labelName = []
        for fieldName in fields.keys():
            labelName.append("<{0}> {0}".format(fieldName))

        dotCode.append("\"root\" [shape = record, label=\"{0}\"];".format(' | '.join(labelName)))
        for fieldName in fields.keys():

            dotCode.append("subgraph cluster{0} {{".format(fieldName))
            dotCode.extend(self.addDotCodeForVariable(fields[fieldName]))
            dotCode.append("}")
            dotCode.append("\"root\":\"{0}\" -> \"{1}\"".format(fieldName, fields[fieldName].getID()))
        return dotCode

    def addDotCodeForVariable(self, variable):
        dotCode = []
        if variable.getTypeVariable() == AggregateVariable.TYPE:
            dotCode.extend(self.addAggregateVariable(variable))
        elif variable.getTypeVariable() == AlternateVariable.TYPE:
            dotCode.extend(self.addAlternateVariable(variable))
        elif variable.getTypeVariable() == BinaryVariable.TYPE:
            dotCode.extend(self.addBinaryVariable(variable))
        else:
            print variable
        return dotCode

    def addAggregateVariable(self, var):
        dotCode = []
        label = "Agg{0}".format(self.idAg)
        self.idAg += 1
        dotCode.append("\"{0}\" [style=filled, fillcolor = red, label=\"{1}\"];".format(var.getID(), label))
        for c in var.getChildren():
            dotCode.extend(self.addDotCodeForVariable(c))
            dotCode.append("\"{0}\" -> \"{1}\"".format(var.getID(), c.getID()))
        return dotCode

    def addAlternateVariable(self, var):
        dotCode = []
        label = "Alt{0}".format(self.idAl)
        self.idAl += 1
        dotCode.append("\"{0}\" [style=filled, fillcolor = yellow, label=\"{1}\"];".format(var.getID(), label))
        for c in var.getChildren():
            dotCode.extend(self.addDotCodeForVariable(c))
            dotCode.append("\"{0}\" -> \"{1}\"".format(var.getID(), c.getID()))
        return dotCode

    def addBinaryVariable(self, var):
        dotCode = []
        label = "Bin{0}".format(self.idBin)
        self.idBin += 1
        dotCode.append("\"{0}\" [style=filled, fillcolor = green, label=\"{1}\"];".format(var.getID(), label))
        return dotCode