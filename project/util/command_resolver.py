

class CommandResolver:

    @staticmethod
    def resolve_command(commands):
        commands = commands.split(' ')

        res = {
            "board_id": commands[2],
            "action": commands[0],
            "username": commands[1]
        }

        if len(commands) > 3:
            coordinate = commands[3].split(',')
            res["x"] = int(coordinate[0])
            res["y"] = int(coordinate[1])

        return res
