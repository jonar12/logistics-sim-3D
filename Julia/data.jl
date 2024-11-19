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
            "width" => rand(1:10),
            "height" => rand(1:10),
            "depth" => rand(1:10)
        ) for i in 1:num_boxes
    ]

    # Combine into a single dictionary
    data = Dict(
        "contenedor" => contenedor,
        "cajas" => cajas
    )

    return data
end

# data = generate_sample_data(5)

data = Dict(
    "contenedor" => Dict(
        "id" => 1,
        "width" => 60,
        "height" => 60,
        "depth" => 60
    ),
    "cajas" => [
        Dict(
            "id" => 1,
            "width" => 20,
            "height" => 20,
            "depth" => 20
        ),
        Dict(
            "id" => 2,
            "width" => 50,
            "height" => 20,
            "depth" => 20
        )
    ]
)