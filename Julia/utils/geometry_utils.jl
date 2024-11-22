function euclidean_distance(pos1::Tuple, pos2::Tuple)
    return sqrt(sum((p1 - p2)^2 for (p1, p2) in zip(pos1, pos2)))
end
