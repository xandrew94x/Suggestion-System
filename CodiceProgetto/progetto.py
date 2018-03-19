from dataset import Dataset
from pprint import pprint
import json
dataset = Dataset("dataset/dati.json")

training_set, test_set = dataset.splitTrainingTest(0.7)
print "Totale grandezza cartella primo utente: ", dataset.getUserLength(0)
print training_set.getUserLength(0)
print test_set.getUserLength(0)

training_set.saveInJSON('trainingset')

from tools import *
import numpy as np
from __future__ import division
games_list = training_set.getUserGames() #ritorna una lista di giochi senza doppioni di tutti i training-set
lista_test_set = test_set.getUserGames() #ritorna una lista di giochi senza doppioni del test-set

matrix = np.zeros((len(games_list), len(games_list)), dtype=np.int) #inizializza la matrice a 0

#incrementa valori nella matrice per avere pesi dei giochi

for a in range(dataset.getNumberOfUsers()):                          #scorre gli utenti
    lista = training_set.getUserData(a)                              #prende l'utente di indice a
    for e in range(len(lista)):                                      #scorre i giochi dell'utente a
        for b in range(len(games_list)):                             #scorre la lista di giochi senza doppioni
            if lista[e] == games_list[b]:                            #compara i nomi dei giochi dell'utente a con la lista dei giochi senza doppioni
                indice_games_list = b                                #metto l'indice della corrispondenza trovata nella lista di giochi senza doppioni (si può anche levare)
                for i in range(len(games_list)):                     #scorre la riga della matrice
                    if i == indice_games_list:                       #controlla se gli indici della matrice corrisponde al gioco
                        for j in range(len(games_list)):             #scorre la colonna della matrice del gioco 
                            #se utente ha gioco e, ha anche il gioco j-esimo?
                            for c in range(len(lista)):              #controlla se il gioco j-esimo è posseduto dall'utente a nella lista di giochi c
                                if games_list[j] == lista[c]:        #controlla il gioco j con il gioco c-esimo
                                    matrix[i][j] = matrix[i][j] + 1  #se c'è (se esiste una corrispondenza) incrementa la posizione nella matrice
print matrix

#calcolo della probabilità

for a in range(dataset.getNumberOfUsers()):                               #scorre gli utente
    #print "Utente lunghezza dataset: ", dataset.getUserLength(a)
    lista = training_set.getUserData(a)                                   #prende l'utente di indice a
    dizionario = dict()                                                   #crea un dizionario
    for l in range(len(lista_test_set)):                                  #scorre la lista del test-set senza doppioni
        indice_games_test = get_indice_games_test(lista_test_set, games_list,l) #prende l'indice del gioco del test-set corrispondente alla matrice dei giochi
        probabilitaTOT = 0                                                #inizializzo prob. a zero
        for e in range(len(lista)):                                       #scorre i giochi dell'utente a        
            indice_games_list = get_indice_game_list(lista, games_list,e) #prende l'indice del gioco del training-set dell'utente a corrispondente alla matrice dei giochi
            somma_valori = get_somma_valori(games_list,indice_games_test,matrix)  #serve per trovare la Ci, quindi somma la colonna di valori
            probabilita = matrix[indice_games_test][indice_games_list] / somma_valori  #serve per calcolare la probabilita = Nij/Ci
            probabilitaTOT = probabilitaTOT + probabilita                  #somma le probabilità
            #prob = probabilitaTOT/len(lista)                              #esegue l'ultimo calcolo prob-tot/n70%
            dizionario[lista_test_set[l]] = probabilitaTOT                 #mette la prob. nel dizionario
        print l,") probabilita che Utente",a ," abbia gioco ", lista_test_set[l], " -> ", probabilitaTOT
    path = 'result/Utente' + str(a) + '.json'                              #impostiamo il path dove salvare il dizionario
    crea_json_path(path,dizionario)                                        #funzione per creare il file json nel path selezionato




#filter_games(dataset)
#get_random_games("Utente0", 10)
