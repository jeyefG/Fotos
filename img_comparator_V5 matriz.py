# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 10:43:52 2021

@author: jfcog
"""

import os
from skimage import io
import numpy as np
import csv


#listamos las subcarpetas, si las hay:
def sub_fold(path):
    sub_folders = []
    #listamos todos los elementos de la carpeta
    #descartamos los archivos que tengan alguna extensión
    arr = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    for element in arr:
        sub_folders.append(element)
    

    return sub_folders

def fill_map(mapa, path):
    arr = os.listdir(path)
    for element in arr:
        #print(element)
        if '.' in element and element[-3:] == 'jpg' or element[-3:] == 'JPG':
            img_path = str(path)+'/'+str(element)
            img = io.imread(img_path)
            pair = [np.mean(img.ravel()),path, element]
            mapa.append(pair)
    print(mapa)

#entrega la primera subcarpeta aún sin revisar
def chk_subfldrs(path):
    sub_folders = sub_fold(path)
    for element in sub_folders:
        if element == "":
            sub_path = path
        else:
            sub_path = str(path)+'/'+str(element)
        if sub_path not in carpetas_rec:
            print(sub_path)        
            return sub_path
        else:
            continue
        
    return path

def guardado(mapa):    
    mapa.sort()
    f = open(path + '/resultados.txt','w')
    for element in mapa:
        aux = str(element[0]) + ";" + str(element[1] + ";" + str(element[2]))
        print(aux)
        f.write(aux + "\n"  )

    f.close()   
    mapa = []   
    
def mapeado(mapa):
    #Creamos los encabezados de la matriz
    header = ["Picture ID", "Pic name"]
    for element in carpetas_rec:
        header.append(element)
    #mapa expandido cuyo primer registro es el encabezado:
    #ID y listado de todas las carpetas recorridas
    mapa_exp = [header]
    bool_aux = False
    #Ahora recorremos el arreglo mapa ID por ID y vamos llenando el mapa_exp
    aux_reg = 0
    for registry in mapa:
        
        pict_id = registry[0]
        pic_name = registry[2]
        pic_folder = registry[1]
        #tenemos que agregar a mapa_exp un arreglo new_line del tipo [pic Id, ",",",1,","]
        #con el 1 en la posición de pic_folder
        new_line = [pict_id, pic_name]
        for i in carpetas_rec:
            new_line.append(0)
            
        index = carpetas_rec.index(pic_folder)
        new_line[index+2]=1
        #Revisamos si el pic Id ya ha aparecido
        aux_map = 0
        for element in mapa_exp:        
            if aux_map > 0:
                if pict_id == float(element[0]):
                    bool_aux = True
                else:
                    continue
            else:
                aux_map +=1
                continue
        
        if bool_aux:
            mapa_exp[aux_reg][index+2] = int(mapa_exp[aux_reg][index+2]) +1
            bool_aux = False
            continue
        else:
            mapa_exp.append(new_line)
    
        aux_reg += 1
    #Guardamos mapa en txt
    f = open(path + '/mapa.txt','w')
    for element in mapa_exp:
        aux = ""
        for i in element:
            aux += str(i) + ";" 
        aux = aux[:-1]
        print(aux)
        f.write(aux + "\n"  )
    
if __name__=='__main__':
    
    path = 'D:/Fotos M/Resto/Sub'
    #path = "D:/JFG/GBLA/Fotos"
    #path_aux = "D:/JFG/GBLA/Fotos"
    flag = True
    all_folders = False
    carpetas_rec = []
    sub_folders = []
    sub_paths_rec = []
    mapa = []
        
    #print(path_aux)
    #print(carpetas_rec)
    if sub_fold(path):
        sub_folders = sub_fold(path)
        all_folders = False
    new_path = path
    aux = 0 
    aux2 = 0
    delta_path = ""

    #recorremos las subcarpetas de la ruta madre
    while all_folders == False:
        
        print("en While #: " + str(aux))
        
        #buscamos la última carpeta de cada rama que no haya sido recorrida       
        #si existen subfolders en la carpeta actualizamos new_path
        if sub_folders != []:
            aux2 += 1
            new_path = new_path + '/' + sub_folders[0]
            
            #tratamos de encontrar nuevas carpetas. Si hay, actualizamos la ruta
            try:
                sub_fold(new_path)
                #actualizamos las subcarpetas de la nueva carpeta
                sub_folders = sub_fold(new_path)
                #delta_path = ""
                #print(sub_folders)
            #si no existen nuevas carpetas, revisamos los archivos de la última
            #y agregamos esa carpeta a carpetas recorridas
            except Exception as e:
                print(e)
                #delta_path = ""
                #sub_folders = []
            
            
        #si llegamos acá es porque no hay nuevas subcarpetas, y hay que empezar
        #a procesar los archivos en new_path 
        else:

            if new_path not in carpetas_rec:
                print("agregando elementos de carpeta: " + new_path)
                fill_map(mapa, new_path)
                #los elementos de la carpeta ya fueron incorporados
                #se debe incorporar la carpeta a las carpetas recorridas
                #se debe actualizar la ruta
                carpetas_rec.append(new_path)
                #historia de las subcarpetas ya recorridas
                sub_paths_rec.append(delta_path)
                guardado(mapa)
            print(str(carpetas_rec) + "aux #: " + str(aux))
            #aquí debemos chequear antes de mandar a la ruta de la carpeta anterior
            #si nos queda alguna carpeta por revisar aún
            
            #volvemos a ruta anterior para buscar subcarpetas pendientes. Seguimos con la primera subcarpeta pendiente
            if aux2 == 0:
                all_folders = True
            for i in range (0,aux2):
                #chequeamos si volvimos a ruta madre y cortamos loop
                if new_path == path:
                    all_folders = True
                    break
                lst = new_path.rfind("/")
                new_path = new_path[:lst]
                path_aux = chk_subfldrs(new_path)
                if path_aux != new_path:
                    new_path = path_aux
                    sub_folders = sub_fold(new_path)
                    break
                else:
                    if path_aux not in carpetas_rec:
                        new_path = path_aux
                        break

        aux += 1
    
    print(carpetas_rec)
    print(str(aux))
    
    mapeado(mapa)
    
#Aquí procesamos el arreglo mapa para crear una matriz con el ID en la 1 columna
#y todas las carpetas reccoridas como otras columnas, con un 1 en cada instancia


    

"""with open("resultados.csv", "w", newline='') as f:
    write = csv.writer(f,delimiter=";")
    write.writerow(["Lectura_IMG","Carpeta","File"])
    for row in mapa:
        num = str(row[0]).replace('.',',')
        path = str(row[1])
        file = str(row[2])
        write.writerow([num, path, file])
    
    f.close()"""
    
"""mapa.sort()
f = open(path + '/resultados.txt','w')
for element in mapa:
    aux = str(element[0]) + ";" + str(element[1])
    print(aux)
    f.write(aux + "\n"  )

f.close()"""

print("fin")