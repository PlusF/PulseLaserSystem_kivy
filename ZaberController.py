from zaber_motion import Units, Library, LogOutputMode
from zaber_motion.binary import Connection, Device

# 接続後の初回操作時，move_velocityではCommand 21 のエラーで動かず断念　positionの値がシステム上最大値になっていた（実際は最小値だった）のが原因か
# その後move_absoluteで動かしたところCommand 20 のエラーで動かなかったが，そのときpositionが0(原点)に物理的にもどって，2回目からは同じコードで動いた．それ以降はmove_velocityでも動作確認済
# positonの値域は0~25000ぐらい？
# メモ：開発環境（自分のPC）で動作確認できるようにしておく
class ZaberController:
    def __init__(self):
        self.unit_pos = Units.LENGTH_MICROMETRES
        self.unit_vel = Units.VELOCITY_MICROMETRES_PER_SECOND

        self.port = 'COM3' #check
        self.connection = Connection.open_serial_port(self.port)
        # 引数[0]がパソコンに直接つながれているアクチュエータ，引数[1]が連結されたもう一つのアクチュエータ
        self.device_x = self.connection.detect_devices()[0]
        # print(self.device_x)
        self.device_y = self.connection.detect_devices()[1]
        # print(self.device_y)

        print('position before moving')
        print(f'x position : {self.device_x.get_position(unit=self.unit_pos)}')
        print(f'y position : {self.device_y.get_position(unit=self.unit_pos)}')

        #velocity等の各種値設定
        self.vel = 1000
        self.x_absolute_position = 100
        self.y_absolute_position = 100
        self.x_relative_position = 1000
        self.y_relative_position = 1000

        self.move_absolute()
        # self.move_relative()
        # self.move_right()
        # self.move_left()
        # self.move_top()
        # self.move_bottom()


        input('enterでstop') #応急処置
        self.stop()

        print('position after moving')
        print(f'x position : {self.device_x.get_position(unit=self.unit_pos)}')
        print(f'y position : {self.device_y.get_position(unit=self.unit_pos)}')

        pass

    def move_top(self):
        self.device_y.move_velocity(self.vel, unit=self.unit_vel)
        pass

    def move_bottom(self):
        self.device_y.move_velocity(-self.vel, unit=self.unit_vel)
        pass

    def move_left(self):
        self.device_x.move_velocity(-self.vel, unit=self.unit_vel)
        pass

    def move_right(self):
        self.device_x.move_velocity(self.vel, unit=self.unit_vel)
        pass

    def move_absolute(self):
        self.device_x.move_absolute(self.x_absolute_position, unit=self.unit_pos)
        self.device_y.move_absolute(self.y_absolute_position, unit=self.unit_pos)
        pass

    def move_relative(self):
        self.device_x.move_relative(self.x_relative_position, unit=self.unit_pos)
        self.device_y.move_relative(self.y_relative_position, unit=self.unit_pos)
        pass

    def stop(self):
        self.device_x.stop(unit=self.unit_pos)
        self.device_y.stop(unit=self.unit_pos)
        pass


if __name__ == '__main__':
    z = ZaberController()
