include("../agents/lift.jl")
include("../agents/box.jl")

using Agents

function calculate_priority(lift, model)
    # Example: Use the Manhattan distance to the nearest box as the priority
    nearest_box = find_nearest_box(lift, model)
    return nearest_box == nothing ? Inf : manhattan_distance(lift.pos, nearest_box.pos)
end

function find_nearest_box(lift, model)
    boxes = [agent for agent in allagents(model) if agent isa Box]
    return isempty(boxes) ? nothing : argmin(box -> manhattan_distance(lift.pos, box.pos), boxes)
end

function manhattan_distance(pos1, pos2)
    return sum(abs.(pos1 .- pos2))
end
