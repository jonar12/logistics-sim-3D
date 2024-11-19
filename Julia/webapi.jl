include("simple.jl")
using Genie, Genie.Renderer.Json, Genie.Requests, UUIDs, Agents, HTTP

# Diccionarios de simulaciones y pasos
instances = Dict()
step_counter = Dict{String, Int}()

# Ruta para inicializar simulación
route("/simulations", method=POST) do
    payload = jsonpayload()
    griddims = (100, 100, 100)  # Tamaño del contenedor
    n_boxes = 20

    model = initialize_model(griddims, n_boxes)
    id = string(uuid1())
    instances[id] = model
    step_counter[id] = 0

    json(Dict("Location" => "/simulations/$id"))
end

# Ruta para ejecutar pasos
route("/simulations/:id") do
    simulation_id = payload(:id)
    model = instances[simulation_id]

    # Ejecutar un paso
    run!(model, 1)
    step_counter[simulation_id] += 1

    # Obtener estado actual
    boxes = [agent for agent in allagents(model) if agent isa Box]
    robots = [agent for agent in allagents(model) if agent isa Robot]

    json(Dict(
        "step" => step_counter[simulation_id],
        "boxes" => boxes,
        "robots" => robots
    ))
end

Genie.config.run_as_server = true
Genie.config.cors_headers["Access-Control-Allow-Origin"] = "*"
Genie.config.cors_headers["Access-Control-Allow-Headers"] = "Content-Type"
Genie.config.cors_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS" 
Genie.config.cors_allowed_origins = ["*"]

up()
