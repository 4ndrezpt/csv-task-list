#linux version
import os
import sys
import csv
import json
import time
import shutil
import codecs
import time
import gi
gi.require_version('Notify','0.7')
from gi.repository import Notify

'''
Inicio del Cambio: 2-19-2024
Fecha de Aceptacion: 2-18-2024
Proyecto: Lista de Tareas en CSV
Módulo: Notificationes con WINDOWS
Developer: Andrés Felipe Zapata

'''

'''
Inicio del cambio: 10-06-2024
Fecha de aceptacion: 10-06-2024
Proyecto: Lista de Tareas en CSV
Modulo: agregar anotaciones en tareas ** note **
        Mejorar espaciado,
        Agregar nombre de proyecto al MENU
test: Manjaro 6.6-32-1
    will test: Win10 22h2
Developer: Andres Felipe Zapata
'''
'''
Inicio del cambio: 5-10-2026
Fecha de aceptacion: 2-10-2026
Proyecto: Lista de Tareas en CSV
Modulo: agregar impacto a las tareas con su modidicador ** note **
test: Debian 13
    will test: Debian 13
Developer: Andres Felipe Zapata
'''
'''
Prioridad
1. immediatly = urgente + importante
2. soon / delegated = No urgente + importante
3. postposed = urgente + No importante
4. moved = No urgente + No importante

Impacto=
1. quick wins = high impact + low effort
2. big project = high impact + high effort
3. fills-in = low impact + low effort
4. busywork = low impact + high effort
'''
def notification(title, message):
    '''
    enviar Notificacione a SO WINDOWS
    params: titulo, mensaje
    return VOID, notificacion WINDOWS
    '''
    Notify.init('TODO-list END -v')
    notification = Notify.Notification.new(title,message)
    notification.show()

todo = []
path = ''
files = os.listdir()
opexist = False
# Caso: No existe el archivo

try:
    path_file = input('Ingrese la ruta de la lista: \n')
    if path_file == '':
        idx = 0
        for file in files:
            print(idx + 1, f' {file}')
            idx += 1
        print()
        opt = int(input('Elige el # de la lista de la carpeta: \n'))
        path_file = files[opt-1]
    if os.path.exists(path_file):
        modo = 'r'
        print('the file exist')
    else:
        modo = 'a+'
        path_file = path_file + '.csv'
        notification('Nueva lista creada: ',path_file)
        print('Nueva lista creada: ',path_file)

except Exception as err:
    #logging.error(traceback.format_exc())
    print(err)

#print(folder)
#with open(splt_path[-1], modo, newline='') as file_csv:
with open(path_file, modo, newline='', encoding='utf-8') as file_csv:
    content_file = csv.reader(file_csv, delimiter=';')
    #content_file = content_file.read().decode('utf-8')
    for line in content_file:
        "task.split(';')"
        #print(line)
        todo.append(line)
    print('total de Tareas:',  len(todo))
    notification('TODO: ',f'Hay tareas pendientes: {len(todo)} tareas')

file_csv.close()
#print(todo)

def print_todo(todo):
    index = 0
    if len(todo) == 0:
        print('Lista Vacia')
        acumulative()
    else:
        for idx, task in enumerate(todo):
            if task[3] == 'True' or task[4] == "True":
                tmp = task
                todo.pop(idx)
                todo.append(tmp)
        tasks_completed(todo)


def tasks_completed(todo):
    index = 0
    print('{:>1} {:>18} {:>14} {:>15} {:>15} {:>15} {:>8}'.format('Indice',
                                                         'Tarea',
                                                         'Inicio',
                                                         'Final',
                                                         'Prioridad',
                                                         'Impacto',
                                                         'Estado'))
    print('---'*31)

    for task in todo:

        # Leer el formato de fecha y convertirlo
        #beg_date = time.strptime(task[1], '%Y-%m-%d')
        #end_date = time.strptime(task[2], '%Y-%m-%d')
        if(len(task) > 4):
            #Calcular estado de tarea
            status = 'Completo' if task[5] == 'True' else 'Pendiente'
            print('{:>1} {:>25} {:>15} {:>15} {:>15} {:>12} {:>8}'.format(index + 1,
                                                         task[0],
                                                         task[1],
                                                         task[2],
                                                         task[3],
                                                         task[4],
                                                  status))
        else:
            #Calcular estado de tarea
            status = 'Completo' if task[4]== 'True' else 'Pendiente'
            print('{:>1} {:>25} {:>15} {:>15} {:>15} {:>12}'.format(index + 1,
                                                         task[0],
                                                         task[1],
                                                         task[2],
                                                         task[3],
                                                status))


        print('---'*31)
        index += 1
    print('\n \n')
def special(todo):
    '''
funcion para agregar anotacion
a una tarea en lugar de prioridad
    '''
    num_task = int(input('\n Escribe el índice de la tarea que deseas anotar: \n'))
    if num_task < 0 and num_task > len(todo):
        print('Debes ingresar un número válido- \n')
    else:
        print('Número válido')
        note = input('\n Agrega la nota a la tarea: \n')
        note = '**' + note + '**'
        task = todo[num_task - 1]
        task[3] = note
        todo.pop(num_task - 1)
        #print(num_task)
        todo.insert(num_task - 1,task)
        print(task)
        print()
        #print(todo)
        #new tmp file to replace todo
        #maybe there's no way to erase the other data
        with open('tmp.csv','w+',newline='',encoding='utf-8') as tmp_file:
            writer = csv.writer(tmp_file, delimiter=';')
            writer.writerows(todo)
        #Utilizamos el atributo .name para reemplazar un archivo por otro
        shutil.move(tmp_file.name, file_csv.name)
    print('**-> La nota ha sido agregada \n ')
    print_todo(todo)

def find_document():
    '''
función para encontrar archivo csv
lista los archivos en la carpeta con OS
permite elegir de la lista el archivo
params: None
return: void
    '''
    files = os.listdir()
    print('acumultaive todo')
    extension = ['csv']
    valid__files = []
    modo = 'r'
    count = 0
    for file in files:
        if file.endswith('.csv'):
            valid__files.append(file)
            files = valid__files
    for file in files:
        count += 1
        print(f'{count}  {file}')
    file = int(input("Elige el archivo que deseas revisar: \n"))
    rw_file = valid__files[file - 1]
    count = 0
    todo_old = []
    print('Has elegido revisar la lista:',rw_file)
    with open(rw_file, 'r', newline='',encoding='utf-8') as old_csv:
        content_old = csv.reader(old_csv, delimiter=';')
        for line in content_old:
            todo_old.append(line)
    old_csv.close()

    return todo_old

        #print(content_old)

        #print(tmp_content)
        #if len(tmp_content) > 0:
def acumulative():
    content_old = find_document()
    const_list = []
    for line in content_old:
        "task.split(';')"
        todo.append(line)
    tmp_list = list(content_old)
    if len(tmp_list) > 0:
        notification('TODO: ','Hay tareas pendientes: ')
        print('There are tasks todo')
    else:
        notification('TODO: ','No Hay tareas pendientes: ')
        print("There are'nt tasks todo")
    #ciclo para filtrar las tareas finalizadas y agregarlas al documento
    #print(len(todo))
    print('Tareas en la Lista: ',len(todo))
    #Almacenar indices para borrar tareas completas
    tmp = []
    for idx, task in enumerate(todo):
        #print(task)
        if task[3] == 'KONST':
            task[4] = 'False'
            const_list.append(task)
        if task[4] != 'False':
            tmp.append(idx)
    print('line 122', tmp)
    #todo = const_list + todo
    #print(tmp)
    #print(todo)
    if len(tmp) != 0:
        del todo[tmp[0]:(tmp[-1] + 1)]

        #del todo[tmp[0]: len(tmp)]
    '''
    else:
        print('Congratulations: theres no task left behind')
    '''

    with open('tmp.csv','w+',newline='',encoding='utf-8') as tmp_file:
        writer = csv.writer(tmp_file, delimiter=';')
        writer.writerows(todo)
            #Utilizamos el atributo .name para reemplazar un archivo por otro
    shutil.move(tmp_file.name, file_csv.name)
    #print(todo)

def select_task(todo):
    num_task = int(input('Ingresa el número de la tarea: \n'))
    if num_task < 0 and num_task > len(todo):
        print('Debes ingresar un número válido- \n')
    else:
        task = todo[num_task - 1]
        if task[4] == 'True':
            print('La tarea ya ha sido completada. \n')
        else:
            task[4] = 'True'
            todo.pop(num_task - 1)
            #print(num_task)
            #todo.insert(num_task - 1,task)
            todo.append(task)
            print(task)
            print()
            #print(todo)
            #new tmp file to replace todo
            #maybe there's no way to erase the other data
            with open('tmp.csv','w+',newline='', encoding='utf-8') as tmp_file:
                writer = csv.writer(tmp_file, delimiter=';')
                writer.writerows(todo)
            #Utilizamos el atributo .name para reemplazar un archivo por otro
            shutil.move(tmp_file.name, file_csv.name)
def add_task(todo):
    task_nm = input('Ingresa la nueva tarea a realizar: \n')
    task_bgdt = input('Ingresa la fecha de inicio: \n')
    task_endt = input('Ingresa la fecha final: \n')
    task_prior = input('Ingresa la propridad: \n')
    task_impact = input('Ingresa el impacto: \n')
    task_bool = False

    task_nw = [task_nm, task_bgdt, task_endt, task_prior, task_impact, task_bool]
    todo.append(task_nw)
    #new tmp file to replace todo
    #maybe there's no way to erase the other data
    with open('tmp.csv','w+',newline='',encoding='utf-8') as tmp_file:
        writer = csv.writer(tmp_file, delimiter=';')
        writer.writerows(todo)
    #Utilizamos el atributo .name para reemplazar un archivo por otro
    shutil.move(tmp_file.name, file_csv.name)
def mod_prior(todo):
    num_task = int(input('Ingresa el número de la tarea: \n'))
    if num_task < 0 and num_task > len(todo):
        print('Debes ingresar un número válido- \n')
    else:
        task = todo[num_task - 1]
        task_prior = input('Agregar prioridad a la Tarea: \n')
        task[3] = task_prior
        todo.pop(num_task - 1)
        #print(num_task)
        todo.insert(num_task - 1,task)
        print(task)
        print()
        #print(todo)
        #new tmp file to replace todo
        #maybe there's no way to erase the other data
        with open('tmp.csv','w+',newline='',encoding='utf-8') as tmp_file:
            writer = csv.writer(tmp_file, delimiter=';')
            writer.writerows(todo)
        #Utilizamos el atributo .name para reemplazar un archivo por otro
        shutil.move(tmp_file.name, file_csv.name)
def mod_impact(todo):
    num_task = int(input('Ingresa el número de la tarea: \n'))
    if num_task < 0 and num_task > len(todo):
        print('Debes ingresar un número válido- \n')
    else:
        task = todo[num_task - 1]
        task_impact = input('Agregar prioridad a la Tarea: \n')
        task[4] = task_impact
        todo.pop(num_task - 1)
        #print(num_task)
        todo.insert(num_task - 1,task)
        print(task)
        print()
        #print(todo)
        #new tmp file to replace todo
        #maybe there's no way to erase the other data
        with open('tmp.csv','w+',newline='',encoding='utf-8') as tmp_file:
            writer = csv.writer(tmp_file, delimiter=';')
            writer.writerows(todo)
        #Utilizamos el atributo .name para reemplazar un archivo por otro
        shutil.move(tmp_file.name, file_csv.name)
def del_task(todo):
    '''
    Función para borrar tareas de la lista
    Params= Indice de la tarea en la lista
    '''
    print_todo(todo)
    num_task = int(input('Ingresa el número de la tarea: \n'))
    if num_task < 0 and num_task > len(todo):
        print('Debes ingresar un número válido- \n')
    else:
        todo.pop(num_task - 1)
        #new tmp file to replace todo
        #maybe there's no way to erase the other data
        with open('tmp.csv','w+',newline='',encoding='utf-8') as tmp_file:
            writer = csv.writer(tmp_file, delimiter=';')
            writer.writerows(todo)
        #Utilizamos el atributo .name para reemplazar un archivo por otro
        shutil.move(tmp_file.name, file_csv.name)

def menu():
    response = None
    options = ['Leer lista de tareas',
               'Marcar una tarea como completa',
               'Agregar una tarea a la lista',
               'Borrar una tarea de la lista',
               'Guardar lista de tareas',
               'Cambiar Prioridad a una tarea',
               'Cambiar Impactor de una tarea',
               'Anotar en una lista',
               'SALIR']
    index = 0
    while response != 8:
        print('\n *** TODO LIST CSV EDITION *** \n')
        for option in options:
            print('{:>1} {:>15}'.format(index + 1, option))
            index += 1
        try:
            response = int(input('\n Ingresa la opción que deseas ejecutar: \n'))
        except Exception as err:
            print(err)
        if response == 1:
            print('\n 1. Leer lista de tareas \n')
            print_todo(todo)
        elif response == 2:
            print('\n 2. Marcar tarea como completa \n')
            select_task(todo)
        elif response == 3:
            print('\n 3. Agregar tarea a la lista \n')
            add_task(todo)
        elif response == 4:
            print('\n 4. Borrar una tarea de la lista \n')
            del_task(todo)
        elif response == 5:
            print('\n 5. Guardar lista de tareas \n')
            pass
        elif response == 6:
            print('\n 6. Agregar prioridad a la  tarea \n')
            mod_prior(todo)
        elif response == 7:
            print('\n 7. Agregar prioridad a la  tarea \n')
            mod_impact(todo)
        elif response == 8:
            print('\n 8. Anotar en una tarea \n')
            special(todo)
        elif response == 9:
            print('Gracias por utilizar nuestros sistemas')
            sys.exit()
        else:
            print()
            print('**'*15)
            print('Ingresa un a opcion Válida')
            print('**'*15)
            print()
        index = 0
menu()
