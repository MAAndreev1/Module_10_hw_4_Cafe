from threading import Thread
from random import randint
import time
import queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        time.sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = queue.Queue()

    # Прибытие гостей
    def guest_arrival(self, *guests):
        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    break
                elif all([x.guest for x in self.tables]):
                    self.queue.put(guest)
                    print(f'{guest.name} в очереди')
                    break

    def discuss_guests(self):  # Обслужить гостей
        while not self.queue.empty() or any([x.guest for x in self.tables]):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен.')
                    table.guest = None
                if table.guest is None and not self.queue.empty():
                    guest = self.queue.get()
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')


tables = [Table(number) for number in range(1, 6)]
# for i in tables:
#     print(i.number)
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
                'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']
guests = [Guest(name) for name in guests_names]
# for i in guests:
#     print(i.name)
cafe = Cafe(*tables)
# for i in cafe.tables:
#     print(i.number)
cafe.guest_arrival(*guests)
cafe.discuss_guests()

for i in guests:
    i.join()
