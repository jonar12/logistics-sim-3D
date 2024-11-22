include("../agents/box.jl")

using Agents

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
