from PIL import Image, ImageDraw, ImageFont
import json
import codecs

letter_sizing = 128
# Load the image
image = Image.new(mode="L", size=(5 * letter_sizing, 2 * letter_sizing))

# Create a drawing context
draw = ImageDraw.Draw(image)

letter_height = int(letter_sizing * 0.8)
# Define the text properties
font = ImageFont.truetype("comic-sans-bold.ttf", letter_height)
positions = dict()
for i in range(0, 10):
    text = str(i)
    text_color = 255

    center_x = i % 5 * letter_sizing
    center_y = i // 5 * letter_sizing
    # Calculate the position to center the text
    text_length = draw.textlength(text, font)
    print(i, draw.textbbox((center_x, center_y), text, font=font))
    positions[i] = draw.textbbox((center_x, center_y), text, font=font)
    x = center_x + (letter_sizing - text_length) / 2
    y = center_y

    # Add text to the image
    draw.text((center_x, center_y), text, fill=text_color, font=font)

    # Save or display the modified image
image.save("./guacamole/entities/texture_num.png")
with codecs.open("./guacamole/entities/texture_num.json", mode="w") as f:
    json.dump(positions, f)
print(positions)
