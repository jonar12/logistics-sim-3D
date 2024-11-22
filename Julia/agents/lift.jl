using Agents

@agent struct Lift(GridAgent{3})
    carrying_box::Union{Box, Nothing} = nothing
    orientation::Symbol = :up
end
