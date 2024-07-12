import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
print('Server has started....')

questions = ["What is the Italian word for PIE? \n a.Mozarella\n b.Pasty\n_c.Patty\n d.Pizza",
             "Water boils at 212 Units at which scale? \n a.Fahrenheit\n b Celsius.\n c.Rankine \n d.Kelvin",
             "Which sea creature has three hearts? \n a.Dolphin\n b.Octopus \n c.Walrus\nd.Seal",
             "Who was the character famous in our childhood rhymes associated with a lamb? \n a.Mary\n b.Jack\n c.Johnny\n d.Mukesh",
             "How many bones does an adult human have? \n a.206\n b.208\n c.201\n d.196",]
answers = ['d', 'a', 'b', 'a', 'a']

def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

def clientthread(conn):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d.".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                    remove_question(index)
                    index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
                break
        except:
            continue


    

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    new_thread = Thread(target=clientthread, args=(conn,))
    new_thread.start()