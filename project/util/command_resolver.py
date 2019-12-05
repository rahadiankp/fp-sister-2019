

class CommandResolver:

    @staticmethod
    def resolve_command(commands):
        commands = commands.split(' ')

        if commands[0] == 'START':
            return {
                'action': 'START',
                'username': commands[1]
            }
        elif commands[0] == 'UPDATE':
            return {
                'action': 'UPDATE'
            }
        else:
            res = {
                "board_id": int(commands[2]),
                "action": commands[0],
                "username": commands[1]
            }

            if len(commands) > 3:
                coordinate = commands[3].split(',')
                res["x"] = int(coordinate[0])
                res["y"] = int(coordinate[1])

            return res
