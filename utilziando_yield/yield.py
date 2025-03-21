def get_joelho(*pedido):
    for pedidos in pedido:
        yield f'{pedido} joelho'

print('\nusando yield:')
for salgado in get_joelho(4,6,8):
    print(salgado)
