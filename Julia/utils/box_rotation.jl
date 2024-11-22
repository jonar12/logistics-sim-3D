function rotate_box(rotation_code::Int, width::Int, height::Int, depth::Int)
    # Define rotation mappings based on the rotation code
    mapping = Dict(
        0 => (width, height, depth),      # RT_WHD
        1 => (height, width, depth),      # RT_HWD
        2 => (height, depth, width),      # RT_HDW
        3 => (depth, height, width),      # RT_DHW
        4 => (depth, width, height),      # RT_DWH
        5 => (width, depth, height)       # RT_WDH
    )

    # Return the modified dimensions
    return mapping[rotation_code]
end
