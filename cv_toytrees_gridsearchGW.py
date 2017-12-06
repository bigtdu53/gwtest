import numpy as np
import os,sys
module_path = os.path.abspath(os.path.join('/Users/vayer/Documents/OT/Python/GW_tests/'))
if module_path not in sys.path:
    sys.path.append(module_path)
from graph import *
import copy
import NN,time
from sklearn.model_selection import GridSearchCV

nTree=100
depth=3
c=20
d=30
dataset=build_binary_uniform_dataset(nTree1=nTree,nTree2=nTree,maxdepth=depth,c=c,d=d)
X,y=zip(*dataset)
dir_path='./'
result_file='result_toytrees_GW.csv'
text_file = open(os.path.join(dir_path, result_file), 'w')

n_splits=5
start_time = time.time()

print('CV Nb_splits : ', n_splits, file=text_file)
print('Number of tree : ', nTree, file=text_file)
print('Max_depth :',depth,file=text_file)
print('c,d :', (c,d),file=text_file)


tuned_parameters = [{'epsilon':list(np.linspace(10,15,1)),
                     ,'method':['weighted_shortest_path']
                     ,'normalize_distance':[False,True]}]

print('Tuned_parameters : ',tuned_parameters,file=text_file) 

gw_1NN=NN.Tree_GW_1NN_Classifier(parallel=True)
clf = GridSearchCV(gw_1NN, tuned_parameters, cv=n_splits,verbose=1,n_jobs=3)
clf.fit(np.array(X).reshape(-1,1),np.array(y))


print('--------------------------', file=text_file)
print('--------------------------', file=text_file)
print('', file=text_file)
print("Best parameters set found on development set:", file=text_file)
print('', file=text_file)
print(clf.best_params_, file=text_file)
print('', file=text_file)
print('--------------------------', file=text_file)
print('--------------------------', file=text_file)
print("Grid scores on development set:", file=text_file)
print('', file=text_file)
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
        % (mean, std * 2, params), file=text_file)
print('', file=text_file)


end_time = time.time()
print('--------------------------', file=text_file)
print('--------------------------', file=text_file)
print('All Time :', end_time-start_time, file=text_file)