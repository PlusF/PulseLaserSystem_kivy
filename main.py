from kivy.app import App
from kivy.base import ExceptionManager, ExceptionHandler
from kivy.core.window import Clock, Window
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from ConfigLoader import ConfigLoader
from PulseLaserController import PulseLaserController
from ZaberController import ZaberController


class CrashHandler(ExceptionHandler):
    def handle_exception(self, inst):
        print(inst)
        return ExceptionManager.PASS


class MainWindow(BoxLayout):
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    delta_x = NumericProperty(100)
    delta_y = NumericProperty(50)
    Window.size = (350, 700)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_request_close=self.quit)

        self.cl = ConfigLoader('./config.json')

        self.freq: int = 16
        self.vel: float = 1.0

        self.laser = PulseLaserController(self.cl)
        self.stage = ZaberController(self.cl)

        self.move_funcs = {
            'x': {
                '+': self.stage.move_right,
                '-': self.stage.move_left
            },
            'y': {
                '+': self.stage.move_top,
                '-': self.stage.move_bottom
            }
        }

        Clock.schedule_interval(self.update_position, 0.1)  # 0.1秒ごとに位置を更新．

    def update_position(self, dt):
        self.pos_x, self.pos_y = self.stage.get_position_all()

    def move(self, axis: str, direction: str):
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        move_func = self.move_funcs[axis][direction]

        if auto_on:
            self.emit_laser()
        move_func(self.vel)

    def stop_moving(self):
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        if auto_on:
            self.stop_laser()
        self.stage.stop_all()

    def emit_laser(self):
        ok = self.laser.emit(self.freq)
        if not ok:
            print('invalid frequency')

    def stop_laser(self):
        self.laser.stop()

    def handle_laser(self):
        to_emit = self.ids.toggle_manual_emit.state == 'down'
        if to_emit:
            self.emit_laser()
        else:
            self.stop_laser()

    def check_freq(self, freq_str):
        try:
            freq = int(freq_str)
        except ValueError:
            print('invalid freq input')
            return
        freq = max(16, freq)
        freq = min(10000, freq)
        self.ids.freq_input.text = str(freq)

    def check_vel(self, vel_str: str):
        try:
            vel = float(vel_str)
        except ValueError:
            print('invalid vel input')
            return
        vel = max(0.05, vel)
        vel = min(10000.0, vel)
        self.ids.vel_input.text = str(vel)

    def set_freq_from_slider(self, value: int):
        index = int(value)
        freq_list = [16, 50, 100, 500, 1000, 5000, 10000]
        self.freq = freq_list[index]
        self.ids.freq_input.text = str(self.freq)

    def set_vel_from_slider(self, value: int):
        index = int(value)
        vel_list = [1, 5, 10, 50, 100, 500, 1000]
        self.vel = vel_list[index]
        self.ids.vel_input.text = str(self.vel)

    def start_program_mode(self):
        pass

    def quit(self, obj):
        self.laser.quit()
        self.stage.quit()


class MainApp(App):
    def build(self):
        window = MainWindow()
        return window


if __name__ == '__main__':
    ExceptionManager.add_handler(CrashHandler())
    MainApp().run()

