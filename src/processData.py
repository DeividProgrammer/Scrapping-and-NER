import csv
import json
import nltk
import wikipedia
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

# Ensure necessary NLTK resources are downloaded
'''
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
'''

def load_json_data(filepath):
    """Loads JSON data from a file."""
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


def extract_text(data):
    """Extracts project information text from the loaded JSON data."""
    return [project["project_information"] for project in data]


def perform_ner(text):
    """Performs Named Entity Recognition on the provided text."""
    sentences = sent_tokenize(text)
    tokenized_sentences = [word_tokenize(sent) for sent in sentences]
    pos_tagged_sentences = [pos_tag(sent) for sent in tokenized_sentences]
    chunked_sentences = [ne_chunk(tagged) for tagged in pos_tagged_sentences]
    return chunked_sentences


def extract_entities(chunked_sentences):
    """Extracts and returns entities from chunked sentences."""
    entities = []
    for sent in chunked_sentences:
        for chunk in sent:
            if hasattr(chunk, 'label') and chunk.label():
                entities.append(' '.join(c[0] for c in chunk))
    return entities

def detect_category(sentence):
    grammar ="NP: {<DT>?<JJ>?<VBN>*<NN>?<NN>}"
    cp = nltk.RegexpParser(grammar)

    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    cs = cp.parse(tagged)

    descriptive_phrase = ""
    for subtree in cs.subtrees(filter=lambda x: x.label() == 'NP'):
        np_words = [word for word, tag in subtree.leaves()]
        noun_phrase = ' '.join(np_words)
        descriptive_phrase += noun_phrase + " "

    descriptive_phrase = descriptive_phrase.strip()

    return "Thing" if descriptive_phrase == '' else descriptive_phrase

def wikipedia_summary(entity):
    try:
        summary = wikipedia.summary(entity, sentences=1, auto_suggest=False)
        return detect_category(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        return handle_disambiguation(e)
    except wikipedia.exceptions.PageError:
        return try_auto_suggest(entity)
    except Exception as e:
        print(f"Error processing entity '{entity}': {str(e)}")
        return "Thing"
def handle_disambiguation(e):
    if e.options:
        try:
            return wikipedia_summary(e.options[0])  # Try the first suggested option
        except Exception:
            pass
    return "Multiple options"

def try_auto_suggest(entity):
    try:
        summary = wikipedia.summary(entity, sentences=1, auto_suggest=True)
        return detect_category(summary)
    except Exception:
        return "No page found"

def get_entity_summaries(entities):
    """Fetches summaries for each entity from Wikipedia."""
    summaries = {}
    for entity in entities:
        summaries[entity] = wikipedia_summary(entity)
        print(f"Entity: {entity}\nSummary: {summaries[entity]}\n")
    return summaries

def write_csv(csv_filename, entity_summaries):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Escribir la cabecera del CSV
        writer.writerow(["Entity", "Summary"])

        for entity, summary in entity_summaries.items():
            writer.writerow([entity, summary])
def main():
    # Load and process the JSON data
    data = load_json_data('../results/projectData.json')
    texts = extract_text(data)

    # Perform NER and extract entities
    all_entities = []
    for text in texts:
        chunked_sentences = perform_ner(text)
        entities = extract_entities(chunked_sentences)
        all_entities.extend(entities)

    # Get summaries for each unique entity (most important words)
    unique_entities = list(set(all_entities))
    #Get wikipedia information of them.
    entity_summaries = get_entity_summaries(unique_entities)

    write_csv('../results/results.csv', entity_summaries)


if __name__ == '__main__':
    main()
