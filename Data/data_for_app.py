# import the necessary libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import kde
import numpy as np

# import the class created in other files
from Data.teams import Teams


# Class to get the datas pre formatted for the application graphics + leaderboard showing
class Data_For_App(Teams):
    
    # Iniitalize the class with the file path
    def __init__(self, file_path : str) :
        super().__init__(file_path)

    # Function to get a Gaussian curve from a list of data
    def get_gaussienne_graph(self, list_data, name_fig, title, is_by_name, own_time):
        density = kde.gaussian_kde(list_data)
        x = np.linspace(min(list_data), max(list_data), 1000)
        y = density(x)

        plt.clf()
        plt.scatter(list_data, density(list_data), color="red", zorder = 2, marker="+", s=50)
        plt.plot(x, y, color="blue")
        plt.title(title)

        # Modify x-axis to show time in hh:mm format
        def format_time(value, _):
            hours = int(value // 3600)
            minutes = int((value % 3600) // 60)
            return f"{hours:02d}h{minutes:02d}"
        
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
        plt.gca().invert_xaxis()
        plt.gca().yaxis.set_visible(False)
        plt.ylabel("")
        plt.xlabel("Race Time")

         # If is_by_name is True, draw the red arrow to show where the result is 
        if is_by_name and own_time != 0:
            # Get the corresponding y-value for the team's time on the curve and then creating the arrow pointing toward the value
            y_own_time = density(own_time)
            plt.gca().annotate('', xy=(own_time, y_own_time), xytext=(own_time, -0.05), arrowprops=dict(facecolor='red', edgecolor='red', lw=2, linestyle='-'))

        plt.savefig(name_fig, dpi=500)
        
    # Function to get the create the overall and category graphs depeding on the parameters input
    def create_data_graphs(self, name : str, distance : float, sex : int, is_team_result : bool, fig_1 = "Data/left_figure.png", fig_2 = "Data/right_figure.png"):
        # for a team result
        if is_team_result:
            overall_title = "Overall teams results"
            if sex == self.team_type.MIXED :
                category_title = "Mixed teams results"
            elif sex == self.team_type.MEN :
                category_title = "Men teams results"
            elif sex == self.team_type.WOMEN :
                category_title = "Women teams results"
            # no name in the search, we then search for the teams results for both the category : by sex and the mixed one
            if name == "" :
                # get the teams
                teams_overall = self.get_teams()
                time_teams_overall = [team.data[self.field.TEAM_TIME] for team in teams_overall]
                self.get_gaussienne_graph(time_teams_overall, fig_1, overall_title, False, 0)

                # get the teams for the category
                teams_category = self.get_teams_by_category(sex)
                time_teams_category = [team.data[self.field.TEAM_TIME] for team in teams_category]
                self.get_gaussienne_graph(time_teams_category, fig_2, category_title, False, 0)

            else : 
                team_searched = self.get_team(name)
                team_searched_time = team_searched.data[self.field.TEAM_TIME]

                # get the teams
                teams_overall = self.get_teams()
                time_teams_overall = [team.data[self.field.TEAM_TIME] for team in teams_overall]
                self.get_gaussienne_graph(time_teams_overall, fig_1, overall_title, True, team_searched_time)

                # get the teams for the category
                teams_category = self.get_teams_by_category_by_name(name)
                time_teams_category = [team.data[self.field.TEAM_TIME] for team in teams_category]
                self.get_gaussienne_graph(time_teams_category, fig_2, category_title, True, team_searched_time)

        # for an individual result
        else :
            if distance == 10 : 
                overall_title = "Overall runners results for 10km"
                category_title = "Runners results by category for 10km"
            elif distance == 7.2 :
                overall_title = "Overall runners results for 7.2km"
                category_title = "Runners results by category for 7.2km"
            elif distance == 5 :
                overall_title = "Overall runners results for 5km"
                category_title = "Runners results by category for 5km"
            
            # no name in the search, we then search for the individual results for both the category : by sex and the mixed one
            if name == "" :
                # get the overall results for the distance
                distance_overall = self.Distance_Relay("", distance, self.team_type.MIXED, self.get_teams()).distance_relay
                time_distance_overall = [distance / runner.speed * 3600 for runner in distance_overall if runner.speed != 0]
                self.get_gaussienne_graph(time_distance_overall, fig_1, overall_title, False, 0)

                # get the results for the category for the distance
                distance_category = self.Distance_Relay("", distance, sex, self.get_teams()).distance_relay
                time_distance_category = [distance / runner.speed * 3600 for runner in distance_category if runner.speed != 0]
                self.get_gaussienne_graph(time_distance_category, fig_2, category_title, False, 0)

            else :
                runner_searched = self.Distance_Relay(name, distance, sex, self.get_teams()).runner_searched
                runner_searched_time = distance / runner_searched.speed * 3600 if runner_searched.speed != 0 else 0

                # get the overall results for the distance
                distance_overall = self.Distance_Relay("", distance, self.team_type.MIXED, self.get_teams()).distance_relay
                time_distance_overall = [distance / runner.speed * 3600 for runner in distance_overall if runner.speed != 0]
                self.get_gaussienne_graph(time_distance_overall, fig_1, overall_title, True, runner_searched_time)

                # get the results for the category for the distance
                distance_category = self.Distance_Relay("", distance, runner_searched.sex, self.get_teams()).distance_relay
                time_distance_category = [distance / runner.speed * 3600 for runner in distance_category if runner.speed != 0]
                self.get_gaussienne_graph(time_distance_category, fig_2, category_title, True, runner_searched_time)
               
        return fig_1, fig_2
