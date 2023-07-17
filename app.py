from jagger import Jagger, open_window, redirect
import views
from jagger.globals import current_form
import sys
from PySide6.QtWidgets import QDialog


app = Jagger(sys.argv)


@app.view(view_name='/')
class HomeView(views.home.Ui_MainWindow):
    type = 'window'
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(main_window)


@app.action(view_name='/', widget_name='pushButton')
def hello():
    redirect(view_name='/second')


@app.view(view_name='/second')
class SecondView(views.second.Ui_MainWindow):
    type = 'window'
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(main_window)


@app.action(view_name='/second', widget_name='actionCriarBanco')
def ola():
    open_window(view_name='/second/criar_banco')


@app.view(view_name='/second/criar_banco')
class BDView(QDialog, views.bd.Ui_MainWindow):
    type = 'window'
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.setupUi(self.main_window)


@app.action(view_name='/second/criar_banco', widget_name='pushButton')
def get_path():
    form = current_form
    print(form)


if __name__ == '__main__':
    app.run(start='/')
