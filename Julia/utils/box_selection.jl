include("../agents/box.jl")

using Agents

function select_box(agent, model)
    # Filter boxes that are not stacked and not being carried
    boxes = [box for box in allagents(model) if box isa Box && !box.is_being_carried && !box.is_stacked]

    # If there are available boxes, prioritize based on final_pos y and z
    if !isempty(boxes)
        # Sort boxes by final_pos (first by y, then by z)
        sorted_boxes = sort(boxes, by = box -> (box.final_pos[2], box.final_pos[3]))

        # Select the highest-priority box (first in the sorted list)
        selected_box = first(sorted_boxes)

        return selected_box
    else
        # Return nothing if no boxes are available
        return nothing
    end
end
