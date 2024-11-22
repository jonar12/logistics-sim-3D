box_types = [
    (1, 1, 1),
    (5, 5, 5),
    (7, 7, 7)
]

function generate_sample_data(num_boxes::Int)
    # Contenedor de 3.3 m2 (capacidad de la Peugeot Partner) (a escala de 10 m2)
    contenedor = Dict(
        "id" => 1,
        "width" => 15,
        "height" => 10,
        "depth" => 22
    )

    cajas = [
        let selected_box = rand(box_types)
            Dict(
                "id" => i,
                "width" => selected_box[1],
                "height" => selected_box[2],
                "depth" => selected_box[3]
            )
        end for i in 1:num_boxes
    ]


    # Combine into a single dictionary
    data = Dict(
        "contenedor" => contenedor,
        "cajas" => cajas
    )

    return data
end

data = generate_sample_data(10)

# data = Dict(
#     "contenedor" => Dict(
#         "id" => 1,
#         "width" => 60,
#         "height" => 60,
#         "depth" => 60
#     ),
#     "cajas" => [
#         Dict(
#             "id" => 1,
#             "width" => 40,
#             "height" => 20,
#             "depth" => 20
#         ),
#         Dict(
#             "id" => 2,
#             "width" => 30,
#             "height" => 20,
#             "depth" => 20
#         )
#     ]
# )
