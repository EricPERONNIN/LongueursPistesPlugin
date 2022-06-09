import pcbnew
import os
import wx

from pcbnew import *
class LongueurPistesPluginAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Mesurer la longeurs de tous les nets et de la piste sélectionnée"
        self.category = "Mesure"
        self.description = "Mesure la longueur de tous les nets du circuit imprimé et de la piste sélectionnée"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        carte = GetBoard()
        pistes = carte.GetTracks()
        nbSegmentsSelection = 0
        longueurSelection = 0
        longueurParNet = dict()
        nbSegmentsParNet = dict()
        longueurTotale = 0

        for piste in pistes:
            #wx.MessageBox(piste.GetNetname(), 'Nom de la piste', wx.OK | wx.ICON_INFORMATION)
            if piste.GetNetname() in longueurParNet:
                longueurParNet[piste.GetNetname()] = longueurParNet[piste.GetNetname()] + piste.GetLength()/1000000
                nbSegmentsParNet[piste.GetNetname()] = nbSegmentsParNet[piste.GetNetname()] + 1
            else:
                longueurParNet[piste.GetNetname()] = piste.GetLength()/1000000
                nbSegmentsParNet[piste.GetNetname()] = 1
            if piste.IsSelected():
                longueurSelection = longueurSelection + piste.GetLength()/1000000
                nbSegmentsSelection = nbSegmentsSelection + 1
        bilan = ''
        for net in longueurParNet:
            longueurTotale = longueurTotale + longueurParNet[net]
            #bilan = bilan + 'Longueur de l\'équipotentielle ' + net + ' : ' + str(longueurParNet[net]) + ' mm en ' + str(nbSegmentsParNet[net]) + ' segment(s).\n'
            bilan = bilan + 'Longueur de l\'équipotentielle ' + net + ' : {0:4.3f}'.format(longueurParNet[net]) + ' mm en ' + str(nbSegmentsParNet[net]) + ' segment(s).\n'
        if nbSegmentsSelection > 0:
            bilan = bilan + '\nLongueur de piste(s) sélectionnée(s) : {0:4.3f}'.format(longueurSelection) + ' mm en ' + str(nbSegmentsSelection) + ' segment(s).\n'
        bilan = bilan + '\nLongueur totale de pistes : {0:4.3f}'.format(longueurTotale) + 'mm'
        bilan = bilan + '\n\nRemarque : la méthode de mesure proposée exploite le centre des segments de pistes et ne constitue pas une mesure du chemin le plus court.'
        wx.MessageBox(bilan, 'Mesure des longueurs de pistes', wx.OK | wx.ICON_INFORMATION)
        
#LongueurPistesPluginAction().register()