'''
Copyright 2013 Lloyd K. Konneker

Licensed under the LGPLv3+
'''

from string import Template

from PySide.QtCore import QSettings
from PySide.QtGui import QDialog, QGridLayout, QDialogButtonBox, QPlainTextEdit

# !!! provide default text
from doc.license import LICENSE_TEXT, LICENSE_TEMPLATE_MAP




class OnceDialog(QDialog):
  '''
  A dialog that shows a scrolling, large text (e.g. license).
  When invoked, it only shows if user has never accepted dialog.
  In other words, one acceptance over all sessions with app since installation.
  
  Typically called at app startup.
  Typically used for, and defaults to, licensing.
  
  Implementation
  ==============
  
  After installation, settings should not exist.
  On first run of program, create settings (but not 'flag' setting, or with value False)
  and then call this dialog.
  Typically your main starts a one shot timer that triggers this dialog after the event loop starts.
  If you do not want user to continue after rejecting this dialog,
  check the result of show() and exit if False.
  
  On subsequent runs, if user accepted on a previous run, then settings exist and 'flag' setting exists with value True,
  and dialog will not be shown.
  
  On subsequent runs if user rejected, settings exist but 'flag' setting not exists,
  and dialog will be shown again.
  Again, user will still be able to use your software unless you exit on show() is False.
  
  For use in licensing
  ====================
  
  Upgrade of app installation should also clear 'flag' setting
  if you expect user to renew their license.
  
  User must accept license after every installation on other computers owned by licensee.
  (Obviously not a networked license server.)
  
  User can subvert licensing by copying settings from ~/.config/...
  '''
  
  
  
  def __init__(self, parent, 
               template=LICENSE_TEXT, 
               templateMap = LICENSE_TEMPLATE_MAP,
               titleText='License', 
               flagSettingName='acceptedLicense'):
    '''
    '''
    super(OnceDialog, self).__init__(parent)
    self.template = template
    self.templateMap = templateMap
    self.titleText = titleText
    self.flagSettingName = flagSettingName
    
    self.scrollingText = QPlainTextEdit(self.filledTemplatedText(), parent=self)
    
    # buttons
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    
    # One scrolling text widget
    layout = QGridLayout()
    layout.addWidget(self.scrollingText)
    
    layout.addWidget(buttonBox)
    self.setLayout(layout)
    self.setWindowTitle(self.tr(self.titleText))
    
    # connections
    buttonBox.accepted.connect(self.accept)
    buttonBox.rejected.connect(self.reject)
  
    self.setGeometry(0, 0, 600, 480)
    

  def filledTemplatedText(self):
    '''
    Fill dialog's template.
    '''
    template = Template(self.template)
    return template.substitute(self.templateMap)
    
    
  def accept(self):
    " User accepts. Raise accepted flag in settings. "
    settings = QSettings()
    settings.setValue(self.flagSettingName, True)
    QDialog.accept(self)  # super close dialog
 
 
  def reject(self):
    " User rejects.  Omit raise accepted flag in settings. "
    QDialog.reject(self)  # super close dialog
    
    
  def show(self):
    '''
    Show unless flag setting exists in settings and its value is True.
    
    Return whether user has accepted license.
    '''
    settings = QSettings()
    # Here False is the default if setting not exist.
    if not settings.value(self.flagSettingName, False):
      # Show synchronously, i.e. modal
      result = self.exec_()
    else:
      # user has already accepted license
      result = True
    return result
