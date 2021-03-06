'''
实例：属性验证：使用描述符验证
'''


class CardHolder:
    acctlen = 8  # Class data
    retireage = 59.5

    def __init__(self, acct, name, age, addr):
        self.acct = acct  # Instance data
        self.name = name  # These trigger __set__ calls too
        self.age = age  # __X not needed: in descriptor
        self.addr = addr  # addr is not managed
    # remain has no data

    class Name:
        def __get__(self, instance, owner):  # Class names: CardHolder locals
            return self.name

        def __set__(self, instance, value):
            value = value.lower().replace(' ', '_')
            self.name = value

    name = Name()

    class Age:
        def __get__(self, instance, owner):
            return self.age  # Use descriptor data

        def __set__(self, instance, value):
            if value < 0 or value > 150:
                raise ValueError('invalid age')
            else:
                self.age = value

    age = Age()

    class Acct:
        def __get__(self, instance, owner):
            return self.acct[:-3] + '***'

        def __set__(self, instance, value):
            value = value.replace('-', '')
            if len(value) != instance.acctlen:  # Use instance class data
                raise TypeError('invald acct number')
            else:
                self.acct = value

    acct = Acct()

    class Remain:
        def __get__(self, instance, owner):
            return instance.retireage - instance.age  # Triggers Age.__get__

        def __set__(self, instance, value):
            raise TypeError('cannot set remain')  # Else set allowed here

    remain = Remain()


if __name__ == '__main__':
    bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')
    print(bob.acct, bob.name, bob.age, bob.remain, bob.addr, sep=' / ')
    bob.name = 'Bob Q. Smith'
    bob.age = 50
    bob.acct = '23-45-67-89'
    print(bob.acct, bob.name, bob.age, bob.remain, bob.addr, sep=' / ')
    sue = CardHolder('5678-12-34', 'Sue Jones', 35, '124 main st')
    print(sue.acct, sue.name, sue.age, sue.remain, sue.addr, sep=' / ')
    try:
        sue.age = 200
    except:
        print('Bad age for Sue')
    try:
        sue.remain = 5
    except:
        print("Can't set sue.remain")
    try:
        sue.acct = '1234567'
    except:
        print('Bad acct for Sue')
