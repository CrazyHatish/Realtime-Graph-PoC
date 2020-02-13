from sqlalchemy import Table, Column, Integer, Float, MetaData, create_engine, select
import pandas as pd
from time import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

engine = create_engine('sqlite:///data.db')

metadata = MetaData()

data = Table('data', metadata,
             Column('time', Float, primary_key=True),
             Column('thing_ma_bob', Float),
             Column('thermostatic_combobulator', Float),
             Column('hypersonic_diffuser', Float))

fig = plt.figure()
axes = fig.subplots(3, 1, sharex=True)
lns = []
colors = ['blue', 'red', 'green']
for i in range(3):
    lns.append(axes[i].plot([], [], color=colors[i])[0])


def init():
    for (i, l) in enumerate([(700, 1300, 'Thing-ma-bob', 'kHz'),
                             (8, 12, 'Thermostatic combobulator', 'GW'),
                             (150, 210, 'Hypersonic diffuser', 'TB/s')]):
        axes[i].set_xlim(-10, 0)
        axes[i].set_ylim(l[0], l[1])
        axes[i].set_title(l[2])
        axes[i].set_ylabel(l[3])

    axes[2].set_xlabel('Δt(s)')

    return lns


def update(_):
    curr_time = time()
    time_limit = curr_time - 10
    s = select([data]).where(data.c.time > time_limit)

    timed_data = pd.read_sql(s, engine)
    time_column = timed_data.loc[:, 'time'] - curr_time

    for (i, d) in enumerate(['thing_ma_bob', 'thermostatic_combobulator', 'hypersonic_diffuser']):
        lns[i].set_data(time_column, timed_data.loc[:, d])

    return lns


ani = FuncAnimation(fig, update, init_func=init, interval=10, blit=True)

plt.show()
