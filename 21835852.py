import time
import math
import multiprocessing as mp
import random

#Función Fibonacci con un diccionario de datos donde almacenamos los resultado para recuperarlos en caso de ser necesario
def fib(n, c={0:1, 1:1}):
    if n not in c:
        x = n // 2
        c[n] = fib(x-1) * fib(n-x-1) + fib(x) * fib(n - x)
    return c[n]

#Función Fibonacci básica 
def fibonacci(n): 
    a = 0
    b = 1
    if n < 0: 
        print("Incorrect input") 
    elif n == 0: 
        return a 
    elif n == 1: 
        return b 
    else: 
        while n > 2:
            a = b 
            b = a + b
            n-=1
        return b

def par_fibo(n):
    n_cores = mp.cpu_count() #cuenta los cores de mi equipo
    operaciones = math.ceil(n/n_cores)#calculos a realizar por cada core
    print("Numero de Cores disponibles: ", n_cores)
    print("Operaciones a realizar por core: ", operaciones)
    MC = mp.RawArray('i', n)# Array de memoria compartida entre cores
    cores = [] #Creamos un array donde vamos a guardar las funciones de cada core
    
    for core in range(n_cores): #Por cada core de nuestro ordenador
        i_MC = min(core * operaciones, n) #Marcamos inicio del trabajo
        f_MC = min((core + 1) * operaciones, n)#Marcamos final de trabajo
        cores.append(mp.Process(target=par_core, args=(MC, i_MC, f_MC)))#Metemos el trabajo de cada core en el array de cores creado anteriormente
    for core in cores:#Para cada core en mi equipo
        core.start()#Los ponemos a trabajar
    for core in cores:#Para cad core en mi equipo
        core.join()#Bloqueamos posibles llamadas hasta que terminen su tarea actual
    return MC

def par_core(MC, i_MC, f_MC): #Trabajo que realiza cada core 
    for i in range(i_MC, f_MC):
        if i == i_MC:
            MC[i] = fib(i)
        elif i == i_MC+1:
            MC[i] = fib(i)
        else:
            MC[i] = MC[i-1] + MC[i-2]

def fibonacciExecute(n):
    
    start = time.time()
    a = fib(n)
    end = time.time()

    start1 = time.time()
    par_fibo(n)
    end1 = time.time()

    print("Número de la serie de fib a calcular: ", n)
    print("Número Calculado demasiado grande, ralentiza el ordenador", a)
    

    print ("Tiempo total fibonacci Secuencialmente calculado: ", end - start)
    print ("Tiempo total fibonacci Paralelamente calculado: ", end1 - start1)

def merge(nlist):
    if len(nlist)>1: #Comprobamos que la lista es mayor que 1
        mid = len(nlist)//2 #Dividimos la lista en 2 para aplicar DyV
        left = nlist[:mid]
        rigth = nlist[mid:]

        merge(left) #Realizamos la llamada para la primera mitad
        merge(rigth) #Realizamos la llamada para la segunda mitad
        i=j=k=0 #Inicializamos variables para recorrer cada mitad de la lista pasada por parametros
        while i < len(left) and j < len(rigth):
            if left[i] < rigth[j]: #Ordenamos los elementos de la lista en funcion de si están en la primera mitad o en la segunda
                nlist[k]=left[i]
                i=i+1
            else:
                nlist[k]=rigth[j]
                j=j+1
            k=k+1
                
        while i < len(left): #Añadimos a la lista final de cada una de las mitades
            nlist[k]=left[i]
            i=i+1
            k=k+1

        while j < len(rigth):
            nlist[k]=rigth[j]
            j=j+1
            k=k+1
        return nlist #Devolvemos la lista final

def paralel_merge(list, inicio, fin): #Pasamos el inicio y el final de la sublista que va a trabajar cada core
    lista = list[inicio:fin]
    merge(lista)

def MergeSort(a):
    n_cores = mp.cpu_count() #cuenta los cores de mi equipo
    subElement = int(len(a)/n_cores)#tamaño del subarray para cada core
    print("Numero de Cores disponibles: ", n_cores)
    print("Elementos por subarray: ", subElement)
    MC = mp.RawArray('i', len(a))# Array de memoria compartida entre cores
    MC= a   #guardamos el array que queremos ordenar en el array de memoria compartida
    cores = [] #Creamos un array donde vamos a guardar las funciones de cada core
    for core in range(n_cores): #Por cada core de nuestro ordenador
        cores.append(mp.Process(target=paralel_merge, args=(MC, subElement*core, subElement*(core+1)))) #Metemos el trabajo de cada core en el array de cores creado anteriormente
    for core in cores:#Para cad core en mi equipo
        core.start()#Los ponemos a trabajar
    for core in cores:#Para cad core en mi equipo
        core.join()#Bloqueamos posibles llamadas hasta que terminen su tarea actual
    merge(MC)
    
            

def mergeExecute(n):
    A = [random.randint(0,215) for j in range(n)] #Creamos una lista del tamaño del numero de expediente 21845538
    B = A
    print("Array a ordenar: ", A)

    start = time.time()
    MergeSort(A)
    end = time.time()
    print("Array Ordenado: ", A)

    start1 = time.time()
    merge(B)
    end1 = time.time()
    print("Array Ordenado: ", B)

    

    print ("Tiempo total merge Paralelo: ", end - start)
    print ("Tiempo total merge Secuencial: ", end1 - start1)

if __name__ == '__main__':
    print("Introduce usuario:")
    usuario = input()
    if usuario == "jesus":
        print("introduce contraseña:")
        contra = int(input())
        if contra == 21835852:
            print("Seleccione lo que quiera:")
            print("1- Fibonacci")
            print("2- Mergesort")
            x = int(input())
            print(x)
            if x == 1:
                print("¿Qué numero quieres usar?")
                num=int(input())
                fibonacciExecute(num)
            elif x == 2:
                print("¿Qué tamaño de array quieres?")
                num=int(input())
                mergeExecute(num)
            else:
                print("Seleccion no valida, por favor seleccione otro")
        else:
            print("Contraseña incorrecta, vuelva a iniciar el programa")
    else:
        print("Usuario incorrecto, vuelva a iniciar el programa")
    