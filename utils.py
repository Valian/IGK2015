import sfml as sf


def create_sprite(texture, width, heigth):
    sprite = sf.Sprite(texture)
    sprite.ratio = (width / texture.size.x * 1.0, heigth / texture.size.y * 1.0)
    return sprite