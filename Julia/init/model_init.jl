include("../APIs/request-3d-bp-api.jl")
include("agent_init.jl")
include("../step/box_step.jl")
include("../step/lift_step.jl")
include("../data.jl")

using Agents

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
