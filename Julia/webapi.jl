include("agents/box.jl")
include("agents/lift.jl")
include("init/model_init.jl")

using Agents
using Genie, Genie.Requests
using UUIDs
using HTTP
import Genie.Renderer.Json: json as genie_json

# Diccionarios de simulaciones y pasos
instances = Dict()
step_counter = Dict{String, Int}()

# Ruta para inicializar simulación
route("/simulations", method=POST) do
    payload = jsonpayload()
    griddims = (200, 150, 200)

    model = initialize_model(griddims)
    id = string(uuid1())
    instances[id] = model
    step_counter[id] = 0

    boxes = [agent for agent in allagents(model) if agent isa Box]
    lifts = [agent for agent in allagents(model) if agent isa Lift]

    genie_json(Dict(
        "Location" => "/simulations/$id",
        "container" => model.container,
        "boxes" => boxes,
        "lifts" => lifts
    ))
end

# Ruta para ejecutar pasos
route("/simulations/:id") do
    simulation_id = payload(:id)
    model = instances[simulation_id]

    # Ejecutar un paso de la simulación
    run!(model, 1)
    step_counter[simulation_id] += 1

    # Obtener estado actual
    boxes = [agent for agent in allagents(model) if agent isa Box]
    lifts = [agent for agent in allagents(model) if agent isa Lift]

    genie_json(Dict(
        "step" => step_counter[simulation_id],
        "boxes" => boxes,
        "lifts" => lifts
    ))
end

Genie.config.run_as_server = true
Genie.config.cors_headers["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Your frontend origin specifically
Genie.config.cors_headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
Genie.config.cors_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
Genie.config.cors_allowed_origins = ["http://localhost:5173"]  # Your frontend origin specifically

up()
