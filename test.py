import pygame
import imageio
from PIL import Image

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# 加载gif图像
gif_path = '1.gif'
frames = imageio.mimread(gif_path)

# 将每一帧转换为Surface对象
surfaces = []
for frame in frames:
    image = Image.fromarray(frame)
    surface = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    surfaces.append(surface)

# 播放动画
frame_index = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制当前帧
    screen.fill((0, 0, 0))
    screen.blit(surfaces[frame_index], (100, 100))
    pygame.display.flip()

    # 延迟一段时间
    pygame.time.delay(100)  # 每帧之间的延迟时间，可以根据需要调整

    # 切换到下一帧
    frame_index = (frame_index + 1) % len(surfaces)

    # 控制帧率
    clock.tick(15)  # 帧率，可以根据需要调整

# 退出Pygame
pygame.quit()
