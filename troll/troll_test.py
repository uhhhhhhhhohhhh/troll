from tkinter import *
from random import randint, choice
from winsound import *

# Область функций
def hit():
    global speed
    score += 1
    play_sound_ok()
    update_points()
    spawn()


def mouse_motion(event):   #координаты курсора (нужны для определения колизии с троллем и квадратом)
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

def spawn():
    global x1, y1
    x1 = randint(0, game_width - bros_width)
    y1 = randint(0, game_height - bros_height)

    x = randint(0, game_width - npc_width)
    y = randint(0, game_height - npc_height)

    # Проверка расстояния до курсора
    while abs(mouse_x - x) < 100 and abs(mouse_y - y) < 100:
        x = randint(0, game_width - npc_width)
        y = randint(0, game_height - npc_height)

    canvas.moveto(npc_id, x, y)
    canvas.moveto(scary_bro, x1, y1)

def show_scr():
    global gameover
    gameover = True
    canvas.itemconfig(screamer_id, state='normal')

def game_update():
    spawn()
    canvas.after(1000, game_update)

def miss_click():
    global speed
    score -= 1
    if score < 0:
        score = 0
        game_over()
    else:
        update_points()
    play_sound_fail()

def play_sound_fail():
    PlaySound('fail4.wav', SND_ASYNC | SND_FILENAME)
def play_sound_ok():
    PlaySound('fail1.wav',SND_ASYNC | SND_FILENAME)
def update_points():
    canvas.itemconfig(text_id, text=f'Очки: {speed}')

def game_over():
    global gameover
    gameover = True
    canvas.itemconfigure(text_id, text='Потрачено')
    PlaySound('fail_end.mp3', SND_ASYNC | SND_FILENAME)

def mouse_click(e):
    global speed
    if gameover:
        return

    if collision_detection(e.x, e.y):   #попал молодец не попал плохой но если на куб нажать то испугаться можно
        hit()
    elif collision_detection_with_bro(e.x, e.y):  # Исправлено
        show_scr()
    else:
        miss_click()

def collision_detection(x, y):   #проверка столкновения курсора с троллем
    position = canvas.coords(npc_id)
    left = position[0]
    top = position[1]
    right = position[0] + npc_width
    bottom = position[1] + npc_height
    return (left <= x <= right and top <= y <= bottom)
def update_points():
    canvas.itemconfig(text_id, text=f'Очки:{speed}')
def collision_detection_with_bro(x, y):  #проверка столкновения курсора с квадратом
    position1 = canvas.coords(scary_bro)
    left1 = position1[0]
    top1 = position1[1]
    right1 = position1[0] + bros_width
    bottom1 = position1[1] + bros_height
    return (left1 <= x <= right1 and top1 <= y <= bottom1)

# Область глобальных переменных
game_width = 720
game_height = 720
npc_width = 120
npc_height = 95
bros_width = 50
bros_height = 50
speed = 10
mouse_x = mouse_y = 0

gameover = False

# Создание и обработка окна
window = Tk()
window.title('проучи тролля')
window.resizable(width=False, height=False)
canvas = Canvas(window, width=game_width, height=game_height)
canvas.pack()

# Виджеты
npc_image = PhotoImage(file='trollface.png')
npc_id = canvas.create_image(0, 0, image=npc_image, anchor=NW)

#scary_bro
x1, y1 = 0, 0
scary_bro = canvas.create_rectangle(x1, y1, x1 + bros_width, y1 + bros_height, fill='red')

screamers = ['monke.png', 'scary_manke.png', 'cool_monky.png']
screamer_image = PhotoImage(file=choice(screamers))
screamer_id = canvas.create_image(0, 0, image=screamer_image, anchor=NW)
canvas.itemconfig(screamer_id, state='hidden')

# Обратный вызов
game_update()
canvas.bind('<Button>', mouse_click)
canvas.bind('<Motion>', mouse_motion)
text_id = canvas.create_text(game_width - 10, 10, fill='black', font='Times 20 bold', text=f'Очки: {speed}', anchor=NE)

# Запуск приложения
window.mainloop()



