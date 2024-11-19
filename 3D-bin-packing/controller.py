from Caja import Caja
from Contenedor import Contenedor
from py3dbp import Packer, Bin, Item, Painter

def controller(contenedor, cajas):
    # Inicializar packer
    packer = Packer()

    # Inicializar contenedor
    box = Bin(
        partno=contenedor.id,
        WHD=(contenedor.width,contenedor.height,contenedor.depth),
        max_weight=28080,
        corner=15,
        put_type=0
    )

    # Agregar contenedor
    packer.addBin(box)

    # Inicializar cajas
    for caja in cajas:
        packer.addItem(
            Item(
                partno=caja.id,
                name=f"Caja {caja.id}",
                typeof='cube',
                WHD=(caja.width, caja.height, caja.depth),
                weight=85.12,
                level=1,
                loadbear=100,
                updown=True,
                color='#FF0000'
            )
        )

    # Calcular packing
    packer.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=False,
        check_stable=False,
        support_surface_ratio=0.75,
        number_of_decimals=0
    )

    cajas_output = []

    for box in packer.bins:
        for item in box.items:
            # Armar output de cajas
            cajas_output.append({
                "id": item.partno,
                "width": int(item.width),
                "height": int(item.height),
                "depth": int(item.depth),
                "position": [int(item.position[0]), int(item.position[1]), int(item.position[2])],
                "rotation_type": item.rotation_type
            })
        # painter = Painter(box)
        # fig = painter.plotBoxAndItems(
        #     title=box.partno,
        #     alpha=0.2,
        #     write_num=True,
        #     fontsize=10
        # )
        # fig.show()
    print(cajas_output)
    return cajas_output

# Mock data for the container and boxes
contenedor = Contenedor(
    id="20ft_Container",
    width=500,  # Length in cm
    height=500,  # Height in cm
    depth=500  # Depth in cm
)

cajas = [
    Caja(id="Box1", width=50, height=50, depth=50),
    Caja(id="Box2", width=40, height=40, depth=40),
    Caja(id="Box3", width=60, height=60, depth=60),
    Caja(id="Box4", width=30, height=30, depth=30)
]

# Call the controller function with the mock data
controller(contenedor, cajas)
