import pandas as pd
import numpy as np

cities = pd.read_csv("data/cities.csv")
providers = pd.read_csv("data/providers.csv")
stations = pd.read_csv("data/stations.csv")
ticket_data = pd.read_csv("data/ticket_data.csv")

#prix min
minPrice = ticket_data['price_in_cents'].min()
print("min price in cents : "+str(minPrice))

#prix max
maxPrice = ticket_data['price_in_cents'].max()
print("max price in cents : "+str(maxPrice))

#prix moyen
meanPrice = ticket_data['price_in_cents'].mean()
print("mean price in cents : "+str(meanPrice))

#ajout d'une colonne contenant les différences entre les dates de départs et les date d'arrivées
ticket_data['diff_dates'] = pd.to_datetime(ticket_data['arrival_ts']) - pd.to_datetime(ticket_data['departure_ts'])


#durée min par trajet
minTimePerPath = ticket_data.groupby(['o_station','d_station']).diff_dates.min()
print('\nmin time per path :')
print(minTimePerPath)

#durée max par trajet
maxTimePerPath = ticket_data.groupby(['o_station','d_station']).diff_dates.max()
print('\nmax time per path :')
print(maxTimePerPath)

#durée moenne par trajet
ticket_data['mean_time'] = ticket_data['diff_dates'].values.astype(np.int64)
meanTimePerPath = ticket_data.groupby(['o_station','d_station']).mean()
meanTimePerPath['mean_time'] = pd.to_timedelta(meanTimePerPath['mean_time'])
print('\nmean time per path :')
print(meanTimePerPath)

#calcul de différence de prix moyens
ticket_data['price_mean_diff'] = ticket_data['price_in_cents'].sub(ticket_data.groupby(['o_station','d_station'])['price_in_cents'].transform('mean'))


#associer les différents types de transport des providers avec le df ticket_data
dict_transport = providers.set_index('id').to_dict()['transport_type']
ticket_data = ticket_data.replace(dict_transport)

train_ticket_data = ticket_data.loc[ticket_data['company']=='train']

print('\nmean price diff per train :')
print(train_ticket_data)
            



