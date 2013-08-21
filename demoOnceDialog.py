'''
App that demonstrates OnceDialog

To reset license acceptance: delete ~/.config/OnceDialog/OnceDialog.conf
'''


from PySide.QtCore import *
from PySide.QtGui import *
import sys

from onceDialog.onceDialog import OnceDialog
# which also depends on existence of doc/license.py
        

class DiagramScene(QGraphicsScene):
    def __init__(self, *args):
        QGraphicsScene.__init__(self, *args)
        self.addSimpleText("OnceDialog demo: if you accept license, it won't show next time you start")


class DiagramView(QGraphicsView):
    def __init__(self, scene, *args):
        QGraphicsView.__init__(self, scene, *args)
        self.scene = scene
        
        
class MainWindow(QMainWindow):
  
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.scene = DiagramScene()
        self.view = DiagramView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)


    def showLicense(self):
      dialog = OnceDialog(parent=self)
      _ = dialog.show()
      # Ignoring result: allowing user to proceed even if rejected license


  
def createSettings(app):
      app.setOrganizationName("DemoOnceDialog")
      app.setOrganizationDomain("DemoOnceDialog.com")
      app.setApplicationName("DemoOnceDialog")
      
      
def main(args):
    app = QApplication(args)
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 500, 200)
    mainWindow.show()

    # Settings should exist before calling OnceDialog
    createSettings(app)
      
    # Timer to display license after app finishes starting
    QTimer.singleShot(0, mainWindow.showLicense)
    
    # Qt Main loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)