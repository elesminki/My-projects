#Importa la llibrería random per a fer les tirades
import random
#Importa la llibrería per a executar comandes de terminal en python (solament utilitzarem cls)
import os

#Funcions:

def mostrarMenu():
    #Es mostra el missatge i es comprova si l'opció escollida és correcta
    #En cas de que no, entrem en un bucle fins que escollim la correcta.
	msg = "\nBenvinguts, jugadors, a l' Oca en Python!\nEscull una opció escrivint el número corresponent:\n1.Inicialitzar Joc\n"
	msg +="2.Visualitzar taulell \n3.Jugar\n0.Sortir" 
	print(msg)
	op = input()
	while not op.isnumeric() or int(op) > 3 or int(op) < 0:
		op = input('\033[41m'+"Opció incorrecte!"+'\033[40m' + "\n" + msg + "\n")
	return int(op)


def generarTaulell():
    # Declarem la posició de cada casella especial i generem les caselles
    l = []
    oques = [5, 9, 14, 18, 23, 27, 32, 36, 41, 45, 50, 54, 59]
    for i in range(1, 64):
        if i in oques:
            l.append("|OCA      ")
        elif i == 26 or i == 53:
            l.append("|DAUS     ")
        elif i == 42:
            l.append("|LAB.     ")
        elif i == 58:
            l.append("|MORT     ")
        else:
            aux = " " if (i<10) else ""
            l.append(f"|{aux}{i}       ")
    return l



def inicialitzarAltreJoc():
	jugadors.clear()
	for i in range(n):
		jugadors.append(1)
	global taulell
	taulell.clear()
	taulell = generarTaulell()
	for i in range(n):
		print(fitxes[i], end="   ")
	print()
	return

def inicialitzarJoc():
    #Concretem el número de jugadors i generem el taulell
    inicialitzarFitxes()
    global n
    n = int(input("Indica quants jugadors sereu (2-6)\n"))
    global jugadors
    inicialitzarAltreJoc()


def mostraTaulell(taulell):
    #Mostra 16 caselles, després fa un salt de línea
    for i in range(len(taulell)):
        if i+1 in jugadors:
            #Mostra la fitxa del jugador en la posició corresponent
            fitxs = ""
            k = 0
            for j in range(len(jugadors)):
                if jugadors[j] == i + 1:
                    fitxs += fitxes[j]
                    k += 1
            espais = (5 - k) * " "
            print(taulell[i][:5] + fitxs + espais, end="")
        else:
            print(taulell[i], end="")
        if i % 16 == 0:
            print("|")
    print("|")
    return


def Jugar(tau):
    #Limpia el terminal fent un cls
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    #Comprova que la partida encara sigui activa i declara el torn
    partidaActiva = True
    torn = -1
    tir = 0
    while partidaActiva:
        torn = (torn + 1) % len(jugadors)
        canviTorn = False

        #Els jugadors tiren els daus fins que algú guanya
        while not canviTorn and jugadors[torn] < 63:
            tir += 1
            canviTorn = ferUnaTirada(tau, torn)
            mostraTaulell(taulell)
            input("\nPrem Enter per continuar...")
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
        #Declara el fi de la partida i mostra el missatge final
        if jugadors[torn] == 63:
            partidaActiva = False
            print(f"Enhorabona, jugador {torn+1}!!! Has guanyat la partida!\n")
            mostraTaulell(taulell)
            inicialitzarAltreJoc()

def inicialitzarFitxes():
    #Generem les fitxes i el seu color en cada cas
    global fitxes
    negre = '\033[40m'
    vermell = '\033[41m'
    verd = '\033[42m'
    groc = '\033[43m'
    blau = '\033[44m'
    lila = '\033[45m'
    cyan = '\033[46m'
    gris = '\033[47m'

    fitxes = []
    fitxes.append(verd + " " + negre)
    fitxes.append(blau + " " + negre)
    fitxes.append(vermell + " " + negre)
    fitxes.append(groc + " " + negre)
    fitxes.append(lila + " " + negre)
    fitxes.append(cyan + " " + negre)
    fitxes.append(gris + " " + negre)	
    
    
def ferUnaTirada(tau, torn):
    #Genera un número com si tiressim els daus
    tirada = random.randint(1, 6)
    print(f"El jugador {torn + 1} ha tret un {tirada}!\n")
    
    #Moure la fitxa
    jugadors[torn] += tirada
    
    #Comprova que el jugador no es pugui passar de la casella final
    if jugadors[torn] > 63:
        jugadors[torn] = 63
    #Comprova que el jugador no es pugui passar de la casella inicial
    elif jugadors[torn] < 1:
        jugadors[torn] = 1


    #Declara la variable utilitzada per canviar el torn dels jugadors quan sigui necessari
    canviTorn = comprovarAccionsTirada(tau, torn)
    return canviTorn
def comprovarAccionsTirada(tau, torn):
    casella = tau[jugadors[torn] - 1]
    
    #En cas de que la casella sigui una OCA, fer:
    if "OCA" in casella:
        print('\033[44m'+f"El jugador {torn + 1} ha arribat a la casella {jugadors[torn]}, una OCA!\n\"D' oca en oca i tiro perquè em toca!\"\n"+'\033[40m')
        segOca = None
        for i in range(jugadors[torn], len(tau)):
            if "OCA" in tau[i]:
                segOca = i
                break
            
            #Mou al jugador corresponent a la seguent OCA
        if segOca:
            jugadors[torn] = segOca + 1
            return False
        else:
            return True
        
    #En cas de que la casella sigui uns DAUS, fer:
    elif "DAUS" in casella:
        print('\033[44m'+f"El jugador {torn + 1} ha arribat a la casella {jugadors[torn]}, uns DAUS!\n"+'\033[40m')
        segDaus = None
        for i in range(len(tau)):
            if "DAUS" in tau[i] and i != jugadors[torn] - 1:
                segDaus = i
                break
        
        if segDaus:
            #Mou al jugador corresponent als seguents DAUS
            jugadors[torn] = segDaus + 1
            return False
        else:
            return True
    
    #En cas de que la casella sigui el LABERINT, fer:
    elif "LAB." in casella:
        print('\033[41m'+f"El jugador {torn + 1} ha arribat a la casella {jugadors[torn]}, el LABERINT...\n"+'\033[40m')
        jugadors[torn] = 30
        return True
    
    #En cas de que la casella sigui la MORT, fer:
    elif "MORT" in casella:
        print('\033[41m'+f"El jugador {torn + 1} ha arribat a la casella {jugadors[torn]}, la MORT...\n"+'\033[40m')
        jugadors[torn] = 1
        return True
    else:
    #En cas de que la casella sigui una Casella Normal, fer:
        return True



#Aquí comença el main:

#Declaració de variables
taulell = []
jugadors = []
fitxes = []
opcio = -1

#Bucle principal
while opcio != 0:
	#Crida a la funció que toca segons el número escollit
	#Si el jugador escull 0 el bucle para, deixant el joc
	opcio = mostrarMenu()
	if opcio == 1:
		inicialitzarJoc()
		mostraTaulell(taulell)
	elif opcio == 2:
		mostraTaulell()
	elif opcio == 3:
		Jugar(taulell)