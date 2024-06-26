import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

from blocks import EstimatorTransformer


if __name__ == "__main__":
    
    # Seed
    np.random.seed(123)

    # Params
    length, paths = 20, 10

    # Data
    X_train = pd.DataFrame(np.random.normal(size=(length, paths)))
    y_train = pd.DataFrame(np.random.normal(size=(length, paths)))
    y_test = pd.DataFrame(np.random.normal(size=(length, paths)))
    
    # Model
    model = EstimatorTransformer(LinearRegression())
    model.fit_transform(X_train, y_train)
    model.transform(y_test)
    #            0         1         2  ...         7         8         9
    # 0  -3.363745 -0.203620  0.043249  ...  1.659705 -0.799401  0.642322
    # 1  -0.095521 -0.087771 -1.277199  ...  0.140047  0.305322 -0.363892
    # 2  -0.164604  0.664352  1.009387  ... -0.954831 -0.263356 -0.485470
    # 3   1.313499 -0.777076 -0.588599  ...  0.171128 -0.086057  0.500458
    # 4  -1.999156  0.558689 -1.210043  ...  1.700496 -0.599200  0.964584
    # 5  -2.323592  1.164172  0.426562  ...  0.155383 -0.915018 -0.196161
    # 6  -1.605306  0.677072 -1.019580  ...  0.441971 -1.081010  0.092056
    # 7  -2.674790 -0.549887  1.200154  ... -0.364424  0.210336  0.914847
    # 8  -0.935067  1.330428  0.094560  ... -0.981395 -0.747905 -0.338797
    # 9   0.765563  0.260773  1.264486  ... -1.545478 -0.173539 -1.047471
    # 10 -3.568304 -0.502000  1.011380  ...  0.171509  0.608375  1.126085
    # 11 -0.908468 -0.695773  0.437262  ...  0.326231 -1.066990  1.118981
    # 12  2.139952  0.039436  0.954278  ... -1.589688  0.432460 -1.099924
    # 13 -2.157686 -0.533652 -0.268615  ...  0.498217 -0.514481  1.363340
    # 14 -0.430800  0.134520  2.648017  ... -1.266465  1.305028 -0.275019
    # 15  0.279099  0.008691 -1.873946  ...  1.211857 -0.521362  0.240005
    # 16 -2.666528  0.703953  0.286060  ...  0.515530  0.180948  0.861535
    # 17 -0.094860 -0.352535 -0.957357  ...  1.081711 -0.185533  1.677372
    # 18  0.789288 -0.719248  0.863841  ... -0.686396 -0.111201  0.125358
    # 19 -3.028579 -0.707747 -1.181925  ...  1.404488 -1.233304  1.042796
    
    # [20 rows x 10 columns]
    