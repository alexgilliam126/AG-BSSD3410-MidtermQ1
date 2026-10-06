from PIL import Image
import colorsys


def composite_image(foreground_name, background_name):
    foreground = Image.open(foreground_name).convert("RGB")
    background = Image.open(background_name).convert("RGB")

    width, height = foreground.size

    # Resize the background to match the foreground
    background = background.resize((width, height))

    # Get the screen color from the top-left pixel
    key_color = foreground.getpixel((0, 0))

    # Convert the screen color from RGB to YIQ
    key_yiq = colorsys.rgb_to_yiq(
        key_color[0] / 255,
        key_color[1] / 255,
        key_color[2] / 255
    )

    # Check every pixel in the foreground image
    for y in range(height):
        for x in range(width):

            pixel = foreground.getpixel((x, y))

            pixel_yiq = colorsys.rgb_to_yiq(
                pixel[0] / 255,
                pixel[1] / 255,
                pixel[2] / 255
            )

            difference = (
                abs(pixel_yiq[0] - key_yiq[0]) +
                abs(pixel_yiq[1] - key_yiq[1]) +
                abs(pixel_yiq[2] - key_yiq[2])
            )

            # Replace pixels close to the screen color
            if difference < 0.45:
                background_pixel = background.getpixel((x, y))
                foreground.putpixel((x, y), background_pixel)

    output_name = foreground_name.replace(".jpg", "_composite.jpg")
    foreground.save(output_name)

    print("Saved:", output_name)


def main():
    composite_image("jack (1).jpg", "sesamestreet.jpg")
    composite_image("guard (1).jpg", "beachsunset.jpg")


main()