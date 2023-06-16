from flask import request, jsonify
import os.path
import supabase
import json
import openai
openai.api_key = "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"
supabase_url = 'https://fjscgxbfprecqhglqrhl.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZqc2NneGJmcHJlY3FoZ2xxcmhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzk0MTcxOTEsImV4cCI6MTk5NDk5MzE5MX0.njMdryE-lJnhk_BIegCDnDE-JnPB7BlbNCI5Tn9lkj8'
supabase = supabase.create_client(supabase_url, supabase_key)

# search through the reviews for a specific product

def createEmbedding():
    query = request.json['query']
    embedding = openai.Embedding.create(input = [query], model="text-embedding-ada-002")['data'][0]['embedding']

    response = supabase.table("documents").insert({
        content: query,
        embedding
    })

    return jsonify({"status": "true", "content": "Success Insert Embedding To Supabase"})

def chat():
    query = request.json['query']
    embedding = openai.Embedding.create(input = [query], model="text-embedding-ada-002")['data'][0]['embedding']

    data = supabase.rpc('match_documents', {
        'query_embedding': embedding,
        'match_threshold': 0.78,
        'match_count': 10,
    }).execute().data


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