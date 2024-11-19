using Agents
include("request-3d-bp-api.jl")
include("data.jl")

@agent struct Box(GridAgent{3})
    is_stacked::Bool = false
    width::Int = 0
    height::Int = 0
    depth::Int = 0
    final_pos::Tuple{Int, Int, Int} = (0, 0, 0)
end

@agent struct Robot(GridAgent{3})
    carrying_box::Union{Box, Nothing} = nothing
end


function initialize_model(griddims, n_boxes)
    space = GridSpace(griddims; periodic=false)
    model = ABM(Union{Box, Robot}, space)

    # Obtener información de cajas
    boxes = getBoxAndItem(data)

    # Crear cajas a partir de la información obtenida
    initialize_boxes(boxes, model)

    # Crear robots
    add_agent!(Robot, model)

    return model
end

function agent_step!(agent::Robot, model)
    # El agente Robot no realiza ninguna acción
end

function agent_step!(agent::Box, model)
    # El agente Box no realiza ninguna acción
end

function getBoxAndItem(data)
    res = post_request("http://localhost:5050/setItemAndBox", data)
    return res
end

# TODO: Acomodar cajas en una linea con cierto padding
function initialize_boxes(boxes, model, padding=5)
    x = 0

    for box in boxes
        if box["id"] isa Int
            box_agent = add_agent!(Box, model)
            box_agent.is_stacked = false
            box_agent.width = box["width"]
            box_agent.height = box["height"]
            box_agent.depth = box["depth"]
            box_agent.pos = (x, div(box_agent.height, 2), 0)
            box_agent.final_pos = Tuple(box["position"])

            # Incrementar x por el ancho de la caja + un padding de separación entre cajas
            x += box["width"] + padding
        end
    end
end