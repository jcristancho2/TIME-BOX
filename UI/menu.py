
import emojic as e

banner_init =f'''
{e.sdo*30}

  |||||||| || |||    ||| ||||||                          
     ||    || || |  | || ||                              
     ||    || ||  ||  || ||||      |||||    |||   ||   ||
     ||    || ||      || ||        ||   | ||   ||  || ||
     ||    || ||      || ||||||    |||||  ||   ||   |||
                                   ||   | ||   ||  || ||
                                   |||||    |||   ||   ||
{e.sdo*30}

'''

login =f'''

'''
menu_principal =f'''
{e.sdo*30}
{e.sdo*12}MEMU PRINCIPAL{e.sdo*11}
{e.sdo*30}

{ e.uno + e.memo} registrar tarea
{e.dos + e.wrench} modificar tarea
{e.tres + e.delete} eliminar tarea
{e.cuatro + e.view} visualizar tarea
{e.cinco + e.users} configuracion de usuarios
{e.cero + e.door} salir 

'''


menu_modificaciones =f'''
{e.sdo*30}
{e.sdo*8}MODIFICACION DE TAREAS{e.sdo*11}
{e.sdo*30}

{ e.uno + e.memo} modificar nombre de la tarea
{e.dos + e.pushpin} modificar estado de la tarea
{e.tres + e.clock} modificar fecha y hora
{e.cero + e.back} regresar 


'''

menu_eliminar =f'''
{e.sdo*30}
{e.sdo*12}ELIMINAR TAREAS{e.sdo*11}
{e.sdo*30}

{ e.uno + e.memo} buscar por id
{e.dos + e.pushpin} modificar estado de la tarea
{e.tres + e.clock} modificar fecha y hora
{e.cero + e.back} regresar 


'''
print(banner_init)
print(menu_principal)
print(menu_eliminar)
print(menu_modificaciones)