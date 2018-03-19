import random
import json
import collections

#ritorna la somma di tutti i contatori di gioco rispetto a tutti gli altri (somma i valori di un intera riga della matrice)
def get_somma_valori(game_list,indice_games_test,matrix):
    somma_valori = 0
    for i in range(len(game_list)):
        somma_valori = somma_valori + matrix[indice_games_test][i]
    return somma_valori

#ritorna l'indice del gioco di un utente nella lista dei giochi senza doppioni
def get_indice_game_list(lista, games_list,e):
    indice_games_list = -1
    for b in range(len(games_list)):
        if lista[e] == games_list[b]:
            indice_games_list = b
    return indice_games_list

#ritorna l'indice del gioco nel test_set, nella lista dei giochi senza doppioni
def get_indice_games_test(lista_test_set, games_list,l):
    indice_games_test = -1
    for g in range(len(games_list)):
        if lista_test_set[l] == games_list[g]:
            indice_games_test = g
    return indice_games_test

#crea un file json e ci salva i dati in dizionario
def crea_json_path(path,dizionario):
    path_to_dataset = path
    with open(path_to_dataset, 'w') as fp:
        #tramite il metodo di collections andiamo ad ordinare i giochi in ordine decrescente in base alla probabilita
        json.dump(collections.OrderedDict(sorted(dizionario.items(), key=lambda t: t[1], reverse=True)), fp)
    print "Done"

#Per la lista di giochi da consigliare prendiamo tutti i giochi nella cartella result che non sono gia nella
#libreria dell'utente e che hanno la probabilita di essere potenzialmente acquistabili dall'utente in questione
#al di sopra di una soglia. Calcolata come la somma delle probabilita dei giochi consigliati, non posseduti dall'utente
#fratto il numero tot di giochi consigliati e non posseduti dall'utente.

def Games_not_owned(d1, d2):                      #d1 = lista dei giochi suggeriti con le probabilita, d2 = libreria dell'utente
    dati_finali = dict()                          #creo un dizionario
    somma_tot = 0
    chiavi = d1.keys()                            #prendiamo la lista dei nomi di giochi che sono le chiavi del dizionario d1
    for i in range(len(chiavi)):                  #scorriamo i nomi dei giochi
        counter = 0
        for j in range(len(d2)):                  #e la libreria dell'utente
            if chiavi[i] != d2[j]:
                counter += 1                      #aumentiamo il contatore ogni volta che trovo un elemento diverso
        if(counter == len(d2)):                   #se non ci sono elementi uguali il contatore = alla dim. libreria di giochi dell'utente
            dati_finali[chiavi[i]] = d1[chiavi[i]]
            somma_tot += d1[chiavi[i]]            #somma = somma delle probabilita dei giochi suggeriti che l'utente non possiede gia
    soglia = somma_tot/len(dati_finali)           #calcoliamo la soglia con la quale filtrare i giochi da consigliare
    return soglia, dati_finali

def filter_games(obj):                                        #filtriamo i giochi in base alla soglia
    for i in range(obj.getNumberOfUsers()):                   #per ogni utente
        path = "result/Utente" + str(i) + ".json"
        d1 = json.load(open(path))                            #prendiamo il dizionario dei giochi suggeriti con le rispettive probabilita
        d2 = obj.getUserData(i)                               #prendiamo la libreria di giochi dell'utente
        dizionario_parziale = dict()                          #creiamo un nuovo dizionario dove salvare i giochi suggeriti
        soglia, dizionario = Games_not_owned(d1, d2)          #prendiamo soglia e dizionario dei giochi suggeriti e non posseduti da utente
        print "Soglia utente" + str(i) + "=" + str(soglia)
        for name in dizionario:                               #scorriamo i giochi che l'utente non possiede
            if(dizionario[name] >= soglia):                   #prendiamo solo quelli con una probabilita >= alla soglia
                dizionario_parziale[name] = dizionario[name]  #li salviamo nel nuovo dizionario
        user = "Utente" + str(i)
        path_to_dataset = 'giochiSuggeriti/' + user + '.json'
        crea_json_path(path_to_dataset,dizionario_parziale)

#stampa tutti i giochi suggeriti
def get_game_list(utente):                                    #prende in input una stringa [nome file json]
    path = "giochiSuggeriti/"+ str(utente) + ".json"
    d1 = json.load(open(path))
    pprint (d1)

#stampa un numero (count) di giochi suggeriti in modo random
def get_random_games(utente, count):                          #prende in input una stringa [nome file json] e quanti giochi mostrare
    path = "giochiSuggeriti/"+ str(utente) + ".json"
    d1 = json.load(open(path))
    for a in range(count):
        print random.choice(d1.keys())
