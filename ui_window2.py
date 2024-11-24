from PySide2 import QtCore, QtGui, QtWidgets


class window2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
