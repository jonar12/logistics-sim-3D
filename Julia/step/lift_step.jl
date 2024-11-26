include("../agents/lift.jl")
include("../utils/box_selection.jl")
include("../utils/movement.jl")
include("../utils/geometry_utils.jl")
include("../utils/priority_management.jl")

using DataStructures

function agent_step!(agent::Lift, model)
    # Check if the agent is at the top of the queue
    if isempty(model.queue) || first(model.queue)[1] != agent
        return # Skip this agent's turn
    end

    # Remove the agent from the queue as it is now active
    dequeue!(model.queue)

    if isnothing(agent.carrying_box)
        # If the lift is not carrying a box, select one and move toward it
        selected_box = select_box(agent, model)
        agent.carrying_box = selected_box

        if selected_box !== nothing
            # Move the lift toward the selected box
            move_lift_to_box(agent, selected_box.pos, model)
        else
            println("No box available for agent $(agent.id) to carry.")
        end
    else
        # If the lift is carrying a box, move towards the box's final position
        box = agent.carrying_box

        # Check if the lift is close enough to the box to begin simultaneous movement
        distance_to_box = euclidean_distance(agent.pos, box.pos)
        if distance_to_box < 1.0 # AQUI cambiar distancia de montacargas-caja para el inicio del cargado
            # Mark the box as being carried
            box.carrying_box.is_being_carried = true
            # Simultaneously move the lift and the box toward the box's final position
            move_lift_and_box(agent, box, box.final_pos, model)
        else
            # Move the lift closer to the box
            move_lift_to_box(agent, box.pos, model)
        end

        # Check if the lift and box have reached the position of the truck entrance
        if agent.pos[3] <= model.container["depth"] + 10 && box.pos[3] <= model.container["depth"] + 10
            println("Agent $(agent.id) delivered box $(box.id) to its final position.")
            box.pos = box.final_pos
            agent.carrying_box = nothing
            box.is_being_carried = false
            box.is_stacked = true
        end
    end

    # Recalculate priority for the agent and requeue it
    push!(model.queue, agent => agent.id)
end
