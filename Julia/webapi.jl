using Genie, Genie.Renderer.Json, UUIDs, Agents

# Diccionarios de simulaciones y pasos
instances = Dict()
step_counter = Dict{String, Int}()

# Ruta para inicializar simulación
route("/simulations", method=POST) do
    payload = jsonpayload()
    griddims = (100, 100, 100)  # Tamaño del contenedor
    n_boxes = get(payload, "n_boxes", 20)

    model = initialize_model(griddims, n_boxes)
    id = string(uuid1())
    instances[id] = model
    step_counter[id] = 0

    json(Dict("simulation_id" => id, "message" => "Simulación creada"))
end

# Ruta para ejecutar pasos
route("/simulations/:id/step") do
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
