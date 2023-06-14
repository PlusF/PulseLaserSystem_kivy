from kivy.app import App
from kivy.base import ExceptionManager, ExceptionHandler
from kivy.core.window import Clock, Window
from kivy.properties import NumericProperty, ListProperty
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
    freq_list = ListProperty([16, 50, 100, 500, 1000, 5000, 10000])
    vel_list = ListProperty([0.5, 1, 5, 10, 50, 100, 500, 1000, 5000, 10000])
    Window.size = (350, 650)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_request_close=self.quit)

        self.cl = ConfigLoader('./config.json')

        # 初期設定（GUIの初期設定と合致している必要あり）
        self.freq: int = 16
        self.vel: float = 1000.0

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
                '+': self.stage.move_bottom,  # アクチュエータの取付方向が上下反転
                '-': self.stage.move_top
            }
        }
        # キーボード入力も受け付けるために必要
        self.is_moving = {
            'x': {
                '+': False,
                '-': False,
            },
            'y': {
                '+': False,
                '-': False,
            }
        }
        # キーボード入力も受け付けるために必要
        self.move_widgets = {
            'x': {
                '+': self.ids.move_right,
                '-': self.ids.move_left,
            },
            'y': {
                '+': self.ids.move_top,
                '-': self.ids.move_bottom,
            }
        }

        def enable_laser(dt):  # Arduinoの接続待ち（1秒もかかりはしないが念のため)
            self.ids.toggle_auto_emit.disabled = False
            self.ids.toggle_manual_emit.disabled = False
        Clock.schedule_once(enable_laser, 1)
        Clock.schedule_interval(self.update_position, self.cl.dt_sec)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key in ['a', 'left']:
            axis = 'x'
            direction = '-'
        elif key in ['w', 'up']:
            axis = 'y'
            direction = '+'
        elif key in ['d', 'right']:
            axis = 'x'
            direction = '+'
        elif key in ['s', 'down']:
            axis = 'y'
            direction = '-'
        else:
            return
        if self.is_moving[axis][direction]:  # 押し続けると複数回の入力が来るので，不要な場合はスルー
            return
        self.move(axis, direction)
        self.move_widgets[axis][direction].state = 'down'

    def _on_keyboard_up(self, keyboard, keycode):
        key = keycode[1]
        if key in ['a', 'left']:
            axis = 'x'
            direction = '-'
        elif key in ['w', 'up']:
            axis = 'y'
            direction = '+'
        elif key in ['d', 'right']:
            axis = 'x'
            direction = '+'
        elif key in ['s', 'down']:
            axis = 'y'
            direction = '-'
        else:
            return
        self.stop_moving(axis, direction)
        self.move_widgets[axis][direction].state = 'normal'

    def update_position(self, dt):
        # 位置情報の更新．Clockによって定期実行される．定期実行のスパンはConfigによって定められている．
        x, y = self.stage.get_position_all()
        self.pos_x, self.pos_y = x, 25400.032 - y  # y軸アクチュエータの取付方向が上下反転

    def move(self, axis: str, direction: str):
        # 上下左右の移動をつかさどる関数．コードの反復を避けるために統一させた．
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        # すでに動いている軸があるか確認
        all_stage_stopped = not any([self.is_moving[a][d] for d in ['+', '-'] for a in ['x', 'y']])
        move_func = self.move_funcs[axis][direction]

        # Auto emissionがONかつまだ照射されていなければレーザー照射
        if auto_on and all_stage_stopped:
            self.emit_laser()
        move_func(self.vel)

        self.is_moving[axis][direction] = True

    def stop_moving(self, axis, direction):
        self.is_moving[axis][direction] = False
        # 反対方向のキーを両方押してしまっている場合は，片方離したところで止めない
        still_moving = any(self.is_moving[axis].values())
        if still_moving:
            return

        if axis == 'x':
            self.stage.stop_x()
        elif axis == 'y':
            self.stage.stop_y()

        # Auto emissionがONかつステージがすべて停止していればレーザー停止
        auto_on = self.ids.toggle_auto_emit.state == 'down'
        all_stage_stopped = not any([self.is_moving[a][d] for d in ['+', '-'] for a in ['x', 'y']])
        if auto_on and all_stage_stopped:
            self.stop_laser()

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
        self.freq = freq

    def check_vel(self, vel_str: str):
        # テキストが変更されると呼び出される．既定の範囲内に収めさせる．
        try:
            vel = float(vel_str)
        except ValueError:
            print('invalid vel input')
            return
        vel = max(0.5, vel)
        vel = min(10000.0, vel)
        self.ids.vel_input.text = str(vel)
        self.vel = vel

    def set_freq_from_slider(self, value: int):
        # スライダーでは離散的にキリの良い値を指定できるように
        # リストの長さとスライダーの値の範囲が合致している必要あり
        index = int(value)
        self.freq = self.freq_list[index]
        self.ids.freq_input.text = str(self.freq)

    def set_vel_from_slider(self, value: int):
        # スライダーでは離散的にキリの良い値を指定できるように
        # リストの長さとスライダーの値の範囲が合致している必要あり
        index = int(value)
        self.vel = self.vel_list[index]
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

