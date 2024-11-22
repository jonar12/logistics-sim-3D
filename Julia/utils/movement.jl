using Agents

function move_lift_to_box(lift, box_pos, model)
    # Calculate steps in y, z, and x
    dy = sign(box_pos[2] - lift.pos[2])
    dz = sign(box_pos[3] - lift.pos[3])
    dx = sign(box_pos[1] - lift.pos[1])

    # Prioritize y movement first
    if dy != 0
        new_pos = (lift.pos[1], lift.pos[2] + dy, lift.pos[3])
        if is_valid_position(new_pos, model)
            lift.pos = new_pos
            return
        end
    end

    # Then prioritize z movement
    if dz != 0
        new_pos = (lift.pos[1], lift.pos[2], lift.pos[3] + dz)
        if is_valid_position(new_pos, model)
            lift.pos = new_pos
            return
        end
    end

    # Finally, prioritize x movement
    if dx != 0
        new_pos = (lift.pos[1] + dx, lift.pos[2], lift.pos[3])
        if is_valid_position(new_pos, model)
            lift.pos = new_pos
            return
        end
    end
end

function move_lift_and_box(lift, box, target_pos, model)
    # Calculate steps in x, y, and z
    dx = sign(target_pos[1] - lift.pos[1])
    dy = sign(target_pos[2] - lift.pos[2])
    dz = sign(target_pos[3] - lift.pos[3])

    # Prioritize y movement first
    if dy != 0
        new_lift_pos = (lift.pos[1], lift.pos[2] + dy, lift.pos[3])
        new_box_pos = (box.pos[1], box.pos[2] + dy, box.pos[3])
        if is_valid_position(new_lift_pos, model) && is_valid_position(new_box_pos, model)
            lift.pos = new_lift_pos
            box.pos = new_box_pos
            return
        end
    end

    # Then prioritize x movement
    if dx != 0
        new_lift_pos = (lift.pos[1] + dx, lift.pos[2], lift.pos[3])
        new_box_pos = (box.pos[1] + dx, box.pos[2], box.pos[3])
        if is_valid_position(new_lift_pos, model) && is_valid_position(new_box_pos, model)
            lift.pos = new_lift_pos
            box.pos = new_box_pos
            return
        end
    end

    # Finally, prioritize z movement
    if dz != 0
        new_lift_pos = (lift.pos[1], lift.pos[2], lift.pos[3] + dz)
        new_box_pos = (box.pos[1], box.pos[2], box.pos[3] + dz)
        if is_valid_position(new_lift_pos, model) && is_valid_position(new_box_pos, model)
            lift.pos = new_lift_pos
            box.pos = new_box_pos
            return
        end
    end
end

function is_valid_position(pos, model)
    # Verify if the new position is within model bounds
    in_bounds = all(pos .>= (0, 0, 0)) && all(pos .< model.griddims)
    return in_bounds
end
