class DebugConnection:
    def __init__(self):
        pass

    def detect_devices(self):
        return [DebugDevice('x'), DebugDevice('y')]

    def close(self):
        print('close connection')


class DebugDevice:
    def __init__(self, name: str):
        self.name = name
        self.pos = 0

    def move_velocity(self, vel: float, unit):
        print(f'{self.name} moving by velocity {vel} {unit}')
        self.pos += vel

    async def move_absolute_async(self, pos: float, unit):
        print(f'{self.name} moving to absolute {pos} {unit}')

    def get_position(self, unit):
        # print(f'{self.name} position is  {self.pos} {unit}')
        return self.pos

    def stop(self):
        print(f'{self.name} stop')


class DebugSerial:
    def __init__(self, *args, **kwargs):
        pass

    def write(self, msg):
        print(f'serial write:\n\t{msg}')

    def close(self):
        print('close serial')
