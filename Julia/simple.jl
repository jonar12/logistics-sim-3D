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


function initialize_model(griddims)
    space = GridSpace(griddims; periodic=false)
    model = ABM(Union{Box, Robot}, space; agent_step!, properties = Dict(:griddims => griddims, :corners => []))

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
    if agent.pos != agent.final_pos
        move_towards(agent, agent.final_pos, model)
    else 
        agent.is_stacked = true
    end
end

function getBoxAndItem(data)
    res = post_request("http://localhost:5050/setItemAndBox", data)
    return res
end

# TODO: Acomodar cajas en una linea con cierto padding
function initialize_boxes(boxes, model, padding=5)
    x = 40

    for box in boxes
        if box["id"] isa Int
            box_agent = add_agent!(Box, model)
            box_agent.is_stacked = false
            box_agent.width = box["width"]
            box_agent.height = box["height"]
            box_agent.depth = box["depth"]
            box_agent.pos = (x, div(box_agent.height, 2), 20)
            box_agent.final_pos = Tuple(box["position"])

            println("Original box position: ", box_agent.pos)
            println("Final box position: ", box_agent.final_pos)

            # Incrementar x por el ancho de la caja + un padding de separación entre cajas
            x += box["width"] + padding
        else 
            push!(model.corners, Tuple(box["position"]))
        end
    end
end

function move_towards(agent, target_pos, model)
    # Calcular paso para caja eje x, z y y
    dx = sign(target_pos[1] - agent.pos[1])
    dz = sign(target_pos[3] - agent.pos[3])
    dy = sign(target_pos[2] - agent.pos[2])

    # Moverse primero en el eje x
    if dx != 0
        new_pos = (agent.pos[1] + dx, agent.pos[2], agent.pos[3])
        if is_valid_position(new_pos, model)
            agent.pos = new_pos
            return
        end
    end

    # Si el movimiento en x no es valido o se completó, moverse en el eje z
    if dz != 0
        new_pos = (agent.pos[1], agent.pos[2], agent.pos[3] + dz)
        if is_valid_position(new_pos, model)
            agent.pos = new_pos
            return
        end
    end

    # Si los movimientos en x y z no son validos o se completaron, moverse en el eje y
    if dy != 0
        new_pos = (agent.pos[1], agent.pos[2] + dy, agent.pos[3])
        if is_valid_position(new_pos, model)
            agent.pos = new_pos
            return
        end
    end
end


function is_valid_position(pos, model)
    # Verificar si la nueva posición esta dentro de los limites del modelo
    in_bounds = all(pos .>= (0, 0, 0)) && all(pos .< model.griddims)
    # no_collision = isempty(agents_at(pos, model))
    return in_bounds
end