import asyncio
from zaber_motion import Units
from zaber_motion.binary import Connection
from DebugClass import DebugConnection
from ConfigLoader import ConfigLoader

# 接続後の初回操作時，positionが[25400, 25400](最大値)になってしまう　電源を落とす直前に[25400, 25400]に移動しておくことで一応対処可能(0.01μmオーダーの誤差はある)
# システム上でpositionの値域を超えて動かそうとしても止まってしまう
# システム上は問題ないが現実の最小値(0)まで到達すると座標がリセットされる
# positionの値域は0~25400


class ZaberController:
    def __init__(self, cl: ConfigLoader):
        self.unit_pos = Units.LENGTH_MICROMETRES
        self.unit_vel = Units.VELOCITY_MICROMETRES_PER_SECOND

        self.default_position = [25400, 25400]

        self.port = cl.port_stage

        if cl.mode == 'DEBUG':
            self.connection = DebugConnection()
        elif cl.mode == 'RELEASE':
            self.connection = Connection.open_serial_port(self.port)

        # [0]がパソコンに直接つながれているアクチュエータ，[1]が連結されたもう一つのアクチュエータ
        self.device_x, self.device_y = self.connection.detect_devices()[:2]

    def move_top(self, vel: float):
        self.device_y.move_velocity(vel, unit=self.unit_vel)

    def move_bottom(self, vel: float):
        self.device_y.move_velocity(-vel, unit=self.unit_vel)

    def move_left(self, vel: float):
        self.device_x.move_velocity(-vel, unit=self.unit_vel)

    def move_right(self, vel: float):
        self.device_x.move_velocity(vel, unit=self.unit_vel)

    async def move_absolute_async(self, abs_x: float, abs_y: float):
        # x,yが同時に動く
        if (0 <= abs_x <= 25400) and (0 <= abs_y <= 25400):
            await asyncio.gather(
                self.device_x.move_absolute_async(abs_x, unit=self.unit_pos),
                self.device_y.move_absolute_async(abs_y, unit=self.unit_pos)
            )
            return True
        else:
            print('move_absolute : positions are out of range')
            return False

    async def move_relative_async(self, rel_x: float, rel_y: float):
        # x,yが同時に動く
        cur_x, cur_y = self.get_position_all()
        x = cur_x + rel_x  # 移動後の座標
        y = cur_y + rel_y
        if (0 <= x <= 25400) and (0 <= y <= 25400):
            await asyncio.gather(
                self.device_x.move_relative_async(rel_x, unit=self.unit_pos),
                self.device_y.move_relative_async(rel_y, unit=self.unit_pos)
            )
            return True
        else:
            print('move_relative : positions are out of range')
            return False

    async def move_default_async(self):
        await self.move_absolute_async(*self.default_position)

    def get_position_x(self):
        return self.device_x.get_position(unit=self.unit_pos)

    def get_position_y(self):
        return self.device_y.get_position(unit=self.unit_pos)

    # x,y座標をリストにして返す
    def get_position_all(self):
        x = self.get_position_x()
        y = self.get_position_y()
        return [x, y]

    def stop_x(self):
        self.device_x.stop()

    def stop_y(self):
        self.device_y.stop()

    def stop_all(self):
        self.stop_x()
        self.stop_y()

    def quit(self):
        self.connection.close()


async def test(self):
    # 各種関数の動作確認用

    print('position before moving')
    print(f'x position : {self.get_position_x()}  y position : {self.get_position_y()}')

    # await self.move_absolute(20000, 20000)
    # await self.move_relative(1000, 1000)
    await self.move_default()
    # self.move_right(1000)
    # self.move_left(1000)
    # self.move_top(1000)
    # self.move_bottom(1000)

    input('enterでstop')  # 応急処置
    self.stop_all()

    print('position after moving')
    print(f'x position : {self.get_position_x()}  y position : {self.get_position_y()}')


def main():
    PORT_NUM = "COM3"  # check
    z = ZaberController(PORT_NUM)

    asyncio.run(test(z))

    # loop = asyncio.get_event_loop() #こちらで実行すると次の警告が出る：DeprecationWarning: There is no current event loop
    # tasks = asyncio.gather(z.test())
    # loop.run_until_complete(tasks)

    z.quit()


if __name__ == '__main__':
    main()
