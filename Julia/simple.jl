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
        # If the lift is not carrying a box, select one and move toward it
        selected_box = select_box(agent, model)
        agent.carrying_box = selected_box

        if selected_box !== nothing
            # Move the lift toward the selected box
            move_towards(agent, selected_box.pos, model)
        else
            println("No box available for agent $(agent.id) to carry.")
        end
    else
        # If the lift is carrying a box, move towards the box's final position
        box = agent.carrying_box

        # Check if the lift is close enough to the box to begin simultaneous movement
        distance_to_box = euclidean_distance(agent.pos, box.pos)
        if distance_to_box < 1.0
            # Simultaneously move the lift and the box toward the box's final position
            move_towards(agent, box.final_pos, model)
            move_towards(box, box.final_pos, model)
        else
            # Move the lift closer to the box
            move_towards(agent, box.pos, model)
        end

        # Check if the lift and box have reached the final position
        if agent.pos == box.final_pos && box.pos == box.final_pos
            println("Agent $(agent.id) delivered box $(box.id) to its final position.")
            agent.carrying_box = nothing
            box.is_being_carried = false
            box.is_stacked = true
        end
    end
end

function agent_step!(agent::Box, model)

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


function select_box(agent, model)
    # Filter boxes that are not stacked and not being carried
    boxes = [box for box in allagents(model) if box isa Box && !box.is_being_carried && !box.is_stacked]

    # If there are available boxes, select one at random
    if !isempty(boxes)
        selected_box = rand(boxes)
        # Mark the selected box as being carried
        selected_box.is_being_carried = true
        return selected_box
    else
        # Return nothing if no boxes are available
        return nothing
    end
end

function euclidean_distance(pos1::Tuple, pos2::Tuple)
    return sqrt(sum((p1 - p2)^2 for (p1, p2) in zip(pos1, pos2)))
end
