include("../utils/box_rotation.jl")
include("../utils/color_utils.jl")

using Agents

function initialize_lifts(model, n_lifts=1, spacing=10)
    z = 90

    for i in 1:n_lifts
        lift = add_agent!(Lift, model)
        lift.pos = (div(model.container["width"], 2), 0, z)
        z += spacing
    end
end

function initialize_boxes(boxes, model, padding=1)
    z = model.container["depth"] + 40

    for box in boxes
        # Crear agente Box
        box_agent = add_agent!(Box, model)

        # Inicializar propiedades del agente Box
        box_agent.WHD = rotate_box(box["rotation_type"], box["width"], box["height"], box["depth"])
        box_agent.pos = (model.container["width"] + 120, 0, z)
        box_agent.final_pos = Tuple(box["position"])
        box_agent.color = random_hex_color()

        # Incrementar x por el ancho de la caja + un padding de separación entre cajas
        z += box["width"] + padding
    end
end
