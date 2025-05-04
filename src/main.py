# Programmed with <3 by fluffy

# CUSTOMER DATA: https://schedule-1.fandom.com/wiki/Customers

from dataclasses import dataclass
from enum import Enum
import os

class Area(Enum):
    NORTHTOWN = 0
    WESTVILLE = 1
    DOWNTOWN = 2
    DOCKS = 3
    SUBURBIA = 4
    UPTOWN = 5

    @staticmethod
    def find(key:str) -> 'Area | None':
        try:
            return Area[key]
        except KeyError:
            return None

class Standard(Enum):
    VERY_LOW = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    VERY_HIGH = 4

    @staticmethod
    def find(key:str) -> 'Standard | None':
        try:
            return Standard[key]
        except KeyError:
            return None

@dataclass
class MinMax:
    min:float
    max:float

def strfield(data, length:int, space:str=' ') -> str:
    return str(data) + space * (length - len(str(data)))

@dataclass
class Customer:
    name:str
    area:Area
    standard:Standard
    weed_affinity:float
    meth_affinity:float
    coca_affinity:float
    weekly_budget:MinMax
    orders_per_week:MinMax
    additional:str # TOO LAZY TO PARSE THIS RN

    def __repr__(self) -> str:
        s:str = '| '
        s += strfield(self.name, 20) + ' | '
        s += strfield(self.area, 20) + ' | '
        s += strfield(self.standard, 20) + ' | '
        s += strfield(self.weed_affinity, 5) + ' | '
        s += strfield(self.meth_affinity, 5) + ' | '
        s += strfield(self.coca_affinity, 5) + ' | '
        s += strfield(self.weekly_budget.min, 5) + ' | '
        s += strfield(self.weekly_budget.max, 5) + ' | '
        s += strfield(self.orders_per_week.min, 5) + ' | '
        s += strfield(self.orders_per_week.max, 5) + ' |'
        return s

    @staticmethod
    def parse(line:str) -> 'Customer':
        fields:list[str] = line.split('\t')
        name:str = fields[0]
        area:Area = Area.find(fields[1].upper())
        standard:Standard = Standard.find(fields[2].upper().replace(' ', '_'))
        weed_affinity:float = float(fields[3])
        meth_affinity:float = float(fields[4])
        coca_affinity:float = float(fields[5])
        weekly_budget:MinMax = MinMax(int(fields[6][1:]), int(fields[7][1:]))
        orders_per_week:MinMax = MinMax(int(fields[8]), int(fields[9]))
        additional:str = '\t'.join(fields[10:])
        return Customer(
            name, area, standard, weed_affinity, meth_affinity, coca_affinity, weekly_budget, orders_per_week, additional
        )

def get_table_headers() -> str:
    s:str = '  '
    s += strfield('Name', 20) + '   '
    s += strfield('Area', 20) + '   '
    s += strfield('Standard', 20) + '   '
    s += strfield('Weed', 5) + '   '
    s += strfield('Meth', 5) + '   '
    s += strfield('Coca', 5) + '   '
    s += strfield('Min B', 5) + '   '
    s += strfield('Max B', 5) + '   '
    s += strfield('Min O', 5) + '   '
    s += strfield('Max O', 5) + '  '
    return s

def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def main() -> int:
    customers:list[Customer]
    with open('./data/customers', 'r', encoding='utf-8') as data_stream:
        customers = [Customer.parse(line.strip()) for line in data_stream.readlines()]

    clear_terminal()
    # while 1:
    #     raw_command = input('> ')
    #     args = raw_command.split(' ')

    # print(f'   {get_table_headers()}')
    # i:int = 0
    # cs = sorted(customers, key=lambda c: c.area.value)
    # for c in cs:
    #     print(f'{i:2}', c)
    #     i += 1
    # return 0

    supported_areas:list[Area] = [Area.NORTHTOWN, Area.WESTVILLE, Area.DOWNTOWN]

    for area in supported_areas:
        customer_list:list[Customer] = sorted(customers, key=lambda customer: (
            (customer.weed_affinity) * (
                (customer.weekly_budget.min + customer.weekly_budget.max) / 2
            ) * (
                (customer.orders_per_week.min + customer.orders_per_week.max) / 2
            )
        ), reverse=1)
        print(f'{area}:')
        print(f'   {get_table_headers()}')
        i:int = 0
        average_orders:int = 0
        average_budget:int = 0
        average_affinity:int = 0
        for c in customer_list:
            if i >= 8: continue
            if c.area != area: continue
            print(f'{i:2}', c)
            average_orders += (c.orders_per_week.min + c.orders_per_week.max) / 2
            average_budget += (c.weekly_budget.min + c.weekly_budget.max) / 2
            average_affinity += (c.weed_affinity)
            customers.remove(c)
            i += 1
        print('')
        print(f'Average Orders: {average_orders / 8} / week')
        print(f'Average Budget: {average_budget / 8} $ / week')
        print(f'Average Affinity: {average_affinity / 8}')
        print(f'Sector Valuability: {average_orders * average_budget * average_affinity / 1000000} $ / week²')
        print()

    supported_areas:list[Area] = [Area.DOCKS]

    for area in supported_areas:
        customer_list:list[Customer] = sorted(customers, key=lambda customer: (
            (customer.coca_affinity) * (
                (customer.weekly_budget.min + customer.weekly_budget.max) / 2
            ) * (
                (customer.orders_per_week.min + customer.orders_per_week.max) / 2
            )
        ), reverse=1)
        print(f'{area}:')
        print(f'   {get_table_headers()}')
        i:int = 0
        average_orders:int = 0
        average_budget:int = 0
        average_affinity:int = 0
        for c in customer_list:
            if i >= 8: continue
            if c.area != area: continue
            print(f'{i:2}', c)
            average_orders += (c.orders_per_week.min + c.orders_per_week.max) / 2
            average_budget += (c.weekly_budget.min + c.weekly_budget.max) / 2
            average_affinity += (c.coca_affinity)
            customers.remove(c)
            i += 1
        print('')
        print(f'Average Orders: {average_orders / 8} / week')
        print(f'Average Budget: {average_budget / 8} $ / week')
        print(f'Average Affinity: {average_affinity / 8}')
        print(f'Sector Valuability: {average_orders * average_budget * average_affinity / 1000000} $ / week²')
        print()
    return 0

if __name__ == '__main__':
    quit(main())