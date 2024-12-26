# import the necessary libraries
from enum import Enum


# Define the teams_data class to parse the data and store the team information
class Teams:

    # Enum to define the team categories
    class team_type(Enum):
        MEN = 0
        WOMEN = 1
        MIXED = 2 # Admin is included in the mixed category
        UNKOWN = 4


    # Enum to define the fields of the team_info object
    class field(Enum):
        TEAM_NAME = 0
        TEAM_CATEGORY = 1
        TEAM_TIME = 2
        TEAM_RANKING_IN_CATEGORY = 3
        TEAM_OVERALL_RANKING = 4


    # Define the runner class to store the data of each runner
    class runner:
        def __init__(self, name: str, sex: int, passage_number: int, distance: float, medley_time: int, speed: float):
            self.name = name
            self.sex = Teams.team_type(sex)
            self.passage_number = passage_number
            self.distance = distance
            self.medley_time = medley_time  # Time in seconds
            self.speed = speed # Speed in km/h


    # Define the team_info object to store the data of each team
    class team_info:
        # Initialize the team_info object with the team's name, category, time, runners, and ranking
        def __init__(self, name: str, category: int, time: int, category_ranking: int, ranking: int, runners: list):
            self.data = {
                Teams.field.TEAM_NAME: name,
                Teams.field.TEAM_CATEGORY: category,
                Teams.field.TEAM_TIME: time,
                Teams.field.TEAM_RANKING_IN_CATEGORY: category_ranking,
                Teams.field.TEAM_OVERALL_RANKING: ranking
            }
            self.runners = runners 


    # Initialize the teams_data object with the file path
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.teams = self._parse_teams()

    # Parse the teams data from the file, return a list of team_info objects
    def _parse_teams(self):
        with open(self.file_path, "r") as file:
            data = file.read().strip().split("\n")

        # Remove the first 5 lines of unnecessary data
        data = data[5:]
        number_of_teams = data.count("") + 1

        # Initialize lists to store each team's data
        teams_data_parsing = [[] for _ in range(number_of_teams)]
        team_index = 0
        while data:
            line = data.pop(0)
            if line == "":
                team_index += 1
                continue
            teams_data_parsing[team_index].append(line)

        # Process each team into team_info objects
        teams = []
        for i, team_info_parsing in enumerate(teams_data_parsing):
            if not team_info_parsing:
                continue
            
            # The first line gives us the data of the team
            team_info_line = team_info_parsing[0].strip().split("|")
            
            # Extract the team name
            team_name = team_info_line[0]
            
            # Get the ekiden total time in seconds
            team_time_str = team_info_line[1].strip().split(" ")[3].split(":")
            team_time = int(team_time_str[0])*3600 + int(team_time_str[1])*60 + int(team_time_str[2])
            
            # Get the team category number
            # Non classed teams have an extra word in the category
            delta = 0
            if team_info_line[2].strip().split(" ")[0] == "Non" :
                delta = 1
            team_category_str = team_info_line[2].strip().split(" ")[1+delta]
            if team_category_str == "Hommes":
                category = Teams.team_type.MEN
            elif team_category_str == "Dames":
                category = Teams.team_type.WOMEN
            elif team_category_str == "Mixte":
                category = Teams.team_type.MIXED
            elif team_category_str == "Admin":
                category = Teams.team_type.MIXED
            else:
                category = Teams.team_type.UNKOWN
            
            # Get the team ranking in its category
            category_team_ranking = team_info_line[2].strip().split(" ")[0][:2]
            if category_team_ranking[1] == '°':
                category_team_ranking = category_team_ranking[0]
            if category_team_ranking == "No":
                category_team_ranking = -1
            else :
                category_team_ranking = int(category_team_ranking)
            
            # Get the team overall ranking
            team_ranking = i+1

            runners = []
            # Process the runners data, 6 runners for line 3/4/5/6/7/8
            for i in range(2, 8) : 
                
                runner_info = team_info_parsing[i].split("\t")

                # Name and Sex
                runner_name = runner_info[1].strip()
                runner_sex = Teams.team_type.MEN if runner_info[2] == "M" else Teams.team_type.WOMEN

                # Runner passage number
                runner_passage_number = i-1

                 # Runner distance
                runner_distance = 7.2
                if (runner_passage_number == 1 or runner_passage_number == 3 or runner_passage_number == 5):
                    runner_distance = 5.0
                elif (runner_passage_number == 2 or runner_passage_number == 4):
                    runner_distance = 10.0

                # Medley time 
                medley_time_str = runner_info[4]
                medley_time = 0
                # Check if the time includes hours (separating the hours, minutes, and seconds differently if there is hours or not)
                if not 'X' in medley_time_str:
                    if 'h' in medley_time_str:
                        medley_time = 3600 * int(medley_time_str[0]) + 60 * int(medley_time_str[2:4]) + int(medley_time_str[5:7])
                    else:
                        medley_time = 60 * int(medley_time_str[0:2]) + int(medley_time_str[3:5])
            
                # Speed
                runner_speed_str = runner_info[5].strip()
                if runner_speed_str and runner_speed_str.replace(",", ".").replace(".", "", 1).isdigit():
                    runner_speed = float(runner_speed_str.replace(",", "."))
                else:
                    runner_speed = 0.0  # Or handle as needed (e.g., raise an error or set a default value)

                # Append the runner to the runners list
                partial_runner = Teams.runner(name=runner_name, sex=runner_sex, passage_number=runner_passage_number, distance=runner_distance, medley_time=medley_time, speed=runner_speed)
                runners.append(partial_runner)


            # Create a team_info instance and add it to the teams list
            team = Teams.team_info(name=team_name, category=category, time=team_time, category_ranking=category_team_ranking, ranking=team_ranking, runners=runners)
            teams.append(team)

        # Return the list of team_info objects
        return teams

    # Function to get the teams
    def get_teams(self):
        return self.teams
    
    # Function to get the team based on its name (or at least a part of it)
    def get_team(self, team_name: str):
        for team in self.teams:
            if team_name in team.data[Teams.field.TEAM_NAME]:
                return team
        return None
    
    # Function to get the teams of one category
    def get_teams_by_category(self, category):
        if category == Teams.team_type.UNKOWN:
            return self.teams
        return [team for team in self.teams if team.data[Teams.field.TEAM_CATEGORY] == category]
    
    # Function to get the teams of a category depending on the team name
    def get_teams_by_category_by_name(self, name : str):
        category_searched = -1
        for team in self.teams : 
            if name in team.data[Teams.field.TEAM_NAME] :
                category_searched = team.data[Teams.field.TEAM_CATEGORY]
                break
        return self.get_teams_by_category(category_searched)
    
    # Function to get the runners of a team
    def get_runners(self, team):
        return team.runners
    

    # Define the number relay class to store the data of each relay
    class Number_Relay:

        # Initialize the number relay object with the number of the relay and teams data
        def __init__(self, name : str, number: int, sex: int, teams: list):
            self.name = name
            self.number = number
            self.sex = sex
            self.teams = teams
            self.number_relay = self.get_number_relay(name, number, sex)

        # function to get the distance relay
        # the sex matter, because it will get the scratch time of the runners, or the ordering based on the sex
        def get_number_relay(self, name : str, number : int,  sex : int):
            self.name = name    
            self.number = number
            self.sex = sex
            relay_number = []
            # empty name means we want to get the relay based on the number, still looking at the sex
            if name == "":
                for team in self.teams:
                    if team.runners[self.number - 1].sex == sex or sex == Teams.team_type.MIXED : 
                        relay_number.append(team.runners[self.number - 1])
            # otherwise we want to get the relay based on the name, still looking at the sex
            else : 
                number_searched = -1
                sex_searched = -1
                for team in self.teams : 
                    for runner in team.runners : 
                        if name in runner.name : 
                            number_searched = runner.passage_number
                            self.number = number_searched
                            sex_searched = runner.sex
                            self.sex = sex_searched
                            break
                # if the number is not found, return an empty list since there is no runner with this name
                if number_searched == -1 :
                    return []
                for team in self.teams:
                    if team.runners[number_searched - 1].sex == sex or sex == Teams.team_type.MIXED : 
                        relay_number.append(team.runners[number_searched - 1])
            # return the list of the runners
            return relay_number


    # Define the distance relay class to store the data of each relay
    class Distance_Relay:

        # Initialize the distance relay object with the distance and teams data
        def __init__(self, name : str, distance: float, sex: int, teams: list):
            self.name = name
            self.distance = distance
            self.sex = sex
            self.teams = teams
            self.distance_relay = self.get_distance_relay(name, distance, sex)
            self.runner_searched = self.get_runner_by_name(name)

        # function to get the runner searched by the name
        def get_runner_by_name(self, name : str):
            for team in self.teams:
                for runner in team.runners : 
                    if name in runner.name :
                        return runner
            return None

        # function to get the distance relay
        # the sex matter, because it will get the scratch time of the runners, or the ordering based on the sex
        # no name means that we want to get the relay based on the distance, still looking at the sex
        # if we want a WOMEN but the name correspond to a MEN, it will return the MIXED relay
        def get_distance_relay(self, name : str, distance : float, sex : int):
            self.name = name
            self.distance = distance
            self.sex = sex
            relay_distance = []
            # empty name means we want to get the relay based on the distance, still looking at the sex
            if name == "":
                for team in self.teams:
                    for runner in team.runners : 
                        if runner.distance == distance and (runner.sex == sex or sex == Teams.team_type.MIXED) : 
                            relay_distance.append(runner)
            # otherwise we want to get the relay based on the name, still looking at the sex
            else : 
                distance_searched = -1
                sex_searched = -1
                for team in self.teams : 
                    for runner in team.runners : 
                        if name in runner.name :
                            distance_searched = runner.distance
                            self.distance = distance_searched
                            sex_searched = runner.sex
                            self.sex = sex_searched
                            break
                # if the distance is not found, return an empty list since there is no runner with this name
                if distance_searched == -1 or sex_searched == -1 :
                    return []
                for team in self.teams:
                    for runner in team.runners : 
                        if runner.distance == distance_searched and (runner.sex == sex_searched or sex == Teams.team_type.MIXED) : 
                            relay_distance.append(runner)
            # return the list of the runners
            return relay_distance
