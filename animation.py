import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

with open('bilard.txt', 'r') as f:
    data = f.readlines()

n = len(data[0].split()) // 4
friction = 0.001
positions = []
#Istotna część dla animacji

for i in range(len(data)):
    row = data[i].split()
    x, y, vx, vy = [float(row[j * 4]) for j in range(n)], [float(row[j * 4 + 1]) for j in range(n)], [float(row[j * 4 + 2]) for j in range(n)], [float(row[j * 4 + 3]) for j in range(n)]

    if i < len(data) - 1:
        next_row = data[i + 1].split()
        d = np.sqrt((float(next_row[0]) - x[0]) ** 2 + (float(next_row[1]) - y[0]) ** 2)
        v = np.sqrt(vx[0] ** 2 + vy[0] ** 2)
        t = (v - np.sqrt(v ** 2 - 2 * friction * d)) / friction

    positions.append((x.copy(), y.copy()))

    n_frames = int(t * 120)

    for j in range(1, n_frames + 1):
        t_j = j / 120
        x_j = x + np.array(vx) * t_j
        y_j = y + np.array(vy) * t_j
        x_j -= 0.5 * friction * t_j ** 2 * np.sign(vx)
        y_j -= 0.5 * friction * t_j ** 2 * np.sign(vy)

        positions.append((x_j.copy(), y_j.copy()))

fig, ax = plt.subplots()

#Wizualia

table_width = 10
table_height = 10
frame_thickness = 0.2
frame_color = '#1b4d3f'
cushion_thickness = 0.4
cushion_color = '#4f2d00'
colors = ['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082', '#800080', '#00FFFF', '#FF00FF', '#FFC0CB', '#00FF00', '#000000', '#800000', '#808000', '#008080']

ax.set_facecolor(cushion_color)
offset = 1.0

ax.set_xlim(-offset, table_width + offset)
ax.set_ylim(-offset, table_height + offset)

frame = plt.Rectangle((0, 0), table_width, table_height, color=frame_color, zorder=0)
ax.add_patch(frame)

frame_lines = [plt.Line2D([0, table_width], [0, 0], color='black', linewidth=0.5),
               plt.Line2D([0, table_width], [table_height, table_height], color='black', linewidth=0.5),
               plt.Line2D([0, 0], [0, table_height], color='black', linewidth=0.5),
               plt.Line2D([table_width, table_width], [0, table_height], color='black', linewidth=0.5)]

for line in frame_lines:
    ax.add_artist(line)

cushion_colors = ['#8B4513', '#8B4513', '#8B4513', '#8B4513']
cushions = [plt.Rectangle((0, 0), table_width, cushion_thickness, color=color, zorder=1) for color in cushion_colors]
for cushion in cushions:
    ax.add_patch(cushion)

pocket_colors = ['#000000', '#000000', '#000000', '#000000']
pocket_positions = [(0, 0), (table_width, 0), (0, table_height), (table_width, table_height)]
pockets = [plt.Circle(position, 0.8, color=color, zorder=2) for position, color in zip(pocket_positions, pocket_colors)]
for pocket in pockets:
    ax.add_patch(pocket)

corner_pocket_radius = 0.8 / np.sqrt(2)
corner_pocket_positions = [(0, 0), (table_width, 0), (0, table_height), (table_width, table_height)]
corner_pocket_colors = ['#000000', '#000000', '#000000', '#000000']
corner_pockets = [plt.Circle(position, corner_pocket_radius, color=color, zorder=2) for position, color in zip(corner_pocket_positions, corner_pocket_colors)]
for corner_pocket in corner_pockets:
    ax.add_patch(corner_pocket)

bile_radius = 0.5
bile_edge_color = '#000000'
bile_fill_color = colors[:n]
bile_patches = [plt.Circle((x[i], y[i]), bile_radius, edgecolor=bile_edge_color, facecolor=color) for i, color in enumerate(bile_fill_color)]
for patch in bile_patches:
    ax.add_patch(patch)

small_radius = 0.25
small_fill_color = '#FFFFFF'
number_color = '#000000'
small_patches = [plt.Circle((x[i], y[i]), small_radius, edgecolor=number_color, facecolor=small_fill_color, zorder=3) for i in range(n)]
for patch in small_patches:
    ax.add_patch(patch)

numbers = [plt.Text(x[i], y[i], str(i + 1), color=number_color, ha='center', va='center', zorder=4) for i in range(n)]
for number in numbers:
    ax.add_artist(number)


def animate(i):
    for j in range(n):
        bile_patches[j].center = (positions[i][0][j], positions[i][1][j])
        small_patches[j].center = (positions[i][0][j], positions[i][1][j])
        numbers[j].set_position((positions[i][0][j], positions[i][1][j]))
    return bile_patches + small_patches + numbers


#num_frames = len(positions)
num_frames = len(data[0])
ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=8.33, blit=True, repeat=False)
plt.show()
ani.save('animation.gif', writer='pillow')

