import maya.cmds as cmds
import maya.mel as mel
import time

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#----------------------------------------------------------------------------------------------------------------------
class Polygon(object):
    
#----------------------------------------------------------------------------------------------------------------------
    def __init__(self, path):
        self.path = path
        self.vtxs = []

        vtxsList = cmds.ls(cmds.polyListComponentConversion(path, tv = True), l = True, fl = True)
        for vtx in vtxsList:
            xFormRes = cmds.xform(vtx, q = True, ws = True, t = True)
            self.vtxs.append((xFormRes[0], xFormRes[1], xFormRes[2]))

#----------------------------------------------------------------------------------------------------------------------
    def printPolygon(self):
        print('\n')
        print('face -> "' + self.path + '"  ')
        for v in self.vtxs: print(v)

#----------------------------------------------------------------------------------------------------------------------
    def isEqualToPolygon(self, tPoly):
        if len(self.vtxs) != len (tPoly.vtxs): return False
        for sVtx in self.vtxs:
            if (not sVtx in tPoly.vtxs): return False
        return True

#    def isEqualToPolygon(self, tPoly):
#
#        if len(self.vtxs) != len (tPoly.vtxs): return False
#
#        tVtxs = tPoly.vtxs[:]
#        for sVtx in self.vtxs:
#            found = False
#            for tVtx in tVtxs:
#                if sVtx == tVtx:
#                    tVtxs.remove(tVtx)
#                    found = True
#                    break
#            if not found: return False
#        return True

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#----------------------------------------------------------------------------------------------------------------------
def checkSelection(selectedNodes):
    if len(selectedNodes) != 2: raise Exception("Select source and then target POLYGON objects.")
    if (
        not len( cmds.ls(selectedNodes[0], l = True, dag = True, ap = True, typ = "mesh") )  or
        not len( cmds.ls(selectedNodes[1], l = True, dag = True, ap = True, typ = "mesh") )
    ): raise Exception("Select 2 polygons objects.")

#----------------------------------------------------------------------------------------------------------------------
def run():

    start = time.clock()

    selectedNodes = cmds.ls(sl = True, l = True)
    checkSelection(selectedNodes)

    srcPolygons = cmds.ls(cmds.polyListComponentConversion(selectedNodes[0], tf = True), l = True, fl = True)
    tgtPolygons = cmds.ls(cmds.polyListComponentConversion(selectedNodes[1], tf = True), l = True, fl = True)

    sourcePolygons = [Polygon(poly) for poly in srcPolygons]
    targetPolygons = [Polygon(poly) for poly in tgtPolygons]

    polygonsToDelete = []

    for sPoly in sourcePolygons:
        for tPoly in targetPolygons:
            if sPoly.isEqualToPolygon(tPoly):
                polygonsToDelete.append(tPoly.path)
                break

    if not len(polygonsToDelete):
        cmds.select(selectedNodes[1])
        raise Exception("There is no same polygons in these 2 objects.")
    else:
        cmds.delete(polygonsToDelete)
        cmds.select(selectedNodes[1])

    print("time consumed: " + str(time.clock() - start))
