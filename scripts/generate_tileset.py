from PIL import Image, ImageDraw

def generate_tileset():
    tile_size = 32
    grid_size = 4
    img_size = tile_size * grid_size
    img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 0: Grass (Green)
    draw.rectangle([0, 0, 31, 31], fill=(34, 139, 34))
    # 1: Water (Blue)
    draw.rectangle([32, 0, 63, 31], fill=(30, 144, 255))
    # 2: Wall/Stone (Gray)
    draw.rectangle([64, 0, 95, 31], fill=(105, 105, 105))
    # 3: Dirt (Brown)
    draw.rectangle([96, 0, 127, 31], fill=(139, 69, 19))

    img.save('/home/ubuntu/dragon-evolution-rpg/assets/tilesets/placeholder_tileset.png')
    print("Tileset gerado em assets/tilesets/placeholder_tileset.png")

if __name__ == "__main__":
    generate_tileset()
