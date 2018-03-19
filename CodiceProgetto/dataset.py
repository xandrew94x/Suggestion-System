import numpy as np
from copy import copy
import json
from pprint import pprint

class Dataset:
    def __init__(self, path_to_dataset):                 #costruttore
        self.path_to_dataset = path_to_dataset           #cartella/file da dove prendere il dataset
        self.data = json.load(open(path_to_dataset))
        self.games = dict()
        for i in range(len(self.data)):                  #creiamo il nuovo dizionario con tutti gli utenti e i rispettivi giochi
            user = "Utente"+str(i)
            self.games[user] = self.data[i][user]

    #stampa il dataset dell'istanza corrente
    def printDataset(self):
        pprint (self.games)
        
    #ritorna il numero di utenti nel nostro dataset
    def getNumberOfUsers(self):
        return len(self.games)
    
    #ritorna la dimensione del dataset di un determinato utente (numero di giochi)
    def getUserLength(self, user):
        key = "Utente" + str(user)
        return len(self.games[key])
    
    #ritorna la lista dei giochi di un determinato utente
    def getUserData(self, user):
        key = "Utente" + str(user)
        return (self.games[key])
    
    #ritorna la dimensione totale dell'istanza corrente. es numero totale di elementi dentro il dataset
    def getLength(self):
        return sum([len(x) for x in self.games.values()])
    
    #ritorna gli utenti
    def getUsers(self):
        return sorted(self.games.keys())
    
    #divide il dataset in due parti, iniziando a tagliare da percent_train
    def splitTrainingTest(self, percent_train):
        training_games=dict()                                      #inizializza i dizionari che conterranno
        test_games=dict()                                          #i giochi di training e test
        for user in self.getUsers():                               #per ogni utente
            games = self.games[user]                               #ottieni la lista dei nomi dei giochi relativi a quell'utente
            shuffled_names = np.random.permutation(games).tolist() #li mischi e da numpy array passiamo alle liste
            split_idx=int(len(shuffled_names)*percent_train)       #calcoliamo l'indice da dove dividere
            training_games[user]=shuffled_names[0:split_idx]       #salva i primi nomi nella variabile di training
            test_games[user]=shuffled_names[split_idx::]           #e i restanti in quella di test

        training_dataset = copy(self)                              #creiamo una copia dell'oggetto per il dataset del training set
        training_dataset.games = training_games                    #e nell'attributo games mettiamo i giochi del training set

        test_dataset = copy(self)                                  #stessa cosa per il test set
        test_dataset.games = test_games

        return training_dataset, test_dataset
    
    #controlla se ci sono doppioni nella lista
    def control(self, lista, item):
        for i in range(len(lista)):
            if(item == lista[i]):
                return False
        return True

    #ritorna una lista con tutti i nomi dei giochi di tutti gli utenti(senza doppioni)
    def getUserGames(self):
        game_names = list()
        for user in self.games:                                    #per ogni utente
            for i in range(len(self.games[user])):                 #scorriamo i giochi
                if(self.control(game_names, self.games[user][i])): #chiamiamo la funzione di sopra per vedere se il nome games[user][i]
                    game_names.append(self.games[user][i])
        return game_names

#salva in un file json la lista di giochi, creata con la funzione di sopra
    def saveInJSON(self, fileName):
       path_to_dataset = 'training_dataset/' + fileName + '.json'
       with open(path_to_dataset, 'w') as fp:
           json.dump(self.getUserGames(), fp)
