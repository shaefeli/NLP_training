from sklearn.linear_model import LogisticRegression

def log_reg(X, y):
    clf = LogisticRegression(random_state=0, max_iter=200).fit(X,y)
    print(clf.score(X,y))
    return clf