def cargar_mtl(archivo_mtl):
    materiales = {}
    material_actual = None
    with open(archivo_mtl, 'r') as f:
        for linea in f:
            if linea.startswith('newmtl'):
                material_actual = linea.split()[1]
                materiales[material_actual] = {}
            elif linea.startswith('Kd'):  # Color difuso
                valores = list(map(float, linea.split()[1:]))
                materiales[material_actual]['Kd'] = valores
            elif linea.startswith('Ka'):  # Color ambiental
                valores = list(map(float, linea.split()[1:]))
                materiales[material_actual]['Ka'] = valores
            elif linea.startswith('Ks'):  # Color especular
                valores = list(map(float, linea.split()[1:]))
                materiales[material_actual]['Ks'] = valores
            elif linea.startswith('Ns'):  # Brillo
                brillo = float(linea.split()[1])
                materiales[material_actual]['Ns'] = brillo
    return materiales