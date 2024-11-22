using Agents

@agent struct Box(GridAgent{3})
    is_stacked::Bool = false
    is_being_carried::Bool = false
    WHD::Tuple{Int, Int, Int} = (0, 0, 0)
    final_pos::Tuple{Int, Int, Int} = (0, 0, 0)
    color::String = ""
end
