import arcade

# Настройки окна
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Platformer"

# Константы для игрока
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 25

TILE_SCALING = 0.5


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.scene = None

        self.player_sprite = None
        self.player_physics_engine = None

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        # Создание (уровня)
        self.scene = arcade.Scene()

        # Создаём слои
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Platforms")

        # Добавляем main платформу
        for x in range(0, 1920, 64):
            platform = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            platform.center_x = x
            platform.center_y = 32
            self.scene.add_sprite("Platforms", platform)

        for y in range(0, 1920, 64):
           platform = arcade.Sprite(":resources:images/tiles/stoneMid.png", TILE_SCALING)
           platform.center_x = 32
           platform.center_y = y
           self.scene.add_sprite("Platforms", platform)

        # Платформы
        for i in range(5):
            platform = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            platform.center_x = 100 + i * 250
            platform.center_y = 96 + i * 250
            self.scene.add_sprite("Platforms", platform)

        # Создание игрока
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_idle.png", TILE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 200
        self.scene.add_sprite("Player", self.player_sprite)

        # Создание физического движка для игрока
        self.player_physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene["Platforms"], gravity_constant=GRAVITY)

        # Камера
        '''self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)'''
        self.camera_sprites = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)

    def on_draw(self):
        # Отрисовка
        self.clear()
        self.camera_sprites.use()
        self.scene.draw()
        self.camera_gui.use()

    def center_camera_to_player(self):
        # Find where player is, then calculate lower left corner from that
        screen_center_x = self.player_sprite.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera_sprites.viewport_height / 2)

        # Set some limits on how far we scroll
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Here's our center, move to it
        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        # Обновление физики игрока
        self.player_physics_engine.update()
        self.scene["Platforms"].update()

        # Обновление позиции камеры
        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        # Управление движением игрока
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if self.player_physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.TAB:
            self.setup()

        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        # Остановка движения игрока
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


# Запуск игры
def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
