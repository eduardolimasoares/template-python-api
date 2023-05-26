from yoyo import step

def apply_step(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO status (status) VALUES ('Ativo')")
    cursor.execute("INSERT INTO status (status) VALUES ('Inativo')")
    cursor.execute("INSERT INTO status (status) VALUES ('Pendente')")

steps = [
  step(apply_step)
]

"""
yoyo init --database sqlite:///mydb.sqlite3  migrations
"""