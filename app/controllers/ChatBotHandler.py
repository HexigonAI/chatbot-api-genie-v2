from flask import request, jsonify
import os.path
import supabase
import json
import openai
import pymysql
import numpy as np
openai.api_key = "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"

def connect():
    return pymysql.connect(host="localhost", user="root", password="", database="embeddings", charset='utf8mb4')

def calculateCosineSimilarity():
    # con = connect()
    # cursor = con.cursor()
    # query = "wind"
    # query2 = "fire"
    query = {
      "users": [
        {
          "id": 1,
          "firstName": "Terry",
          "lastName": "Medhurst",
          "maidenName": "Smitham",
          "age": 50,
          "gender": "male",
          "email": "atuny0@sohu.com",
          "phone": "+63 791 675 8914",
          "username": "atuny0",
          "password": "9uQFF1Lh",
          "birthDate": "2000-12-25",
          "image": "https://robohash.org/hicveldicta.png?size=50x50&set=set1",
          "bloodGroup": "A−",
          "height": 189,
          "weight": 75.4,
          "eyeColor": "Green",
          "hair": {
            "color": "Black",
            "type": "Strands"
          },
          "domain": "slashdot.org",
          "ip": "117.29.86.254",
          "address": {
            "address": "1745 T Street Southeast",
            "city": "Washington",
            "coordinates": {
              "lat": 38.867033,
              "lng": -76.979235
            },
            "postalCode": "20020",
            "state": "DC"
          },
          "macAddress": "13:69:BA:56:A3:74",
          "university": "Capitol University",
          "bank": {
            "cardExpire": "06/22",
            "cardNumber": "50380955204220685",
            "cardType": "maestro",
            "currency": "Peso",
            "iban": "NO17 0695 2754 967"
          },
          "company": {
            "address": {
              "address": "629 Debbie Drive",
              "city": "Nashville",
              "coordinates": {
                "lat": 36.208114,
                "lng": -86.58621199999999
              },
              "postalCode": "37076",
              "state": "TN"
            },
            "department": "Marketing",
            "name": "Blanda-O'Keefe",
            "title": "Help Desk Operator"
          },
          "ein": "20-9487066",
          "ssn": "661-64-2976",
          "userAgent": "Mozilla/5.0 ..."
        },
      ],
      "total": 100,
      "skip": 0,
      "limit": 30
    }

    query2 = "what is the gender of Edwin F"

    embedding = openai.Embedding.create(input = [json.dumps(query),query2], model="text-embedding-ada-002")['data']

    embeddingNumpy1 = np.array(embedding[0]['embedding'])
    embeddingNumpy2 = np.array(embedding[1]['embedding'])

    dot_product = np.dot(embeddingNumpy1, embeddingNumpy2)

    magnitude_embedding1 = np.linalg.norm(embeddingNumpy1)
    magnitude_embedding2 = np.linalg.norm(embeddingNumpy2)

    cosine_similarity = dot_product / (magnitude_embedding1 * magnitude_embedding2)

    print("cosine similiary ",cosine_similarity)


    # cursor.execute('INSERT INTO `documents` (id,content,embedding) VALUES (NULL, %s, %s)', (json.dumps(query), str(embedding)))
    # con.commit()
    # con.close()

    return jsonify({"status": "true"})
    # return jsonify({"status": "true", "content": "Success Insert Embedding To Supabase"})

def chat():
    query = request.json['query']
    embedding = openai.Embedding.create(input = [query], model="text-embedding-ada-002")['data'][0]['embedding']

    # data = supabase.rpc('match_documents', {
    #     'query_embedding': embedding,
    #     'match_threshold': 0.78,
    #     'match_count': 10,
    # }).execute().data


    # Inisialisasi variabel
    contextText = ''
    tokenCount = 0

    # Menggabungkan dokumen yang cocok
    for i in range(len(data)):
        content = data[i]['content']

        contextText += f"{content.strip()}\n---\n"

    prompt = "\nContext sections: "+contextText+" \n Question: "+query+" \n Answer: "
    print("Prompt : ",prompt)
    completions = openai.Completion.create(
                engine="text-davinci-003",
                prompt=query,
                max_tokens=512,
                n=1,
                stop=None,
                temperature=0.7,  
            )
    message = completions.choices[0].text
    print(message)
        
    return jsonify({"status": "true", "content": message})