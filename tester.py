import sqlite3
import random
import time
import re
import pprint
import win_unicode_console

def sec_print(txt):
    print(str(txt))


def return_type(codice):
    """Are considered special question the ones in comprensione category since they must be load in bulk"""
    if re.search('[AB]{2}[0-9]{5}', codice):
        return "s"  #special
    return "n"  #normal

def special_handle(codice, c):
    block = (codice[:5] + "%", )
    #pprint.pprint(block)
    c.execute("""select *
                from domande
                where codice LIKE ?""", block)
    questions = c.fetchall()
    sec_print(questions[0][0])
    sec_print(questions[0][1])
    #print( unicode(questions[0][1]), "utf-8", errors="ignore" )
    counter = 0
    error = 0
    for i in range(1, len(questions)):
        sec_print(questions[i][0] + "\n")   #codice
        sec_print(questions[i][1] + "\n")   #domanda
        sec_print(questions[i][2] + "\n")   #a
        sec_print(questions[i][3] + "\n")   #b
        sec_print(questions[i][4] + "\n")   #c
        sec_print(questions[i][5] + "\n")   #d
        reply = input("risposta: ")
        if reply == questions[i][6]:
            sec_print("Corretto\n")
            counter += 1
        else:
            sec_print("La risposta corretta è " + str(questions[i][6]) + "\n")
            error = 1
            break
    return counter, error


def random_question(rows, c):
    pos = (random.randrange(1, rows), )
    c.execute("""select *
                from domande
                where rowid == ?""", pos)
    question = c.fetchone()
    type = return_type(question[0])

    if type == "n":
        sec_print(question[0] + "\n")   #codice
        sec_print(question[1] + "\n")   #domanda
        sec_print(question[2] + "\n")   #a
        sec_print(question[3] + "\n")   #b
        sec_print(question[4] + "\n")   #c
        sec_print(question[5] + "\n")   #d
        reply = input("risposta: ")
        if reply == question[6]:
            sec_print("Corretto\n")
            return 1, 0
        else:
            sec_print("La risposta corretta è " + str(question[6]) + "\n")
            return 0, 1
    else:
        return special_handle(question[0], c)


if __name__ == '__main__':
    win_unicode_console.enable()
    conn = sqlite3.connect('question.db')
    c = conn.cursor()
    c.execute("""select count(distinct(codice))
                    from domande""")
    rows = c.fetchone()
    counter = 0
    for i in range(0, 3):
            result, error = random_question(rows[0], c)

            if result >= 0:
                counter += result
                time.sleep(2)
            elif result == None:
                time.sleep(2)

            if error == 1:
                sec_print("Fine\n" + str(counter)+ " risposte corrette\n")
                break
    conn.close()