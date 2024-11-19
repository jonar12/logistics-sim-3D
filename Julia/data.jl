function generate_sample_data(num_boxes::Int)
    # Generate container data
    contenedor = Dict(
        "id" => 1,
        "width" => 100,
        "height" => 100,
        "depth" => 100
    )

    # Generate random boxes
    cajas = [
        Dict(
            "id" => i,
            "width" => rand(10:50),
            "height" => rand(10:50),
            "depth" => rand(10:50)
        ) for i in 1:num_boxes
    ]

    # Combine into a single dictionary
    data = Dict(
        "contenedor" => contenedor,
        "cajas" => cajas
    )

    return data
end

data = generate_sample_data(5)