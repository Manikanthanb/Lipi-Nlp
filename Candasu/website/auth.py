from logging import exception
from exceptiongroup import catch
from flask import Blueprint ,render_template,request,redirect,url_for,flash,session
import tensorflow as tf
from  keras.models import load_model,model_from_json

import copy
import math
from . import dict
# from dict import find
from sys import exit
import numpy as np 
from functools import wraps
from datetime import datetime
import pickle
# from tensorflow.keras import load_model
import tensorflow 
# from tensorflow import * 
# from tensorflow.keras import * 
# from p import Module1,Module2,Module3,Module2_instance,Module1_instance,Module3_instance 
import p
aut=Blueprint("auth",__name__)

@aut.route('/')
def home():
 return render_template('home.html')

@aut.route('/chandasu',methods=['GET','POST'])
def chandasu():
    try:
        if request.method == 'POST':
            print("hello")
            inp=request.form.get('cpoem')
            print(inp)
            # ex=open("ex1.txt",'w', encoding="utf8")
            with open('ex1.txt', 'w',encoding='utf-8') as ex:
                print("ex opened")
                for line in inp.split('\n'):
                    ex.write(line )
                    print(line)
            print("ex  opened for reading")
            f = open("ex1.txt","r",encoding="utf-8")
            print("after ex")
            f1=open("Chandassu.txt",'w', encoding="utf8")
            f1.close()
            f2=open("laghu_Guru.txt",'w', encoding="utf8")
            f2.close()
            print("after files")
            Module1_instance=p.Module1()
            akshara_list=Module1_instance.line_partition(f)
            Module2_instance=p.Module2()
            lm,lg_list=Module2_instance.laghu_guru(copy.deepcopy(akshara_list))
            Module3_instance=p.Module3()
            Module3_instance.chandassu(copy.deepcopy(akshara_list),copy.deepcopy(lg_list),copy.deepcopy(lm))
            with open('Chandassu.txt', 'r',encoding='utf8') as f5:
                content = f5.read()
                return render_template("chandasu.html",content=content)    

        return render_template("chandasu.html")    
    except Exception as e:
        flash(f"Something went wrong ,please logout and try again {e}",category="error")
        return render_template("home.html")    
    
def predict_output_for_sentence(sentence):
    model, tokenizer = models()
    max_seq_length = 8
    print(type(sentence))
    # print("harsha")
    poem=sentence.strip().split()
    i=0
    while(i<len(poem)):
        print(poem[i],len(poem[i]))
        if(len(poem[i])<=2 and i+1<len(poem)):
            poem[i+1]=poem[i]+poem[i+1]
            poem.remove(poem[i])
        else:
            i+=1
    predicted_words = []
    for ik in poem:
        # print(ik)
        ans=''
    # Preprocess the input sentence
        input_sequence = tokenizer.texts_to_sequences([ik])
        # print(input_sequence)
        input_sequence_padded = tf.keras.preprocessing.sequence.pad_sequences(input_sequence, maxlen=max_seq_length, padding='post')

        # Predict for each word in the input sentence
        predicted_output_sequence = model.predict(input_sequence_padded)
        predicted_word_indices = np.argmax(predicted_output_sequence, axis=-1)
        # print("predicted indices")
        # print(predicted_word_indices)
        # Convert predicted word indices to words
        # predicted_words = [tokenizer.sequences_to_texts([[word_index]])[0].strip() for word_index in predicted_word_indices[0]]
        
        # predicted_word = tokenizer.sequences_to_texts([[predicted_word_indices[0][0]]])[0].strip()
        for word_index in predicted_word_indices[0]:
            # Get the predicted word for each index
            predicted_word = tokenizer.sequences_to_texts([[word_index]])[0].strip()
            ans+=" "+predicted_word
        # print("predicted word")
        # print(ans)
        if(sum(predicted_word_indices[0])==0):
            predicted_words.append(ik)
        else:
            predicted_words.append(ans) 

        # Combine the predicted words into a single string
    # print("predicted words")
    # print(predicted_words)
    predicted_poem = ' '.join(predicted_words)
   

    return predicted_poem


def get_word_meaning(word):
    # Implement your logic to get the meaning of the word from your meanings dictionary
    # This is a placeholder, you should replace it with your actual logic
    hash_key = word
    with open('hash_table.pkl', 'rb') as f:
                meanings = pickle.load(f)

                # print("Meanings")
                # print(meanings)
                try:
                    # print('fetching meaning')
                    # print(hash_key)
                    # print(meanings[hash_key])
                    if meanings[hash_key]=='' or meanings[hash_key]==None:
                        return word
                    return meanings[hash_key]
                except Exception as e:
                    # print(e)
                    pass
def models():
    with open('tokenizer.json') as f:
        tokenizer =tf.keras.preprocessing.text.tokenizer_from_json(f.read())

    # Model reconstruction from JSON file
    with open('model_architecture.json', 'r') as f:
        model = model_from_json(f.read())

    # Load weights into the new model
    model.load_weights('model_weights.h5')

    return model, tokenizer
 
@aut.route('/translation', methods=['GET', 'POST'])
def translation():
    try:
        if request.method == 'POST':
            print("translation")
            inp2 = request.form.get('tpoem')
            processed_words = predict_output_for_sentence(inp2)
            processed_words=processed_words.split()
            print(processed_words[0])
            # inp3=dict.find(processed_words[0])
            # if inp3==False:
            #     inp3=inp2
            inp3=predict_output_for_sentence(inp2)
            print(type(inp3))
            # inp2=str(inp3)
            word_list = inp2.split()
            print('inp2')
            num_lines = 4
            part_length = (len(word_list) + num_lines - 1) // num_lines

            # Split the word_list into lines
            lines = [" ".join(word_list[i * part_length: (i + 1) * part_length]) for i in range(num_lines)]

            # Write the lines to a text file
            with open("finalout.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(lines))

            # Read the processed poem from the file
            with open("finalout.txt", "r", encoding="utf-8") as file:
                inp2 = file.read()
                
            word_list = inp3.split()
            print('inp2')
            num_lines = 4
            part_length = (len(word_list) + num_lines - 1) // num_lines

            # Split the word_list into lines
            lines = [" ".join(word_list[i * part_length: (i + 1) * part_length]) for i in range(num_lines)]

            # Write the lines to a text file
            with open("finalout1.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(lines))

            # Read the processed poem from the file
            with open("finalout1.txt", "r", encoding="utf-8") as file:
                inp3 = file.read()

            

            # Process each word and get the meaning
            processed_words=inp3.split()
            final = []
            for word in processed_words:
                meaning = get_word_meaning(word)
                if meaning is None:
                    final.append(word)
                final.append(meaning)

            # Join the processed words back into a poem
            processed_poem = ' '.join(filter(None, final))

            # Split the processed poem into four lines
            word_list = processed_poem.split()
            part_length = len(word_list) // 4
            lines = [
                " ".join(word_list[i * part_length: (i + 1) * part_length]) for i in range(4)
            ]

            # Write the lines to a text file
            with open("finalout2.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(lines))

            # Read the processed poem from the file
            with open("finalout2.txt", "r", encoding="utf-8") as file:
                processed_poem = file.read()

            # Pass the data to the template
            content = {
                "original_poem": inp2,
                "converted_poem": processed_poem,
                "translation_details": inp3,  # Replace with actual details
            }

            return render_template('translation.html', content=content)

        return render_template('translation.html')

    except Exception as e:
        flash(f"Something went wrong {e}", category="error")
        return render_template("home.html")