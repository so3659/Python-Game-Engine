import pygame
import random

# 게임 객체 클래스
class GameObject:
    def __init__(self, x, y, size, color, velocity):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.velocity = velocity

    def move(self, screen_width, screen_height):
        # 객체 이동
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # 벽과 충돌 감지 및 반사 운동 처리
        if self.x <= 0 or self.x + self.size >= screen_width:
            self.velocity[0] = -self.velocity[0]
        if self.y <= 0 or self.y + self.size >= screen_height:
            self.velocity[1] = -self.velocity[1]

    def draw(self, screen):
        # 객체 그리기
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# 플레이어 클래스
class Player(GameObject):
    def __init__(self, x, y, size, color, velocity):
        super().__init__(x, y, size, color, velocity)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5

# 게임 엔진 클래스
class GameEngine:
    def __init__(self, title, width, height, sound_file):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.sound = pygame.mixer.Sound(sound_file)
        self.objects = [GameObject(random.randint(0, width - 50), random.randint(0, height - 50),
                                   50, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                   [random.randint(-2, 2), random.randint(-2, 2)]) for _ in range(5)]
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.screen.fill((0, 0, 0))
            for obj in self.objects:
                obj.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def update(self):
        for obj in self.objects:
            obj.move(self.width, self.height)
        
        # 충돌 처리
        for i, obj1 in enumerate(self.objects):
            for j, obj2 in enumerate(self.objects):
                if i != j and self.check_collision(obj1, obj2):
                    self.handle_collision(obj1, obj2)

    def check_collision(self, obj1, obj2):
        # 충돌 감지 로직
        return (obj1.x < obj2.x + obj2.size and obj1.x + obj1.size > obj2.x and
                obj1.y < obj2.y + obj2.size and obj1.y + obj1.size > obj2.y)


    def handle_collision(self, obj1, obj2):
        # 충돌 시 가속도를 정의합니다.
        acceleration = 0.1
        # 객체 간 중첩(overlap)을 계산합니다.
        overlap_x = max(0, min(obj1.x + obj1.size, obj2.x + obj2.size) - max(obj1.x, obj2.x))
        overlap_y = max(0, min(obj1.y + obj1.size, obj2.y + obj2.size) - max(obj1.y, obj2.y))

        # 두 객체가 x축과 y축에서 모두 중첩되었다면 충돌이 있었다고 판단합니다.
        if overlap_x > 0 and overlap_y > 0:
            # 충돌 반응을 위해 속도를 반전시킵니다.
            if overlap_x < overlap_y:
                # x축 기준 충돌 반응
                if obj1.velocity[0] != 0:
                    obj1.velocity[0] = -(obj1.velocity[0] + acceleration * (obj1.velocity[0]/abs(obj1.velocity[0])))
                if obj2.velocity[0] != 0:
                    obj2.velocity[0] = -(obj2.velocity[0] + acceleration * (obj2.velocity[0]/abs(obj2.velocity[0])))
                # 겹치는 부분을 해결합니다.
                correction = overlap_x / 2
                if obj1.x < obj2.x:
                    obj1.x -= correction
                    obj2.x += correction
                else:
                    obj1.x += correction
                    obj2.x -= correction
            else:
                # y축 기준 충돌 반응
                if obj1.velocity[1] != 0:
                    obj1.velocity[1] = -(obj1.velocity[1] + acceleration * (obj1.velocity[1]/abs(obj1.velocity[1])))
                if obj2.velocity[1] != 0:
                    obj2.velocity[1] = -(obj2.velocity[1] + acceleration * (obj2.velocity[1]/abs(obj2.velocity[1])))
                # 겹치는 부분을 해결합니다.
                correction = overlap_y / 2
                if obj1.y < obj2.y:
                    obj1.y -= correction
                    obj2.y += correction
                else:
                    obj1.y += correction
                    obj2.y -= correction
        # 속도 계산 및 색 변경 로직
        speed1 = self.calculate_speed(obj1.velocity)
        speed2 = self.calculate_speed(obj2.velocity)
        if speed1 > speed2:
            obj2.color = obj1.color
        else:
            obj1.color = obj2.color
            # 충돌 시 사운드 재생
            self.sound.play()

    def calculate_speed(self, velocity):
        # 속도 계산
        return (velocity[0]**2 + velocity[1]**2)**0.5

# 게임 엔진 인스턴스 생성 및 실행
if __name__ == "__main__":
    game = GameEngine("Game", 800, 600, 'bgm2.mp3')
    # 플레이어 객체를 추가합니다.
    player = Player(400, 300, 50, (255, 255, 255), [0, 0])
    game.objects.append(player)

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

        # 플레이어의 키 입력 처리
        player.handle_keys()

        game.update()
        game.screen.fill((0, 0, 0))
        
        # 모든 게임 객체를 그립니다.
        for obj in game.objects:
            obj.draw(game.screen)
        
        pygame.display.flip()
        game.clock.tick(60)

    pygame.quit()