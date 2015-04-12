import sfml as sf


def create_sprite(texture, width, heigth, position):
    sprite = sf.Sprite(texture)
    sprite.ratio = (width * 1.0 / texture.size.x * 1.0, heigth * 1.0 / texture.size.y * 1.0)
    sprite.position = position
    return sprite