import spacy
from intents import intents
nlp = spacy.load("en_core_web_sm")
# doc = nlp("I want to buy clothes from amazon")

# for token in doc:
#     print(
#         token.text,
#         token.lemma_,
#         token.pos_,
#         token.tag_,
#         token.dep_,
#         token.shape_,
#         token.is_alpha,
#         token.is_stop,
#     )


def get_intent(input_text):
    token_obj = nlp(input_text)

    noun = None
    intent = "unknown_intent"
    location = None

   
    for token in token_obj:
        if token.pos_ == "VERB":  
            lemma = token.lemma_.lower()

            
            if lemma in intents:
                intent = intents[lemma]

            
            for key in intents.keys():
                if key in lemma:
                    intent = intents[key]

        if token.pos_ == "NOUN":  
            noun = token.text

        if token.pos_ == "PROPN":  
            location = token.text

    
    for ent in token_obj.ents:
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            location = ent.text

    
    return {"noun": noun, "intent": intent, "location": location}

# Example usage
input_text = "yesterday i was travelling to jaipur and forgot to take my wallet"
result = get_intent(input_text)
print(result)
