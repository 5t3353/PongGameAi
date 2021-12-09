from pandas import DataFrame ,read_csv ,concat
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor

class AiModel:

    def __init__(self,file):
        self.file = file
        self.data = read_csv(self.file)
        self.X = self.data.drop(columns = "movement").values
        self.y = self.data["movement"].values
        self.X_train , self.X_test ,self.y_train ,self.y_test = train_test_split(self.X,
                                                                                 self.y,
                                                                       random_state = 1,
                                                                        test_size = 0.3)

        self.model_pipe = Pipeline(steps = [('preprocessor',MinMaxScaler()),
                                            ('model',GradientBoostingRegressor(n_estimators = 500))])

    def fit_model(self):

        self.model_pipe.fit(self.X_train, self.y_train)

        train_score = self.model_pipe.score(self.X_train,
                                            self.y_train)

        test_score = self.model_pipe.score(self.X_test,
                                           self.y_test)

        print(f"Train score: {round(train_score,2)*100} %")

        print(f"Test score: {round(test_score,2)*100} %")
