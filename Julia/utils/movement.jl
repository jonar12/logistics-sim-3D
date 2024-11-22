using Agents

function move_towards(agent, target_pos, model)
    # Calcular paso para caja eje x, z y y
    dx = sign(target_pos[1] - agent.pos[1])
    dz = sign(target_pos[3] - agent.pos[3])
    dy = sign(target_pos[2] - agent.pos[2])

    if dy != 0
        new_pos = (agent.pos[1], agent.pos[2] + dy, agent.pos[3])
        if is_valid_position(new_pos, model)
            agent.pos = new_pos
            return
        end
    end

    if dz != 0
        new_pos = (agent.pos[1], agent.pos[2], agent.pos[3] + dz)
        if is_valid_position(new_pos, model)
            agent.pos = new_pos
            return
        end
    end

    if dx != 0
        new_pos = (agent.pos[1] + dx, agent.pos[2], agent.pos[3])
        if is_valid_position(new_pos, model)
            agent.pos = new_pos
            return
        end
    end
end

function is_valid_position(pos, model)
    # Verificar si la nueva posición esta dentro de los limites del modelo
    in_bounds = all(pos .>= (0, 0, 0)) && all(pos .< model.griddims)
    # no_collision = isempty(agents_at(pos, model))
    return in_bounds
end
