import os
import re
from docx import Document
import sqlite3



def scan_directory(path, folder, conn):
    for file in os.listdir(path):
        scan_file(path + '/' + file, folder, conn)


def scan_file(path, folder, c):
    print(path+"\n")
    document = Document(path)
    for table in document.tables:
        if folder == "generale":
            for row in table.rows:
                # codice|question|a|b|c|d|answer
                print("add " + row.cells[0].text)
                insert = (row.cells[0].text,
                          row.cells[1].text,
                          row.cells[2].text,
                          row.cells[3].text,
                          row.cells[4].text,
                          row.cells[5].text,
                          row.cells[6].text,
                          folder)
                c.execute("INSERT INTO domande VALUES (?,?,?,?,?,?,?,?)", insert)
        elif folder == "sunto":
            for row in table.rows:
                # codice|question|a|b|c|d|answer
                print("add " + row.cells[0].text)
                insert = (row.cells[0].text,
                          row.cells[1].text,
                          row.cells[2].text,
                          row.cells[3].text,
                          row.cells[4].text,
                          row.cells[5].text,
                          row.cells[6].text,
                          folder)
                c.execute("INSERT INTO domande VALUES (?,?,?,?,?,?,?,?)", insert)
        elif folder == "comprensione":
            for row in table.rows:
                # codice|testo(span 5)|empty
                # codice|question|a|b|c|d|answer

                if re.search('[A-Z]{2}[0-9]{3}0{2}', row.cells[0].text):
                    # is the text
                    print("add " + row.cells[0].text)
                    insert = (row.cells[0].text,
                          row.cells[1].text,
                          None,
                          None,
                          None,
                          None,
                          None,
                          "comprensione_a")
                    c.execute("INSERT INTO domande VALUES (?,?,?,?,?,?,?,?)", insert)
                else:
                    #question over the text
                    print("add " + row.cells[0].text)
                    insert = (row.cells[0].text,
                          row.cells[1].text,
                          row.cells[2].text,
                          row.cells[3].text,
                          row.cells[4].text,
                          row.cells[5].text,
                          row.cells[6].text,
                          "comprensione_b")
                    c.execute("INSERT INTO domande VALUES (?,?,?,?,?,?,?,?)", insert)
    document.save(path)


def scan_question(conn):
    base_path = "../../CulturaGenerale_docx/"
    folders = ["generale", "sunto", "comprensione"]

    for folder in folders:
        scan_directory(base_path + folder, folder, conn)


if __name__ == '__main__':
    if not os.path.isfile("question.db"):
        conn = sqlite3.connect('question.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE domande
                (codice, domanda, a, b, c, d, risposta, tipo)''')
        conn.commit()
        conn.close()

    conn = sqlite3.connect('question.db')
    c = conn.cursor()
    #output = scan_file("../../CulturaGenerale_docx/comprensione/AA.docx", "comprensione", c)
    scan_question(c)
    conn.commit()
    conn.close()