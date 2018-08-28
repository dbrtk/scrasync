

import buffer


def create_file():
    open('user-agents.txt', 'w+').close()
    with open('user-agents.txt', 'a') as _file:
        for k, v in buffer.AGENTS.items():
            for agent_string in v:
                print(agent_string)
                _file.write('%s\n' % agent_string)


if __name__ == '__main__':

    print('creating the file containng user agents.')
    create_file()
