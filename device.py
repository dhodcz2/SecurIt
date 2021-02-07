from dataclasses import dataclass
import sqlite3
import csv
from argparse import ArgumentParser
from client import Client, get_clients


@dataclass
class Device:
    device_id: int
    clients: list[Client]


def rebuild(filename):
    with open(filename) as f:
        r = csv.reader(f)
        rows = list(row for row in r)

        conn = sqlite3.connect('devices.db')
        c = conn.cursor()
        with conn:
            c.executescript("""
             drop table if exists devices;
             create table devices(
             device_id integer primary key ,
             client_id integer
             );
             """)
            c.executemany('insert into devices values (?, ?)', rows)

def get_clients_from_device(device_id: int) -> list[Client]:
    conn = sqlite3.connect('devices.db')
    c = conn.cursor()
    with conn:
        c.execute(f"""
        select client_id
        from devices
        where device_id={device_id}
        """)

class Arguments:
    rebuild: str

if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument('--rebuild', type=str, help='device database to be (re)built')
    args = args.parse_args(namespace=Arguments)

    if args.rebuild:
        rebuild(args.rebuild)
