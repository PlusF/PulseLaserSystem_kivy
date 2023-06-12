import time
import asyncio
from zaber_motion import Units, Library, LogOutputMode
from zaber_motion.binary import Connection, Device

# 接続後の初回操作時，positionが[25400, 25400](最大値)になってしまう　電源を落とす直前に[25400, 25400]に移動しておくことで一応対処可能(0.01μmオーダーの誤差はある)
# システム上でpositionの値域を超えて動かそうとしても止まってしまう
# システム上は問題ないが現実の最小値(0)まで到達すると座標がリセットされる
# positonの値域は0~25400
# メモ：開発環境（自分のPC）で動作確認できるようにしておく

PORT_NUM = 3 #check

class ZaberController:
    def __init__(self, port):
        self.unit_pos = Units.LENGTH_MICROMETRES
        self.unit_vel = Units.VELOCITY_MICROMETRES_PER_SECOND

        self.default_position = [25400, 25400]

        self.port = "COM" + str(port)
        self.connection = Connection.open_serial_port(self.port)
        # 引数[0]がパソコンに直接つながれているアクチュエータ，引数[1]が連結されたもう一つのアクチュエータ
        self.device_x = self.connection.detect_devices()[0]
        # print(self.device_x)
        self.device_y = self.connection.detect_devices()[1]
        # print(self.device_y)

    def move_top(self, vel):
        self.device_y.move_velocity(vel, unit=self.unit_vel)

    def move_bottom(self, vel):
        self.device_y.move_velocity(-vel, unit=self.unit_vel)

    def move_left(self, vel):
        self.device_x.move_velocity(-vel, unit=self.unit_vel)

    def move_right(self, vel):
        self.device_x.move_velocity(vel, unit=self.unit_vel)

    async def move_absolute(self, position_x, position_y):
        #x,yが同時に動く
        if (0 <= position_x <= 25400) and (0 <= position_y <= 25400):
            await asyncio.gather(
                self.device_x.move_absolute_async(position_x, unit=self.unit_pos),
                self.device_y.move_absolute_async(position_y, unit=self.unit_pos)
            )
        else:
            print('move_absolute : positions are out of range')

    async def move_relative(self, position_x, position_y):
        #x,yが同時に動く
        position_list = self.get_position_all()
        x = position_list[0] + position_x #移動後の座標
        y = position_list[1] + position_y
        if (0 <= x <= 25400) and (0 <= y <= 25400):
            await asyncio.gather(
                self.device_x.move_relative_async(position_x, unit=self.unit_pos),
                self.device_y.move_relative_async(position_y, unit=self.unit_pos)
            )
        else:
            print('move_relative : positions are out of range')

    async def move_default(self):
        await self.move_absolute_acync(self.default_position[0], self.default_position[1])

    def get_position_x(self):
        return self.device_x.get_position(unit=self.unit_pos)

    def get_position_y(self):
        return self.device_y.get_position(unit=self.unit_pos)

    #x,y座標をリストにして返す
    def get_position_all(self):
        position_list = []
        position_list.append(self.device_x.get_position(unit=self.unit_pos))
        position_list.append(self.device_y.get_position(unit=self.unit_pos))
        return position_list

    def stop_x(self):
        self.device_x.stop(unir=self.unit.pos)

    def stop_y(self):
        self.device_y.stop(unir=self.unit.pos)

    def stop_all(self):
        self.device_x.stop(unit=self.unit_pos)
        self.device_y.stop(unit=self.unit_pos)

    def quit(self):
        self.connection.close()

    async def test(self):
        #各種関数の動作確認用

        print('position before moving')
        print(f'x position : {self.get_position_x()}  y position : {self.get_position_y()}')

        # await self.move_absolute(2000, 2000)
        # await self.move_relative(1000, 1000)
        await self.move_default()
        # self.move_right(1000)
        # self.move_left(1000)
        # self.move_top(1000)
        # self.move_bottom(1000)

        input('enterでstop') #応急処置
        self.stop_all()

        print('position after moving')
        print(f'x position : {self.get_position_x()}  y position : {self.get_position_y()}')

def main():
    z = ZaberController(PORT_NUM)

    asyncio.run(z.test())

    # loop = asyncio.get_event_loop() #こちらで実行すると次の警告が出る：DeprecationWarning: There is no current event loop
    # tasks = asyncio.gather(z.test())
    # loop.run_until_complete(tasks)

    z.quit()


if __name__ == '__main__':
    main()

