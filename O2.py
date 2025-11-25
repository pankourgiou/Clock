import tkinter as tk
import math
from datetime import datetime
import time

# ===== USER EQUATIONS (as provided) =====
equations = {
    12: "E = E^origami",
    1:  "E = E^sofia",
    2:  "E = E^valis",
    3:  "E = E^Rosa",
    4:  "E = E^Ion",                     # no label supplied for 4 o'clock -> left blank
    5:  "E = E^Anna",
    6:  "E = E^lne",
    7:  "E = E^Ra",
    8:  "E = E^Osiris",
    9:  "E = E^Christina",
    10: "E = E^Alexandra",
    11: "E = E^Claymotion",
}

NOTE_TEXT = (
    "Setting: Origami = Sofia = Valis = Rosa = Anna = lne = Ra = "
    "Osiris = Christina = Alexandra = Claymotion = Ion = 1"
)

# ===== CONFIG =====
CANVAS_SIZE = 600
PADDING_RIGHT = 260   # extra space to the right for note/outside content
WIDTH = CANVAS_SIZE + PADDING_RIGHT
HEIGHT = CANVAS_SIZE
CENTER = CANVAS_SIZE // 2
RADIUS = int(CANVAS_SIZE * 0.42)  # leave some margin

# ===== SETUP TK =====
root = tk.Tk()
root.title("Working Analog Clock with Equations")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Draw outer circle (clock face)
canvas.create_oval(
    CENTER - RADIUS, CENTER - RADIUS,
    CENTER + RADIUS, CENTER + RADIUS,
    width=4, outline="black", fill="#ffffff", tags="face"
)

# Draw minute/second tick marks
for i in range(60):
    angle = math.radians(i * 6 - 90)
    outer = RADIUS
    if i % 5 == 0:
        inner = RADIUS - 18
        width = 3
    else:
        inner = RADIUS - 10
        width = 1
    x1 = CENTER + math.cos(angle) * inner
    y1 = CENTER + math.sin(angle) * inner
    x2 = CENTER + math.cos(angle) * outer
    y2 = CENTER + math.sin(angle) * outer
    canvas.create_line(x1, y1, x2, y2, width=width, tags="face")

# Place hour labels (your equations) around the face
label_radius = RADIUS - 48
for hour in range(1, 13):
    label = equations.get(hour, "")
    angle = math.radians((hour % 12) * 30 - 90)
    x = CENTER + math.cos(angle) * label_radius
    y = CENTER + math.sin(angle) * label_radius
    # use center anchor so multi-word fits nicely; smaller font if long
    font_size = 11
    if len(label) > 18:
        font_size = 9
    canvas.create_text(x, y, text=label, font=("Arial", font_size, "bold"), tags="face")

# Place the note OUTSIDE the clock (to the right)
note_x = CANVAS_SIZE + 20
note_y = 30
canvas.create_text(note_x, note_y, anchor="nw", text=NOTE_TEXT,
                   font=("Arial", 11, "italic"), width=PADDING_RIGHT - 40)

# small center hub
canvas.create_oval(CENTER-6, CENTER-6, CENTER+6, CENTER+6, fill="black", tags="face")

# ===== HANDS: draw & update =====
# We'll re-create hands each frame and tag them "hands" so we can delete easily.
def update_clock():
    canvas.delete("hands")
    # get current time with fractional seconds for smooth motion
    now = datetime.now()
    sec = now.second + now.microsecond / 1_000_000
    minute = now.minute + sec / 60.0
    hour = (now.hour % 12) + minute / 60.0

    # angles (radians); 12 o'clock = -90 deg
    sec_angle = math.radians(sec * 6 - 90)
    min_angle = math.radians(minute * 6 - 90)
    hour_angle = math.radians(hour * 30 - 90)

    # hand lengths
    sec_len = RADIUS - 28
    min_len = RADIUS - 50
    hour_len = RADIUS - 90

    # hand endpoints
    hx = CENTER + math.cos(hour_angle) * hour_len
    hy = CENTER + math.sin(hour_angle) * hour_len
    mx = CENTER + math.cos(min_angle) * min_len
    my = CENTER + math.sin(min_angle) * min_len
    sx = CENTER + math.cos(sec_angle) * sec_len
    sy = CENTER + math.sin(sec_angle) * sec_len

    # draw hour hand
    canvas.create_line(CENTER, CENTER, hx, hy, width=6, capstyle="round",
                       tags="hands")
    # draw minute hand
    canvas.create_line(CENTER, CENTER, mx, my, width=4, capstyle="round",
                       tags="hands")
    # draw second hand (thin)
    canvas.create_line(CENTER, CENTER, sx, sy, width=2, capstyle="round",
                       tags="hands")
    # small tail on second hand for aesthetics
    tail_x = CENTER - math.cos(sec_angle) * 20
    tail_y = CENTER - math.sin(sec_angle) * 20
    canvas.create_line(tail_x, tail_y, CENTER, CENTER, width=2, capstyle="round",
                       tags="hands")

    # optional: digital time readout below the clock
    canvas.delete("digital")
    digital_text = now.strftime("%I:%M:%S %p")
    canvas.create_text(CENTER, CENTER + RADIUS + 28, text=digital_text,
                       font=("Arial", 12), tags=("digital",))

    # schedule next update for smooth animation
    root.after(50, update_clock)  # ~20 FPS for smooth second hand

# initial call
update_clock()

# run
root.mainloop()
