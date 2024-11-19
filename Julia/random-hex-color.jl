using Printf

function random_hex_color()
    # Generate three random integers between 0 and 255 for RGB components
    r = rand(0:255)
    g = rand(0:255)
    b = rand(0:255)

    # Convert the RGB values to a hex color string
    return @sprintf("#%02X%02X%02X", r, g, b)
end