import sfml as sf


def create_sprite(texture, width, heigth, position):
    sprite = sf.Sprite(texture)
    sprite.ratio = (width * 1.0 / texture.size.x * 1.0, heigth * 1.0 / texture.size.y * 1.0)
    sprite.position = position
    return sprite


def intersects(self, rectangle):
    # make sure the rectangle is a rectangle (to get its right/bottom border)
    l, t, w, h = rectangle
    rectangle = sf.Rectangle((l, t), (w, h))

    # compute the intersection boundaries
    left = max(self.left, rectangle.left)
    top = max(self.top, rectangle.top)
    right = min(self.right, rectangle.right)
    bottom = min(self.bottom, rectangle.bottom)

    # if the intersection is valid (positive non zero area), then
    # there is an intersection
    if left < right and top < bottom:
        return sf.Rectangle((left, top), (right-left, bottom-top))