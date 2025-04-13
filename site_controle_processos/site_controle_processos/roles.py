from rolepermissions.roles import AbstractUserRole

class Supervisor(AbstractUserRole):
    available_permissions = {
        #Lançamentos de compras de lentes
        'criar_compra_lentes': True,
        'editar_compra_lentes': True,
        'deletar_compra_lentes': True,
        'consultar_compra_lentes': True,
        'relatorios_compra_lentes': True
    }

class Gerente(AbstractUserRole):
    available_permissions = {
        #Lançamentos de compras de lentes
        'criar_compra_lentes': True,
        'editar_compra_lentes': True,
        'deletar_compra_lentes': True,
        'consultar_compra_lentes': True,
        'relatorios_compra_lentes': True
    }

class AuxiliarDeEstoque(AbstractUserRole):
    available_permissions = {
        #Lançamentos de compras de lentes
        'criar_compra_lentes': True,
        'editar_compra_lentes': True,
        'deletar_compra_lentes': False,
        'consultar_compra_lentes': True,
        'relatorios_compra_lentes': False
    }