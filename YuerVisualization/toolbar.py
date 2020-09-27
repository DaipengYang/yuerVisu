from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMenu, QToolBar, QWidgetAction, QToolButton
from funclibs import new_icon

def new_action(parent, text, slot=None, shortcut=None, icon=None, tip=None,
               checkable=False, enabled=True):
    action = QAction(text, parent)
    if icon is not None:
        action.setIcon(new_icon(icon))
        if shortcut is not None:
            if isinstance(shortcut, (list, tuple)):
                action.setShortcuts(shortcut)
            else:
                action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        action.setCheckable(checkable)
        action.setEnabled(enabled)
        return action

def add_actions(widget, actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif isinstance(action, QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)

class ActionDict(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ToolBar(QToolBar):
    def __init__(self, title):
        super(ToolBar, self).__init__(title)
        layout = self.layout()
        m = (0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setContentsMargins(*m)
        self.setContentsMargins(*m)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def addAction(self, action):
        if isinstance(action, QWidgetAction):
            return super(ToolBar, self).addAction(action)
        btn = QToolButton()
        btn.setDefaultAction(action)
        btn.setToolButtonStyle(self.toolButtonStyle())
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addWidget(btn)

