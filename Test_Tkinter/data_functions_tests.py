# import all the other files and run the main code of the application
from Data import Teams, Data_For_App


'''
teams = Teams("../Data/Ekiden_resultats.txt")
# if there is a name, it only search for the name and don't care about the rest exept the category, if it's mixed, then it will search everyone to get the scratch time
distance_relay_runners = Teams.Distance_Relay("Cuel", 7.2, Teams.team_type.WOMEN, teams.get_teams())
print("Relay distance : ", distance_relay_runners.distance)
for runner in distance_relay_runners.distance_relay:
    print(runner.name, runner.speed)
'''

'''
data = Data_For_App("../Data/Ekiden_resultats.txt")
distance_relay_runners = data.Distance_Relay("Durand", 7.2, Teams.team_type.MIXED, data.get_teams())
print("Relay distance : ", distance_relay_runners.distance)
for runner in distance_relay_runners.distance_relay:
    print(runner.name, runner.speed)
'''

'''
data = Data_For_App("../Data/Ekiden_resultats.txt")
fig_1, fig_2 = data.create_data_graphs("", 7.2, Teams.team_type.MIXED, True)
'''
