using Agents
include("request-3d-bp-api.jl")
include("data.jl")
include("random-hex-color.jl")

@agent struct Box(GridAgent{3})
    is_stacked::Bool = false
    is_being_carried::Bool = false
    WHD::Tuple{Int, Int, Int} = (0, 0, 0)
    final_pos::Tuple{Int, Int, Int} = (0, 0, 0)
    color::String = ""
end

@agent struct Lift(GridAgent{3})
    carrying_box::Union{Box, Nothing} = nothing
    orientation::Symbol = :up
end

function initialize_model(griddims)
    space = GridSpace(griddims; periodic=false, metric = :manhattan)
    model = ABM(Union{Box, Lift}, space; agent_step!, properties = Dict(:griddims => griddims, :container => data["contenedor"]))

    # Obtener información de cajas
    boxes = getBoxAndItem(data)

    # Crear cajas a partir de la información obtenida
    initialize_boxes(boxes, model)

    # Crear Lifts
    initialize_lifts(model)

    return model
end

function agent_step!(agent::Lift, model)
    if isnothing(agent.carrying_box)
        # Si el montacargas no lleva una caja, ir a la zona de cajas
        move_towards(agent, (0, 0, 50), model)

        # Debug nearby agents
        # println("Nearby agents (Box only): ",
        #     [agent for agent in nearby_agents(agent, model, 1.0) if agent isa Box])
        # Esto detecta a los agentes Box cercanos al montacargas

        # Detect nearby boxes
        # Esto NO detecta a los agentes Box cercanos al montacargas
        for agent in nearby_agents(agent, model, 1.0)
            println("Nearby agent: ", agent)
            println("Agent type: ", typeof(agent))

            if agent isa Box
                println("Box detected and selected: ", agent)

                # Mark the box as being carried
                agent.is_being_carried = true

                # Assign the box to the lift
                agent.carrying_box = agent
                break
            end
        end
    else
        # Si el montacargas lleva una caja, mover caja y robot hacia posición final de la caja
        move_towards(agent, agent.carrying_box.final_pos, model) # Movimiento del montacargas
        move_towards(agent.carrying_box, agent.carrying_box.final_pos, model) # Movimiento de la caja
    end
end

function agent_step!(agent::Box, model)
    # El agente Box no realiza ninguna acción
    # if agent.pos != agent.final_pos
    #     move_towards(agent, agent.final_pos, model)
    # else
    #     agent.is_stacked = true
    # end
end

function getBoxAndItem(data)
    res = post_request("http://localhost:5050/setItemAndBox", data)
    return res
end

# TODO: Acomodar cajas en una linea con cierto padding
function initialize_boxes(boxes, model, padding=2)
    x = 0

    for box in boxes
        # Crear agente Box
        box_agent = add_agent!(Box, model)

        # Inicializar propiedades del agente Box
        box_agent.WHD = rotate_box(box["rotation_type"], box["width"], box["height"], box["depth"])
        box_agent.pos = (x, 0, 50)
        box_agent.final_pos = Tuple(box["position"])
        box_agent.color = random_hex_color()

        # Incrementar x por el ancho de la caja + un padding de separación entre cajas
        x += box["width"] + padding
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

function initialize_lifts(model, n_lifts=5, spacing=10)
    x = 100

    for i in 1:n_lifts
        lift = add_agent!(Lift, model)
        lift.pos = (x, 0, 50)
        x += spacing
    end
end
