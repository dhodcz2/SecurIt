from dataclasses import dataclass
import sqlite3
import csv
from argparse import ArgumentParser
# TODO: Implement PostgreSQL instead of SQLite

@dataclass
class Client:
    client_id: int
    name: str = None
    email: str = None
    phone: str = None

def _rebuild(filename):
    with open(filename) as f:
        r = csv.reader(f)
        rows = list(row for row in r)

        conn = sqlite3.connect('clients.db')
        c = conn.cursor()
        with conn:
            c.executescript('''
            drop table if exists clients;
            create table clients(
            client_id integer primary key ,
            name text,
            email text,
            phone text
            );
            ''')
            c.executemany('''
            insert into clients
            values (?, ?, ?, ?)
            ''', rows)


def get_clients_from_client_ids(client_ids: list[int]) -> list[Client]:
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    with conn:
        c.execute("""
        select * from clients where client_id in (%s)
        """ % (', '.join(str(client_id) for client_id in client_ids)))
        return [Client(client) for client in c.fetchall()]

class Arguments:
    rebuild: str

if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument('--rebuild', type=str, help='client database to be (re)built')
    args = args.parse_args(namespace=Arguments)

    if args.rebuild:
        _rebuild(args.rebuild)
