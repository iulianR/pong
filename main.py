import pygame
import sys

# Colors in RGB format
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)


class PongBall:
    """ Ball object """
    SPEED = 3
    SIZE = 15

    def __init__(self):
        # (x, y) position
        self.x = PongGame.WIDTH / 2
        self.y = PongGame.HEIGHT / 2

        # Direction
        self.direction_x = -1
        self.direction_y = 1

    """ Check if a pad has been hit """
    def hit_pad(self, pad):
        if self.x > pad.x and self.x < pad.x + pad.WIDTH:
            if self.y > pad.y and self.y < pad.y + pad.HEIGHT:
                return True

        return False

    """ Reverse direction after a hit """
    def update_direction_after_hit(self):
        self.direction_x *= -1

    """ Update current position based on direction and speed """
    def update(self):
        self.x += self.direction_x * self.SPEED
        self.y += self.direction_y * self.SPEED

        # Check for collision with top/bottom border. If the border has been hit
        # reverse ball's direction
        if self.y <= 0 or self.y + self.SIZE >= PongGame.HEIGHT:
            self.direction_y *= -1

    """ Draw the ball at it's position """
    def render(self, background):
        pygame.draw.rect(background,
                         COLOR_WHITE,
                         pygame.Rect(self.x, self.y, self.SIZE, self.SIZE))


class PongPad:
    SPEED = 5
    WIDTH = 15
    HEIGHT = 80

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        self.y -= self.SPEED

        # Stop at top border
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += self.SPEED

        # Stop at bottom border
        if self.y + self.HEIGHT > PongGame.HEIGHT:
            self.y -= self.SPEED

    """ Draw the paddle at it's position """
    def render(self, background):
        pygame.draw.rect(background,
                         COLOR_WHITE,
                         pygame.Rect(self.x, self.y, PongPad.WIDTH, PongPad.HEIGHT))


class PongGame:
    FPS = 60
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        # Pads and ball
        self.left_pad = PongPad(0, self.HEIGHT / 2)
        self.right_pad = PongPad(self.WIDTH - PongPad.WIDTH, self.HEIGHT / 2)
        self.ball = PongBall()

        # Clock used to limit FPS
        self.clock = pygame.time.Clock()

        # Initialize a screen for display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = None

    def start(self):
        # Fill background
        self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.background = self.background.convert()
        self.background.fill(COLOR_BLACK)

        # Blit everything to screen
        self.screen.blit(self.background, (0, 0))
        # Update the screen
        pygame.display.flip()

        # Main loop
        while True:
            # Check for Quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check for key presses and update paddles accordingly
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_w]:
                self.left_pad.move_up()
            if keys_pressed[pygame.K_s]:
                self.left_pad.move_down()
            if keys_pressed[pygame.K_UP]:
                self.right_pad.move_up()
            if keys_pressed[pygame.K_DOWN]:
                self.right_pad.move_down()

            # Update game state
            self.update()

            # Render current game state
            self.render()

    def update(self):
        # Used to slow things down so game runs at the same FPS on all computers
        self.clock.tick(PongGame.FPS)

        # Check if the ball hit a paddle. If it did, update ball's direction
        if self.ball.hit_pad(self.left_pad) or self.ball.hit_pad(self.right_pad):
            self.ball.update_direction_after_hit()

        # Update ball position based on it's direction and speed
        self.ball.update()

    def render(self):
        self.background.fill(COLOR_BLACK)

        self.left_pad.render(self.background)
        self.right_pad.render(self.background)
        self.ball.render(self.background)

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


def main():
    # Initialize imported pygame modules
    pygame.init()

    # Set the window's caption
    pygame.display.set_caption("Pong")

    # Create new game instance and start the game
    game = PongGame()
    game.start()


if __name__ == '__main__':
    main()
