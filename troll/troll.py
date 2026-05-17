from tkinter import *
from random import randint, choice
from winsound import *

score = 0
# область функций
def hit():
    global score
    score += 1
    update_points()
    play_sound_ok()
    spuwn()

def mouse_motion(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

def spuwn():
    x = randint(1, game_width - npc_width)
    y = randint(1, game_height - npc_height)
    if abs(mouse_x - x) < 100 and abs(mouse_y - y) < 100:
        x = randint(1, game_width - npc_width)  # Исправлено: было x, теперь 1
        y = randint(1, game_height - npc_height)  # Исправлено: было x, теперь 1
        print('новое место')
    canvas.moveto(npc_id, x, y)
    if randint(1, 50) == 1:
        show_scr()

def show_scr():
    global gameover
    gameover = True
    canvas.itemconfig(screamer_id, state='normal')
    # Скрываем скример через 1 секунду
    canvas.after(1000, lambda: canvas.itemconfig(screamer_id, state='hidden'))

def game_update():
    if not gameover:  # Исправлено: обновляем только если игра не окончена
        spuwn()
        canvas.after(1000, game_update)

def miss_click():
    global score
    score -= 1
    if score < 0:
        score = 0
        game_over()
    else:
        update_points()
    play_sound_fail()

def play_sound_ok():
    files = []
    for i in range(1, 7):
        files.append(f'hit{i}.wav')
    file = choice(files)
    PlaySound(file, SND_ASYNC | SND_FILENAME)

def play_sound_fail():
    files = []
    for i in range(1, 8):
        files.append(f'fail{i}.wav')  # Исправлено: отступ
    file = choice(files)  # Исправлено: отступ
    PlaySound(file, SND_ASYNC | SND_FILENAME)

def update_points():
    canvas.itemconfig(text_id, text=f'Очки:{score}')  # Исправлено: было speed, нужно score

def game_over():
    global gameover
    gameover = True
    canvas.itemconfig(text_id, text='Потрачено')
    PlaySound('fail_end.mp3', SND_ASYNC | SND_FILENAME)

def mouse_click(e):
    if gameover:
        return
    if collision_detection(e.x, e.y):
        hit()
    else:
        miss_click()

def collision_detection(x, y):
    position = canvas.coords(npc_id)
    left = position[0]
    top = position[1]
    right = position[0] + npc_width
    bottom = position[1] + npc_height
    return left <= x <= right and top <= y <= bottom

# область глобальных переменных
game_width = 720
game_height = 720
npc_width = 120
npc_height = 95
score = 0  # Исправлено: было speed, теперь score
mouse_x = mouse_y = 0
gameover = False
screamers = ['monke.png', 'scary_manke.png', 'cool_monky.png']

# создание и обработка окна
window = Tk()
window.title('проучи тролля')
window.resizable(width=False, height=False)
canvas = Canvas(window, width=game_width, height=game_height)

# виджеты
npc_image = PhotoImage(file='trollface.png')
npc_id = canvas.create_image(0, 0, image=npc_image, anchor=NW)

# обратный вызов
canvas.bind('<Button-1>', mouse_click)  # Исправлено: '<Button>' на '<Button-1>'
canvas.bind('<Motion>', mouse_motion)

text_id = canvas.create_text(game_width - 10, 10,
                           fill='black',
                           font='Times 20 bold',
                           text=f'Очки:{score}',
                           anchor=NE)

screamer_image = PhotoImage(file=choice(screamers))
screamer_id = canvas.create_image(0, 0,
                                image=screamer_image,
                                anchor=NW)
canvas.itemconfig(screamer_id, state='hidden')

canvas.pack()
game_update()  # Запускаем обновление игры
window.mainloop()