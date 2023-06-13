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

        # 初期設定（GUIの初期設定と合致している必要あり）
        self.freq: int = 16
        self.vel: float = 1.0

        # DEBUG or RELEASEは各クラス内で処理してもらい，main側は意識しなくてよいように
        self.laser = PulseLaserController(self.cl)
        self.stage = ZaberController(self.cl)

        # move関数を統一するために辞書形式に関数をまとめた
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

        Clock.schedule_interval(self.update_position, self.cl.dt_sec)

    def update_position(self, dt):
        # 位置情報の更新．Clockによって定期実行される．定期実行のスパンはConfigによって定められている．
        self.pos_x, self.pos_y = self.stage.get_position_all()

    def move(self, axis: str, direction: str):
        # 上下左右の移動をつかさどる関数．コードの反復を避けるために統一させた．
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        move_func = self.move_funcs[axis][direction]

        # Auto emissionがONであればレーザー照射
        if auto_on:
            self.emit_laser()
        move_func(self.vel)

    def stop_moving(self):
        # Auto emissionがONであればレーザー停止
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        if auto_on:
            self.stop_laser()
        self.stage.stop_all()

    def emit_laser(self):
        # 周波数に問題ないかはLaserクラス内でもチェックされる
        ok = self.laser.emit(self.freq)
        if not ok:
            print('invalid frequency')

    def stop_laser(self):
        self.laser.stop()

    def handle_laser(self):
        # Manual emissionのための関数
        to_emit = self.ids.toggle_manual_emit.state == 'down'
        if to_emit:
            self.emit_laser()
        else:
            self.stop_laser()

    def check_freq(self, freq_str):
        # テキストが変更されると呼び出される．既定の範囲内に収めさせる．
        try:
            freq = int(freq_str)
        except ValueError:
            print('invalid freq input')
            return
        freq = max(16, freq)
        freq = min(10000, freq)
        self.ids.freq_input.text = str(freq)

    def check_vel(self, vel_str: str):
        # テキストが変更されると呼び出される．既定の範囲内に収めさせる．
        try:
            vel = float(vel_str)
        except ValueError:
            print('invalid vel input')
            return
        vel = max(0.05, vel)
        vel = min(10000.0, vel)
        self.ids.vel_input.text = str(vel)

    def set_freq_from_slider(self, value: int):
        # スライダーでは離散的にキリの良い値を指定できるように
        # リストの長さとスライダーの値の範囲が合致している必要あり
        index = int(value)
        freq_list = [16, 50, 100, 500, 1000, 5000, 10000]
        self.freq = freq_list[index]
        self.ids.freq_input.text = str(self.freq)

    def set_vel_from_slider(self, value: int):
        # スライダーでは離散的にキリの良い値を指定できるように
        # リストの長さとスライダーの値の範囲が合致している必要あり
        index = int(value)
        vel_list = [1, 5, 10, 50, 100, 500, 1000]
        self.vel = vel_list[index]
        self.ids.vel_input.text = str(self.vel)

    def start_program_mode(self):
        # TODO: IMPLEMENT ME
        pass

    def quit(self, obj):
        # シリアル通信を閉じてからプログラムを終了
        self.laser.quit()
        self.stage.quit()


class MainApp(App):
    def build(self):
        window = MainWindow()
        return window


if __name__ == '__main__':
    ExceptionManager.add_handler(CrashHandler())
    MainApp().run()

