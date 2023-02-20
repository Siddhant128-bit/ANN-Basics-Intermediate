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
        #model.add(layers.Dense(units=128*2,activation='relu'))
        #model.add(layers.Dense(units=128*3,activation='relu'))

        #model.add(layers.Dense(units=128*4,activation='relu'))
        #model.add(layers.Dense(units=128*3,activation='relu'))
        #model.add(layers.Dense(units=128*2,activation='relu'))
        #model.add(layers.Dense(units=128,activation='relu'))
        model.add(layers.Dense(units=64,activation='relu'))
        model.add(layers.Dense(units=32,activation='relu'))

        model.add(layers.Dense(units=4,activation='softmax'))
        model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),metrics='accuracy')
    
    return model 


def load_data(path):
    data=pd.read_csv('Dataset\\data.csv')
    data=data.dropna()
    data = data.astype(float)
    data.columns=['playerx','playery','powerx','powery','oppx','oppy','a']
    X=np.array(data[['playerx','playery','powerx','powery','oppx','oppy']]).astype(np.float32)
    Y=(np.array(data[['a']]).astype(np.float32)).reshape(-1,1)
    return X,Y

def train_model():
    X,Y=load_data('Dataset\\data.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)

    model=create_model(X_train,y_train)
    
    model.fit(X_train,y_train,epochs=15,validation_data=(X_test,y_test),shuffle=True,batch_size=64)
    model.save('tf_model.h5')

def predict_from_model(prediction_data):
    model=models.load_model('tf_model.h5')
    moves=['left','right','up','down']
    output=np.argmax(model.predict([np.array(prediction_data)][0]))
    print(moves[output])
    return output

if __name__=='__main__':
    train_model()
    print(predict_from_model([[150,155,8,177,151.0,86.0]]))
