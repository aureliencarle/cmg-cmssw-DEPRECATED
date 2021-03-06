from PhysicsTools.Heppy.physicsobjects.Lepton import Lepton
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
import math

# Find all tau IDs here: 
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#Tau_ID_2014_preparation_for_AN1
# and the names by which they are accessible with tau.tauId(...) here
# http://cmslxr.fnal.gov/lxr/source/PhysicsTools/PatAlgos/python/producersLayer1/tauProducer_cfi.py

class Tau(Lepton):
    
    def __init__(self, tau):
        self.tau = tau
        super(Tau, self).__init__(tau)
        
    def relIso(self, dummy1, dummy2):
        '''Just making the tau behave as a lepton.'''
        return -1

    def mvaId(self):
        '''For a transparent treatment of electrons, muons and taus. Returns -99'''
        return -99

    def dxy(self, vertex=None):
        '''FIXME: Being checked with tau POG'''
        if vertex is None:
            vertex = self.associatedVertex
        vtx = self.leadChargedHadrCand().vertex()
        p4 = self.p4()
        return ( - (vtx.x()-vertex.position().x()) *  p4.y()
                 + (vtx.y()-vertex.position().y()) *  p4.x() ) /  p4.pt()

    def dxy_pog(self, vertex=None):
        '''More precise dxy calculation as pre-calculated in the tau object
        for the primary vertex it was constructed with.
        Returns standard dxy calculation if the passed vertex differs from the
        one in the tau object.
        '''
        if vertex is None:
            vertex = self.associatedVertex
        # Why are x/y/z saved in the tau object instead of a reference to the
        # PV?
        if vertex.x() == self.vertex().x():
            return self.physObj.dxy()
        else:
            return self.dxy(vertex)


    def dz(self, vertex=None):
        '''FIXME: Being checked with tau POG'''
        if vertex is None:
            vertex = self.associatedVertex
        vtx = self.leadChargedHadrCand().vertex()
        p4 = self.p4()
        return  (vtx.z()-vertex.position().z()) - ((vtx.x()-vertex.position().x())*p4.x()+(vtx.y()-vertex.position().y())*p4.y())/ p4.pt() *  p4.z()/ p4.pt()
    
    def zImpact(self, vertex=None):
        '''z impact at ECAL surface'''
        if vertex is None:
            vertex = self.associatedVertex
        return vertex.z() + 130./math.tan(self.theta())

    def __str__(self):
        lep = super(Tau, self).__str__()
        spec = '\t\tTau: decay = {decMode:<15}'.format(
            decMode = tauDecayModes.intToName(self.decayMode())
        )
        return '\n'.join([lep, spec])


def isTau(leg):
    '''Duck-typing a tau'''
    try:
        # Method independently implemented in pat tau and PF tau
        leg.leadPFChargedHadrCandsignedSipt()
    except AttributeError:
        return False
    return True

