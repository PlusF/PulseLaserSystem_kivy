from kivy.app import App
from kivy.uix.widget import Widget


class MainWindow(Widget):
    pass


class MainApp(App):
    def build(self):
        window = MainWindow()
        return window


if __name__ == '__main__':
    MainApp().run()
