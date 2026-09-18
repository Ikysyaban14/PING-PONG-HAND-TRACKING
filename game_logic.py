import random
import pygame


class PongGame:
    """
    Logika utama game Pong:
    - Paddle pemain
    - Paddle AI
    - Bola
    - Pantulan bola
    - Sistem skor
    - Indikator status hand tracking
    """

    def __init__(self, width=1000, height=600):
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pong Hand Tracking")

        self.clock = pygame.time.Clock()

        self.background_color = (20, 20, 20)
        self.white = (245, 245, 245)
        self.green = (80, 220, 120)
        self.red = (230, 80, 80)
        self.gray = (150, 150, 150)

        self.paddle_width = 18
        self.paddle_height = 120
        self.paddle_speed = 600

        self.ball_size = 18
        self.ball_speed_x = 450
        self.ball_speed_y = 300

        self.player_paddle = pygame.Rect(
            40,
            height // 2 - self.paddle_height // 2,
            self.paddle_width,
            self.paddle_height,
        )

        self.ai_paddle = pygame.Rect(
            width - 40 - self.paddle_width,
            height // 2 - self.paddle_height // 2,
            self.paddle_width,
            self.paddle_height,
        )

        self.ball = pygame.Rect(
            width // 2 - self.ball_size // 2,
            height // 2 - self.ball_size // 2,
            self.ball_size,
            self.ball_size,
        )

        self.ball_velocity = pygame.Vector2(
            self.ball_speed_x,
            random.choice([-self.ball_speed_y, self.ball_speed_y]),
        )

        self.player_score = 0
        self.ai_score = 0

        self.font_score = pygame.font.Font(None, 96)
        self.font_info = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def reset_ball(self, direction):
        """
        Mereset bola ke tengah layar.

        direction:
            1  -> bola bergerak ke kanan
            -1 -> bola bergerak ke kiri
        """
        self.ball.center = (self.width // 2, self.height // 2)

        self.ball_velocity = pygame.Vector2(
            self.ball_speed_x * direction,
            random.choice([-self.ball_speed_y, self.ball_speed_y]),
        )

    def update_player_paddle(self, hand_y_normalized, dt):
        """
        Menggerakkan paddle pemain berdasarkan koordinat Y tangan.

        hand_y_normalized:
            Nilai Y MediaPipe dari 0.0 sampai 1.0.
        """
        if hand_y_normalized is not None:
            target_y = hand_y_normalized * self.height
            target_top = target_y - self.paddle_height // 2

            # Gerakan halus menuju posisi tangan.
            difference = target_top - self.player_paddle.y
            movement = difference * min(1.0, 12.0 * dt)

            self.player_paddle.y += int(movement)

        self.player_paddle.top = max(self.player_paddle.top, 0)
        self.player_paddle.bottom = min(
            self.player_paddle.bottom,
            self.height,
        )

    def update_ai_paddle(self, dt):
        """
        AI sederhana yang mengikuti posisi vertikal bola.
        """
        target_y = self.ball.centery
        difference = target_y - self.ai_paddle.centery

        max_movement = int(self.paddle_speed * 0.75 * dt)

        if abs(difference) <= max_movement:
            self.ai_paddle.centery = target_y
        else:
            self.ai_paddle.centery += (
                max_movement if difference > 0 else -max_movement
            )

        self.ai_paddle.top = max(self.ai_paddle.top, 0)
        self.ai_paddle.bottom = min(
            self.ai_paddle.bottom,
            self.height,
        )

    def update_ball(self, dt):
        """
        Menggerakkan bola dan menangani tabrakan.
        """
        self.ball.x += int(self.ball_velocity.x * dt)
        self.ball.y += int(self.ball_velocity.y * dt)

        # Pantulan atas dan bawah layar.
        if self.ball.top <= 0:
            self.ball.top = 0
            self.ball_velocity.y = abs(self.ball_velocity.y)

        elif self.ball.bottom >= self.height:
            self.ball.bottom = self.height
            self.ball_velocity.y = -abs(self.ball_velocity.y)

        # Tabrakan dengan paddle pemain.
        if (
            self.ball.colliderect(self.player_paddle)
            and self.ball_velocity.x < 0
        ):
            self.ball.left = self.player_paddle.right
            self.ball_velocity.x = abs(self.ball_velocity.x)

            self._change_ball_angle(self.player_paddle)

        # Tabrakan dengan paddle AI.
        if (
            self.ball.colliderect(self.ai_paddle)
            and self.ball_velocity.x > 0
        ):
            self.ball.right = self.ai_paddle.left
            self.ball_velocity.x = -abs(self.ball_velocity.x)

            self._change_ball_angle(self.ai_paddle)

        # Bola melewati sisi kiri.
        if self.ball.right < 0:
            self.ai_score += 1
            self.reset_ball(direction=1)

        # Bola melewati sisi kanan.
        elif self.ball.left > self.width:
            self.player_score += 1
            self.reset_ball(direction=-1)

    def _change_ball_angle(self, paddle):
        """
        Mengubah sudut pantulan berdasarkan posisi bola
        terhadap bagian tengah paddle.
        """
        paddle_center = paddle.centery
        ball_center = self.ball.centery

        relative_intersection = (
            ball_center - paddle_center
        ) / (self.paddle_height / 2)

        relative_intersection = max(
            -1.0,
            min(1.0, relative_intersection),
        )

        self.ball_velocity.y = relative_intersection * 500

        # Sedikit meningkatkan kecepatan bola setiap terjadi pantulan.
        self.ball_velocity.x *= 1.03

    def update(self, hand_y_normalized, hand_detected, dt):
        """
        Memperbarui seluruh state game.
        """
        if hand_detected:
            self.update_player_paddle(hand_y_normalized, dt)

        self.update_ai_paddle(dt)
        self.update_ball(dt)

    def draw_center_line(self):
        """
        Menggambar garis putus-putus di tengah arena.
        """
        dash_height = 16
        gap = 12

        y = 0
        while y < self.height:
            pygame.draw.rect(
                self.screen,
                self.gray,
                (
                    self.width // 2 - 2,
                    y,
                    4,
                    dash_height,
                ),
            )
            y += dash_height + gap

    def draw_score(self):
        """
        Menggambar skor pemain dan AI.
        """
        player_text = self.font_score.render(
            str(self.player_score),
            True,
            self.white,
        )

        ai_text = self.font_score.render(
            str(self.ai_score),
            True,
            self.white,
        )

        self.screen.blit(
            player_text,
            (self.width // 2 - 100, 40),
        )

        self.screen.blit(
            ai_text,
            (self.width // 2 + 65, 40),
        )

    def draw_hand_status(self, hand_detected):
        """
        Menggambar indikator Hand Detected: YES/NO.
        """
        status_text = "Hand Detected: YES" if hand_detected else "Hand Detected: NO"
        status_color = self.green if hand_detected else self.red

        text_surface = self.font_info.render(
            status_text,
            True,
            status_color,
        )

        self.screen.blit(text_surface, (30, 20))

    def draw(self, hand_detected):
        """
        Menggambar seluruh elemen game.
        """
        self.screen.fill(self.background_color)

        self.draw_center_line()
        self.draw_score()

        pygame.draw.rect(
            self.screen,
            self.green,
            self.player_paddle,
            border_radius=6,
        )

        pygame.draw.rect(
            self.screen,
            self.red,
            self.ai_paddle,
            border_radius=6,
        )

        pygame.draw.ellipse(
            self.screen,
            self.white,
            self.ball,
        )

        self.draw_hand_status(hand_detected)

        instruction = self.font_small.render(
            "Gerakkan jari telunjuk untuk mengontrol paddle | ESC untuk keluar",
            True,
            self.gray,
        )

        self.screen.blit(
            instruction,
            (
                self.width // 2 - instruction.get_width() // 2,
                self.height - 35,
            ),
        )

        pygame.display.flip()

    def tick(self, fps=60):
        """
        Membatasi FPS game dan mengembalikan delta time.
        """
        return self.clock.tick(fps) / 1000.0