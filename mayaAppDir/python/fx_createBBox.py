import maya.cmds as m
import pymel.core as pm

from watch import *

SCRIPT_NAME = 'FX Create Box'
WIN_NAME = 'fx_createBBoxWin'

MAIN_BUTTONS_HEIGHT = 30

BBOX_NAME = 'bbox'

ui = None

faceMapping = {
    'xPos': '.f[4]',
    'xNeg': '.f[5]',
    'yPos': '.f[1]',
    'yNeg': '.f[3]',
    'zPos': '.f[0]',
    'zNeg': '.f[2]',
}


#noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class CreateBBoxUI(object):
    def __init__(self):
        self.uiCreate()

    def uiCreate(self):

        self.uiClose()

        self.window = pm.window(
            WIN_NAME,
            title=SCRIPT_NAME,
            maximizeButton=False
        )

        with self.window:
            with pm.formLayout() as ui_LAY_mainForm:
                with pm.scrollLayout(childResizable=True) as ui_LAY_mainScroll:
                    with pm.frameLayout(
                            label='Parameters',
                            collapsable=True,
                            marginHeight=3,
                            borderStyle='etchedIn',
                            borderVisible=True,
                            collapse=False
                    ):
                        with pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2)):
                            self.ui_FLTFLDGRP_xPos = pm.floatFieldGrp(numberOfFields=1, label='+X', precision=6)
                            self.ui_FLTFLDGRP_xNeg = pm.floatFieldGrp(numberOfFields=1, label='-X', precision=6)
                            self.ui_FLTFLDGRP_yPos = pm.floatFieldGrp(numberOfFields=1, label='+Y', precision=6)
                            self.ui_FLTFLDGRP_yNeg = pm.floatFieldGrp(numberOfFields=1, label='-Y', precision=6)
                            self.ui_FLTFLDGRP_zPos = pm.floatFieldGrp(numberOfFields=1, label='+Z', precision=6)
                            self.ui_FLTFLDGRP_zNeg = pm.floatFieldGrp(numberOfFields=1, label='-Z', precision=6)

                            pm.separator(style='none', height=5)

                self.ui_BTN_create = pm.button(
                    label='Create',
                    height=MAIN_BUTTONS_HEIGHT,
                    command=self.ui_on_BTN_create_clicked
                )

                self.ui_BTN_close = pm.button(
                    label='Close',
                    height=MAIN_BUTTONS_HEIGHT,
                    command=self.uiClose
                )

                ui_LAY_mainForm.attachForm(ui_LAY_mainScroll, 'top', 2)
                ui_LAY_mainForm.attachForm(ui_LAY_mainScroll, 'left', 2)
                ui_LAY_mainForm.attachForm(ui_LAY_mainScroll, 'right', 2)
                ui_LAY_mainForm.attachControl(ui_LAY_mainScroll, 'bottom', 2, self.ui_BTN_create)

                ui_LAY_mainForm.attachNone(self.ui_BTN_create, 'top')
                ui_LAY_mainForm.attachForm(self.ui_BTN_create, 'left', 2)
                ui_LAY_mainForm.attachPosition(self.ui_BTN_create, 'right', 2, 50)
                ui_LAY_mainForm.attachForm(self.ui_BTN_create, 'bottom', 2)

                ui_LAY_mainForm.attachNone(self.ui_BTN_close, 'top')
                ui_LAY_mainForm.attachPosition(self.ui_BTN_close, 'left', 2, 50)
                ui_LAY_mainForm.attachForm(self.ui_BTN_close, 'right', 2)
                ui_LAY_mainForm.attachForm(self.ui_BTN_close, 'bottom', 2)

        self.setupInitialValues()

    def setupInitialValues(self):
        self.ui_FLTFLDGRP_xPos.setValue1(1)
        self.ui_FLTFLDGRP_xNeg.setValue1(-1)
        self.ui_FLTFLDGRP_yPos.setValue1(1)
        self.ui_FLTFLDGRP_yNeg.setValue1(-1)
        self.ui_FLTFLDGRP_zPos.setValue1(1)
        self.ui_FLTFLDGRP_zNeg.setValue1(-1)

    #noinspection PyUnusedLocal
    def ui_on_BTN_create_clicked(self, *args):
        cube = m.polyCube(ch=False)[0]

        xPosUI = self.ui_FLTFLDGRP_xPos.getValue()[0]
        xNegUI = self.ui_FLTFLDGRP_xNeg.getValue()[0]
        yPosUI = self.ui_FLTFLDGRP_yPos.getValue()[0]
        yNegUI = self.ui_FLTFLDGRP_yNeg.getValue()[0]
        zPosUI = self.ui_FLTFLDGRP_zPos.getValue()[0]
        zNegUI = self.ui_FLTFLDGRP_zNeg.getValue()[0]

        xPos = max(xPosUI, xNegUI)
        xNeg = min(xPosUI, xNegUI)
        yPos = max(yPosUI, yNegUI)
        yNeg = min(yPosUI, yNegUI)
        zPos = max(zPosUI, zNegUI)
        zNeg = min(zPosUI, zNegUI)

        m.move(xPos, cube + faceMapping['xPos'], worldSpaceDistance=True, x=True)
        m.move(xNeg, cube + faceMapping['xNeg'], worldSpaceDistance=True, x=True)
        m.move(yPos, cube + faceMapping['yPos'], worldSpaceDistance=True, y=True)
        m.move(yNeg, cube + faceMapping['yNeg'], worldSpaceDistance=True, y=True)
        m.move(zPos, cube + faceMapping['zPos'], worldSpaceDistance=True, z=True)
        m.move(zNeg, cube + faceMapping['zNeg'], worldSpaceDistance=True, z=True)

        m.xform(cube, cp=True)
        m.rename(cube, BBOX_NAME)

    #noinspection PyUnusedLocal
    def uiClose(self, *args):
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)


def run():
    CreateBBoxUI()
