from abc import ABCMeta, abstractmethod


class SensitiveInfo(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def add(self, user):
        pass


class Info:
    def __init__(self):
        self.users = ['nick', 'tom', 'ben', 'mike']
        self.secret = '0xdeadbeef'

    def read(self):
        print('There are {} users: {}'.format(len(self.users), ' '.join(self.users)))

    def add(self, user):
        sec = input('what is the secret?')
        self.users.append(user) if sec == self.secret else print("That's wrong")
        print('Added user {}'.format(user))


def main():
    info = Info()

    while True:
        print('1. read list |==| 2. add user |==| 3. quit')
        key = input('choose option: ')
        if key == '1':
            info.read()
        elif key == '2':
            name = input('choose username: ')
            info.add(name)
        elif key == '3':
            exit()
        else:
            print('unknown option: {}'.format(key))


if __name__ == "__main__":
    main()
