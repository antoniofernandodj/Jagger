import typing as t
from werkzeug.local import LocalProxy
from PySide6.QtWidgets import QApplication
from contextvars import ContextVar
import typing as t


T = t.TypeVar("T")


class AnonymousUser: ...
au = AnonymousUser()
au.id = None


_cv_app: ContextVar[QApplication] = ContextVar("pyside6.app_ctx")
_cv_usr: ContextVar[QApplication] = ContextVar("pyside6.login_ctx")
_cv_form: ContextVar[QApplication] = ContextVar("pyside6.form_ctx")
_cv_wnd: ContextVar[QApplication] = ContextVar("pyside6.form_ctx")


def get_global_app_instance() -> QApplication:
    global _global_app_instance
    if _global_app_instance is None:
        raise RuntimeError("QApplication instance not set. Call `set_global_app_instance()` first.")
    return _global_app_instance

def set_global_app_instance(app: QApplication) -> None:
    global _global_app_instance
    _global_app_instance = app
    _cv_app.set(app)

def clear_global_app_instance() -> None:
    global _global_app_instance
    _global_app_instance = None
    _cv_app.set(None)



def get_global_user_instance() -> T:
    global _global_user_instance
    return _global_user_instance

def set_global_user_instance(user: t.Any) -> T:
    global _global_user_instance
    _global_user_instance = user
    _cv_usr.set(user)

def clear_global_user_instance() -> None:
    global _global_user_instance
    _global_user_instance = None
    _cv_usr.set(None)



def get_global_form_instance() -> T:
    global _global_form_instance
    return _global_form_instance

def set_global_form_instance(form: t.Any) -> T:
    global _global_form_instance
    _global_form_instance = form
    _cv_usr.set(form)

def clear_global_form_instance() -> None:
    global _global_form_instance
    _global_form_instance = None
    _cv_form.set(None)




def get_global_window_instance() -> T:
    global _global_window_instance
    return _global_window_instance

def set_global_window_instance(window: t.Any) -> T:
    global _global_window_instance
    _global_window_instance = window
    _cv_wnd.set(window)

def clear_global_window_instance() -> None:
    global _global_window_instance
    _global_window_instance = None
    _cv_wnd.set(None)



class QTLocalProxy(LocalProxy):

    def __init__(self, local: ContextVar[T], unbound_message: str) -> None:

        if local is _cv_app:
            def _get_current_object() -> T:
                app_instance = get_global_app_instance()
                if app_instance is None:
                    raise RuntimeError(unbound_message)
                return app_instance
            
        elif local is _cv_form:
            def _get_current_object() -> T:
                form_instance = get_global_form_instance()
                if form_instance is None:
                    raise RuntimeError(unbound_message)
                return form_instance
            
        elif local is _cv_usr:
            def _get_current_object() -> T:
                user_instance = get_global_user_instance()
                if user_instance is None:
                    raise RuntimeError(unbound_message)
                return user_instance
            
        elif local is _cv_wnd:
            def _get_current_object() -> T:
                window_instance = get_global_window_instance()
                if window_instance is None:
                    raise RuntimeError(unbound_message)
                return window_instance
            

        object.__setattr__(self, "_LocalProxy__wrapped", local)
        object.__setattr__(self, "_get_current_object", _get_current_object)


_global_app_instance: t.Optional[QApplication] = None
_global_window_instance: t.Optional[QApplication] = None
_global_user_instance: t.Optional[QApplication] = au
_global_form_instance: t.Optional[QApplication] = {}


current_app = QTLocalProxy(_cv_app, 'Objeto não vinculado')
current_user = QTLocalProxy(_cv_usr, 'Objeto não vinculado')
current_form = QTLocalProxy(_cv_form, 'Objeto não vinculado')
current_window = QTLocalProxy(_cv_wnd, 'Objeto não vinculado')