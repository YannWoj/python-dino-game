class Camera:
    def __init__(self, player, level_width, level_height, screen_width, screen_height):
        self.player = player
        self.level_width = level_width
        self.level_height = level_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        # center the camera on the player
        self.offset_x = self.player.rect.centerx - self.screen_width // 2
        self.offset_y = self.player.rect.centery - self.screen_height // 2

        # prevent the camera from going outside the level boundaries
        self.offset_x = max(0, min(self.offset_x, self.level_width - self.screen_width))
        self.offset_y = max(0, min(self.offset_y, self.level_height - self.screen_height))

    def apply(self, target_rect):
        # apply the camera offset to a given rectangle
        # this shifts its position relative to what the camera sees
        return target_rect.move(-self.offset_x, -self.offset_y)