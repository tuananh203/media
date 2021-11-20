import pygame
import random
from pygame import mixer


class Game:

    def __init__(self):
        pygame.init()  # Init pygame
        self.FPS = 120
        self.fpsClock = pygame.time.Clock()
        self.xScreen, self.yScreen = 640, 800  # Screen create
        self.VBullet = 15  # Tốc độ Bullet
        self.VPlanes = 15  # Tốc độ Planes
        self.VEnemy = 6  # Tốc độ Enemy
        self.scores = 0  # Điểm số
        self.numberEnemy = 2  # Số lượng enemy trong một screen
        self.numberBullet = 6  # Số bullet trong một screen
        self.linkBackGround = './hinh-nen-vu-tru-khong-gian-bi-an.jpg'  # Đường dẫn ảnh background
        self.linkEnemy = './enemy.png'  # Đường dẫn ảnh Enemy
        self.linkPlanes = './planes.png'  # Đường dẫn ảnh Planes
        self.musicBullet = mixer.Sound('./laser.wav')
        self.musicBackground = mixer.Sound('./Victory.wav')
        self.musicTheme = mixer.Sound('./musictheme.wav')
        self.musicEnd = mixer.Sound('./musicend.mp3')
        self.sizexPlanes, self.sizeyPlanes = 80, 80
        self.xPlanes, self.yPlanes = self.xScreen / \
                                     2 - 45, self.yScreen - 100  # Khởi tao vị trí ban đầu planes
        self.screen = pygame.display.set_mode(
            (self.xScreen, self.yScreen))  # Khởi tao kích thước màn hình
        pygame.display.set_caption("Group 15 - Space Invaders")
        self.background = pygame.image.load(self.linkBackGround)
        icon = pygame.image.load(self.linkPlanes)
        pygame.display.set_icon(icon)  # Set icon cho screen
        self.gamerunning = True
        self.listBullet = []
        self.listEnemy = []
        self.YGameOver = 0
        self.K_DOWN = self.K_UP = self.K_LEFT = self.K_RIGHT = False

    def show_score(self, x, y, scores, size):  # Hiển thị điểm
        font = pygame.font.SysFont("comicsansms", size)
        score = font.render(str(scores), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def image_draw(self, url, xLocal, yLocal, xImg, yImg):  # In ra ngoài hình ảnh
        PlanesImg = pygame.image.load(url)
        PlanesImg = pygame.transform.scale(
            PlanesImg, (xImg, yImg))  # change size image
        self.screen.blit(PlanesImg, (xLocal, yLocal))

    def enemy(self):  # Quản lý Enemy
        for count, i in enumerate(self.listEnemy):
            xEnemy = i["xEnemy"]  # Lấy toạn độ X
            yEnemy = i["yEnemy"]  # Lấy toạn độ Y
            if xEnemy < 0 or xEnemy > self.xScreen - self.sizexPlanes:  # Nếu chạm vào hai bên phải trái
                # thì đổi hướng
                self.listEnemy[count]["direction"] = not self.listEnemy[count]["direction"]
            self.image_draw(self.linkEnemy, xEnemy, yEnemy, self.sizexPlanes,
                            self.sizeyPlanes)  # In enemy ra màn hình
            self.listEnemy[count]["xEnemy"] = xEnemy + \
                                              (self.VEnemy if self.listEnemy[count]
                                                              ["direction"] == False else -self.VEnemy)
            self.listEnemy[count]["yEnemy"] = yEnemy + \
                                              self.VEnemy / 2.5  # Toạn độ x xông tốc độ Enemy/3
            # Gán giá trị lớn nhất của Enemy theo y
            self.YGameOver = yEnemy if yEnemy > self.YGameOver else self.YGameOver

    def bullet(self):
        for count, i in enumerate(self.listBullet):
            xBullet = i["xBullet"]  # Lấy trục tọa độ theo X
            yBullet = i["yBullet"]  # Lấy trục tọa độ theo X
            self.image_draw(
                './bullet.png', xBullet,
                yBullet, 25, 60)  # In ra bullet
            self.listBullet[count]["yBullet"] = yBullet - \
                                                self.VBullet  # Tiến y vè phía trước
            if yBullet <= 5:  # nếu toạn độ Y phía trên nàm hình thì xóa
                self.listBullet.remove(self.listBullet[count])

    def run(self):
        while self.gamerunning:
            self.screen.blit(self.background, (0, 0))
            mixer.Channel(1).play(self.musicBackground)
            for event in pygame.event.get():  # Bắt các sự kiện
                if event.type == pygame.QUIT:  # sự kiện nhấn thoát
                    self.gamerunning = False
                if event.type == pygame.KEYDOWN:  # sự kiện có phím nhấn xuống
                    if event.key == pygame.K_DOWN:
                        self.K_DOWN = True
                    if event.key == pygame.K_UP:
                        self.K_UP = True
                    if event.key == pygame.K_LEFT:
                        self.K_LEFT = True
                    if event.key == pygame.K_RIGHT:
                        self.K_RIGHT = True
                    if event.key == pygame.K_SPACE:
                        mixer.Channel(2).play(self.musicBullet)
                        if len(self.listBullet) < self.numberBullet:
                            self.listBullet.append({  # Add Thêm bullet
                                "xBullet": self.xPlanes + self.sizexPlanes / 2 - 25,
                                "yBullet": self.yPlanes - self.sizexPlanes / 2,
                            })
                if event.type == pygame.KEYUP:  # sự kiện thả phím
                    if event.key == pygame.K_DOWN:
                        self.K_DOWN = False
                    if event.key == pygame.K_UP:
                        self.K_UP = False
                    if event.key == pygame.K_LEFT:
                        self.K_LEFT = False
                    if event.key == pygame.K_RIGHT:
                        self.K_RIGHT = False
            if self.K_DOWN:
                self.yPlanes = self.yPlanes + self.VPlanes / 2  # Tiến lên
            if self.K_UP:
                self.yPlanes = self.yPlanes - self.VPlanes / 2  # Tiến xuống
            if self.K_LEFT:
                self.xPlanes = self.xPlanes - self.VPlanes  # Tiến trái
            if self.K_RIGHT:
                self.xPlanes = self.xPlanes + self.VPlanes  # Tiến phải

            # Kiểm tra có vượt quá giới hạn màn hình  và sát về lề màn hình
            self.xPlanes = 0 if self.xPlanes < 0 else self.xPlanes
            self.xPlanes = self.xScreen - self.sizexPlanes if self.xPlanes + \
                                                              self.sizexPlanes > self.xScreen else self.xPlanes
            self.yPlanes = 0 if self.yPlanes < 0 else self.yPlanes
            self.yPlanes = self.yScreen - self.sizeyPlanes if self.yPlanes + \
                                                              self.sizeyPlanes > self.yScreen else self.yPlanes

            # nếu số lượng Enemy ít hơn self.numberEnemy thì tạo thêm
            if len(self.listEnemy) < self.numberEnemy:
                self.listEnemy.append({
                    "xEnemy": random.randint(0, self.xScreen - self.sizexPlanes),
                    "yEnemy": random.randint(-50, int(self.yScreen / 8)),
                    "direction": random.choice((True, False))
                })
            listEnemy2 = self.listEnemy
            # Kiểm tra có trúng bullet
            for countEnemy, enemyIteam in enumerate(listEnemy2):
                xEnemy = enemyIteam["xEnemy"]
                yEnemy = enemyIteam["yEnemy"]
                for countBullet, bulletIteam in enumerate(self.listBullet):
                    xBullet = bulletIteam["xBullet"]
                    yBullet = bulletIteam["yBullet"]
                    # Kiểm tra bullet có nằm giữa Enemy theo trục x không
                    isInX = xEnemy <= xBullet <= xEnemy + self.sizexPlanes
                    # Kiểm tra bullet có nằm giữa Enemy theo trục y không
                    isInY = yEnemy <= yBullet <= yEnemy + self.sizexPlanes / 1.2
                    if isInX and isInY:  # nếu nằm giữa
                        self.listEnemy.remove(
                            self.listEnemy[countEnemy])  # Xóa Enemy
                        self.listBullet.remove(
                            self.listBullet[countBullet])  # Xóa Bullet
                        self.scores = self.scores + 1  # CỘng thêm điểm
                        break
            if self.numberEnemy < 7:
                self.numberEnemy = (self.scores / 15) + 2
            if self.YGameOver > self.yScreen - 50:  # Nếu Enemy về gần đích
                newGame = False
                mixer.stop()
                self.musicEnd.play(1000000)
                while True:
                    for event in pygame.event.get():  # Nếu nhấn
                        if event.type == pygame.QUIT:  # Thoát
                            self.gamerunning = False
                            newGame = True
                            mixer.stop()
                            break
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Thoát
                            newGame = True
                            mixer.stop()
                            break
                    if newGame:  # Thoát vòng while để vào game mới
                        break
                    self.show_score(100, 100, "Scores:{}".format(
                        self.scores), 40)  # In điểm
                    self.show_score(self.xScreen / 2 - 150, self.yScreen / 2 - 100,
                                    "GAME OVER", 50)  # In Thông báo thua
                    self.show_score(self.xScreen / 2 - 120, self.yScreen / 2,
                                    "Press Space to play again", 20)
                    pygame.display.update()
                    self.fpsClock.tick(self.FPS)
                self.scores = 0  # Trả các biến về giá trị ban đầu
                self.listBullet = []
                self.listEnemy = []
                self.YGameOver = 0
                self.xPlanes, self.yPlanes = self.xScreen / \
                                             2 - 45, self.yScreen - 100  # Khởi tao vị trí ban đầu planes
                self.K_DOWN = self.K_UP = self.K_LEFT = self.K_RIGHT = False
            self.show_score(10, 10, "Scores:{}".format(self.scores), 35)
            self.show_score(self.xScreen - 100, 20, "Group 15", 15)
            self.enemy()
            self.bullet()
            self.image_draw(self.linkPlanes, self.xPlanes,
                            self.yPlanes, self.sizexPlanes, self.sizeyPlanes)
            pygame.display.update()  # Update
            self.fpsClock.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
