from kivy.app import App
from kivy.core.window import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.base import ExceptionManager, ExceptionHandler
from ConfigLoader import ConfigLoader
from PulseLaserController import PulseLaserController
from ZaberController import ZaberController
# メモ：ZaberControllerクラスをインポート


def control_auto_emission(func):
    def wrapper(self, *args, **kwargs):
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        if auto_on:
            self.emit_laser()
        ret = func(*args, **kwargs)
        return ret
    return wrapper


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

        self.freq: int = 100
        self.speed: float = 100.0

        self.laser = PulseLaserController(self.cl)
        self.stage = ZaberController(self.cl)

        Clock.schedule_interval(self.update_position, 0.1)  # 0.1秒ごとに位置を更新．

    def update_position(self, dt):
        self.pos_x, self.pos_y = self.stage.get_position_all()

    @control_auto_emission
    def move_top(self):
        # TODO: IMPLEMENT ME
        # メモ：ZaberControllerインスタンスのmove_top関数を呼び出す
        pass

    @control_auto_emission
    def move_bottom(self):
        # TODO: IMPLEMENT ME
        pass

    @control_auto_emission
    def move_left(self):
        # TODO: IMPLEMENT ME
        pass

    @control_auto_emission
    def move_right(self):
        # TODO: IMPLEMENT ME
        pass

    def stop_moving(self):
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        if auto_on:
            self.stop_laser()
        # TODO: stop()

    def emit_laser(self):
        ok = self.laser.emit(self.freq)
        if not ok:
            # TODO: 警告を表示する
            pass

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

    def check_speed(self, speed_str: str):
        try:
            speed = float(speed_str)
        except ValueError:
            print('invalid speed input')
            return
        speed = max(0.05, speed)
        speed = min(10000.0, speed)
        self.ids.speed_input.text = str(speed)

    def set_freq_from_slider(self, value: int):
        index = int(value)
        freq_list = [16, 50, 100, 500, 1000, 5000, 10000]
        self.freq = freq_list[index]
        self.ids.freq_input.text = str(self.freq)

    def set_speed_from_slider(self, value: int):
        index = int(value)
        speed_list = [1, 5, 10, 50, 100, 500, 1000]
        self.speed = speed_list[index]
        self.ids.speed_input.text = str(self.speed)

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

