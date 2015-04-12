import sfml as sf


def create_sprite(texture, width, heigth, position):
    sprite = sf.Sprite(texture)
    sprite.ratio = (width * 1.0 / texture.size.x * 1.0, heigth * 1.0 / texture.size.y * 1.0)
    sprite.position = position
    return sprite


def intersects(rect1, rect2):
    # compute the intersection boundaries
    left = max(rect1.left, rect2.left)
    top = max(rect1.top, rect2.top)
    right = min(rect1.right, rect2.right)
    bottom = min(rect1.bottom, rect2.bottom)

    # if the intersection is valid (positive non zero area), then
    # there is an intersection
    if left < right and top < bottom:
        return sf.Rectangle((left, top), (right-left, bottom-top))