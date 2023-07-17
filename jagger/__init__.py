from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog
from jagger import globals
import logging
import sys


class Jagger:
    def __init__(self, argv: list):
        self.actions: dict[str, dict] = {}
        self.windows = {}
        self.argv = argv

    def view(self, view_name):
        def decorator(cls):
            view = self.actions.get(view_name)
            if view is None:
                self.actions[view_name] = {}
            
            self.actions[view_name]['view_class'] = cls
        return decorator
        
    def action(self, **params):
        def decorator(f):
            view_name = params.get('view_name')
            widget_name = params.get('widget_name')
            if view_name and widget_name:
                view = self.actions.get(view_name)
                if view:
                    view[widget_name] = f
                else:
                    raise KeyError(f'View "{view_name}" not found!')
        return decorator
    
    def setup(self):
        self.app = QApplication(self.argv)
        
        for view_name in self.actions:
            view = self.actions[view_name]
            view_class = view.pop('view_class', None)
            type = 'window'
            try:
                type = view_class.type
            except:
                pass
            
            if type == 'dialog':
                sup = QDialog

            elif type == 'window':
                sup = QMainWindow
                
            else:
                raise RuntimeError('Parent type not compatible')
                
            class Window(sup):
                def __init__(self):
                    super().__init__()
                    
                    if view_class is None:
                        raise Exception
                    self.view = view_class(main_window=self)
                        
                def get_widget(self, button_name):
                    button = getattr(self.view, button_name, None)
                    return button
                
            Window.__name__ = view_name
            window = Window()
            window.name = view_name
            
            for widget_name in view:
                callback = view[widget_name]
                widget = window.get_widget(widget_name)
                if widget:
                    logging.debug('widget found')
                    set_item_callback(widget, callback)
                else:
                    logging.warning('widget not found')
                    
            self.windows[view_name] = window


    def run(self, start):
        self.setup()
        window = self.windows.get(start)
        if not window:
            window = self.windows.get('/')
            if not window:
                logging.info('Selecting first window')
                window = list(self.windows.items())[0][1]

        else:
            logging.info('Setting startup window as "/"')
        
        globals.set_global_window_instance(window)
        self.run_window(window=window)
        sys.exit(self.app.exec())
        
    def run_window(self, window):
        form = {}
        logging.info(f"\n\n\nRunning window {window.name}")
        for widget_name, widget in window.view.__dict__.items():
            try:
                content = get_content(widget)
            except ValueError:
                continue
            else:
                logging.info(f"Widget {widget} is input widget")
                
                set_onchange(widget)
                form[widget_name] = content
        
        globals.set_global_app_instance(self)
        globals.set_global_form_instance(form)
        window.show()


def set_item_callback(item, callback):
    if isinstance(item, QtWidgets.QPushButton):
        item.clicked.connect(callback)
        
    elif isinstance(item, QtGui.QAction):
        item.triggered.connect(callback)
        
    elif isinstance(item, QtWidgets.QAbstractButton):
        item.clicked.connect(callback)

    else:
        raise ValueError(f"Unsupported item type: {type(item)}")


def open_window(view_name):
    app: Jagger = globals.current_app
    for windows_view_name in app.windows:
        if view_name == windows_view_name:
            windows = app.windows[view_name]
            windows.show()


def redirect(view_name):
    app: Jagger = globals.current_app
    for windows_view_name in app.windows:
        if view_name == windows_view_name:
            window = app.windows[view_name]
            app.run_window(window)
            globals.current_window.close()
            globals.set_global_window_instance(window=window)


def get_content(input_widget):
    if isinstance(input_widget, QtWidgets.QTextEdit):
        return input_widget.toPlainText()
        
    elif isinstance(input_widget, QtWidgets.QLineEdit):
        return input_widget.text()
        
    elif isinstance(input_widget, QtGui.QFont):
        return {
            'family': input_widget.family(),
            'size': input_widget.pointSize()
        }
        
    elif isinstance(input_widget, QtWidgets.QTimeEdit):
        return input_widget.time().toPython()
        
    elif isinstance(input_widget, QtWidgets.QDoubleSpinBox):
        return input_widget.value()
        
    elif isinstance(input_widget, QtWidgets.QSpinBox):
        return input_widget.value()

    elif isinstance(input_widget, QtWidgets.QComboBox):
        return input_widget.currentText()
        
    elif isinstance(input_widget, QtWidgets.QCheckBox):
        return input_widget.isChecked()
        
    elif isinstance(input_widget, QtWidgets.QRadioButton):
        if input_widget.isChecked():
            return input_widget.text()
        else:
            return None  # Radio button is not checked
        
    elif isinstance(input_widget, QtWidgets.QDateEdit):
        return input_widget.date().toPython()
        
    elif isinstance(input_widget, QtWidgets.QSlider):
        return input_widget.value()

    elif isinstance(input_widget, QtWidgets.QProgressBar):
        return input_widget.value()

    elif isinstance(input_widget, QtWidgets.QCalendarWidget):
        return input_widget.selectedDate().toPython()

    elif isinstance(input_widget, QtWidgets.QSpinBox):
        return input_widget.value()

    elif isinstance(input_widget, QtWidgets.QDial):
        return input_widget.value()

    elif isinstance(input_widget, QtWidgets.QDateTimeEdit):
        return input_widget.dateTime().toPython()

    elif isinstance(input_widget, QtWidgets.QScrollBar):
        return input_widget.value()

    # Add more cases for other widget types if needed

    else:
        raise ValueError(f"Unsupported widget type: {type(input_widget)}")


def update_form(input_widget):
    current_form = globals.get_global_form_instance()
    value = get_content(input_widget)
    widget_name = input_widget.objectName()
    current_form[widget_name] = value
    globals.set_global_form_instance(current_form)


def set_onchange(input_widget):
    
    update = lambda: update_form(input_widget)
    
    if isinstance(input_widget, QtWidgets.QTextEdit):
        input_widget.textChanged.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QLineEdit):
        input_widget.textChanged.connect(update)
        
    elif isinstance(input_widget, QtGui.QFont):
        input_widget.fontChanged.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QTimeEdit):
        input_widget.timeChanged.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QDoubleSpinBox):
        input_widget.valueChanged.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QSpinBox):
        input_widget.valueChanged.connect(update)

    elif isinstance(input_widget, QtWidgets.QComboBox):
        input_widget.currentIndexChanged.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QCheckBox):
        input_widget.stateChanged.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QRadioButton):
        input_widget.toggled.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QDateEdit):
        input_widget.dateChanged.connect(update)
        
    elif isinstance(input_widget, QtWidgets.QSlider):
        input_widget.valueChanged.connect(update)

    elif isinstance(input_widget, QtWidgets.QProgressBar):
        input_widget.valueChanged.connect(update)

    elif isinstance(input_widget, QtWidgets.QCalendarWidget):
        input_widget.selectionChanged.connect(update)

    elif isinstance(input_widget, QtWidgets.QSpinBox):
        input_widget.valueChanged.connect(update)

    elif isinstance(input_widget, QtWidgets.QDial):
        input_widget.valueChanged.connect(update)

    elif isinstance(input_widget, QtWidgets.QDateTimeEdit):
        input_widget.dateTimeChanged.connect(update)

    elif isinstance(input_widget, QtWidgets.QScrollBar):
        input_widget.valueChanged.connect(update)
        

    else:
        raise ValueError(f"Unsupported widget type: {type(input_widget)}")
