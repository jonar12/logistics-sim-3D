using Agents

@agent struct Box GridAgent{3}
    is_stacked::Bool
    width::Int
    height::Int
    depth::Int
    final_pos::Tuple{Int, Int, Int}
end

@agent struct Robot GridAgent{3}
    carrying_box::Union{Box, Nothing}
end


function initialize_model(griddims, n_boxes)
    space = GridSpace(griddims; periodic=false)
    model = ABM(Union{Box, Robot}, space)

    # Crear cajas
    for i in 1:n_boxes
        dims = (rand(10:30), rand(10:30), rand(10:30))
        pos = (rand(1:griddims[1]), rand(1:griddims[2]), rand(1:griddims[3]))
        final_pos = (0, 0, 0)  # Final definido por la API
        add_agent!(Box(i, false, dims[1], dims[2], dims[3], final_pos), model)
    end

    # Crear robots
    add_agent!(Robot(1, (0, 0, 0), nothing), model)

    return model
end
