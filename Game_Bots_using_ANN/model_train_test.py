import tensorflow as tf
from tensorflow import keras 
from keras import models,layers
from sklearn.model_selection import train_test_split
import pandas as pd 
import numpy as np 

def create_model(X_train,y_train):
    try:
        print('Loaded Model')
        model=models.load_model('tf_model.h5')
    except:
        print('New Model Training Started')
        model=models.Sequential()    
        model.add(layers.Dense(units=32,activation='relu',input_dim=X_train.shape[1])) #1st layer with 6 inputs
        model.add(layers.Dense(units=64,activation='relu'))
        model.add(layers.Dense(units=128,activation='relu'))
        model.add(layers.Dense(units=128*2,activation='relu'))
        model.add(layers.Dense(units=128*3,activation='relu'))

        model.add(layers.Dense(units=128*4,activation='relu'))
        model.add(layers.Dense(units=128*3,activation='relu'))
        model.add(layers.Dense(units=128*2,activation='relu'))
        model.add(layers.Dense(units=128,activation='relu'))
        model.add(layers.Dense(units=64,activation='relu'))
        model.add(layers.Dense(units=32,activation='relu'))

        model.add(layers.Dense(units=y_train.shape[1],activation='sigmoid'))
        model.compile(loss='binary_crossentropy',optimizer='sgd',metrics='accuracy')
    
    return model 


def load_data(path):
    data=pd.read_csv('Dataset\\data.csv')
    data = data.astype(float)
    print(data)
    data.columns=['playerx','playery','powerx','powery','oppx','oppy','l','r','u','d']
    X=np.array(data[['playerx','playery','powerx','powery','oppx','oppy']])
    Y=np.array(data[['l','r','u','d']])
    return X,Y

def train_model():
    X,Y=load_data('Dataset\\data.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)

    model=create_model(X_train,y_train)
    
    model.fit(X_train,y_train,epochs=15,validation_data=(X_test,y_test),shuffle=True,batch_size=16)
    model.save('tf_model.h5')

def predict_from_model(prediction_data):
    model=models.load_model('tf_model.h5')
    print(model.predict([np.array(prediction_data)]))
    output=np.argmax(model.predict([np.array(prediction_data)][0]))
    return output

#train_model()
#print(predict_from_model([[100,170,288,31,207.92,207.92]]))
