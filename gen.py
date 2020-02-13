from sqlalchemy import Table, Column, Integer, Float, MetaData, create_engine
from time import sleep, time
from math import sin, cos
from random import random

engine = create_engine('sqlite:///data.db')

metadata = MetaData()

data = Table('data', metadata,
             Column('time', Float, primary_key=True),
             Column('thing_ma_bob', Float),
             Column('thermostatic_combobulator', Float),
             Column('hypersonic_diffuser', Float))

metadata.create_all(engine)
ins = data.insert()
conn = engine.connect()

prev_time = time()
data_to_send = []

for i in range(10000000000000):
    data_to_send.append({'time': time(),
                         'thing_ma_bob': 800 + 400*random(),
                         'thermostatic_combobulator': 10 + sin(i/100)*random(),
                         'hypersonic_diffuser': 180 - 20*cos(i/100)
                         })

    if time() - prev_time >= 0.001:
        conn.execute(ins, data_to_send)
        prev_time = time()
        data_to_send = []
    else:
        sleep(0.000001)
