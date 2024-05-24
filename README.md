# Scrapping and NER

This project consist of two parts and files:
1. Crawler: we crawl a site and store in projectData.json
2. NER (processData.py): we do a ner clasification via linking with wikipedia and store in results.csv

## Installation

Before running the script, ensure that you have the necessary Python libraries installed. You can install them using pip:

```bash
pip install requests
pip install BeautifulSoup
pip install nltk wikipedia
```

## Part 1: Web Crawling and Data Extraction from Collins Website

### Introduction

Collins is a renowned creative agency known for its innovative design solutions and impactful branding strategies. With a diverse portfolio of projects spanning various industries, Collins has established itself as a leader in the field of design and branding.

This project aims to extract all the projects that it has ever made and their most important data about them.

### Web Resource Description

- **Main URL**: [https://www.wearecollins.com](https://www.wearecollins.com)
- **Extracted Information**: 
  - Project Title
  - Team Members
  - Project Information
  - Date Modified
  - Date Published
  - Related Project URLs

### Possible Issues with Crawling

- **Policies**: Ensure compliance with robots.txt to avoid being blocked by the website.
- **Rate Limiting**: Implement a crawl interval to prevent overwhelming the server and getting banned.
- **Depth Limit**: Set a crawl depth limit to prevent infinite crawling loops and excessive resource consumption.
- **User-Agent String**: Use a legitimate User-Agent string to identify the crawler and comply with the website's policies.
- **Deciding how to store the data**: I chose JSON format because it is clearer for reading and showing the type of data I'm extracting.

### Design of the Extraction Task

- **Inputs**: Seed URL, crawl interval, crawl depth limit, user-agent string.
- **Outputs**: Extracted data stored in a structured format (JSON).

### Implementation

I decided to use Python as the main language with different libraries:

- **BeautifulSoup**: for extracting data from the HTML.
- **json**: to transform the data into JSON format to write them into a JSON file.
- **time**: to set the interval between HTTPS petitions to avoid overflow of the website.
- **requests**: to make HTTPS requests of the website.

I didn't decide to use Scrapy for this case because some modifications were needed for this website. Especially identify the type of website, although both of them had really similar domains. In other cases, Scrapy is highly recommended because of its ease of use. But I found making a crawler by myself more useful for the future as I can personalize them easily for a specific client.

### Function definitions:

- **addToJsonFile(res)**: This function takes a dictionary `res` and writes its contents into a JSON file. It first converts the dictionary into a JSON string with indentation (`json.dumps(res, indent=4)`), then writes this string into a file named 'projectData.json' located at '01/results/'. The file is opened in write mode ('w') using a `with` statement to ensure proper file handling.

- **get_dates(soup)**: This function takes a BeautifulSoup object `soup` (representing an HTML page) as input. It finds a `<script>` tag with the attribute type set to 'application/ld+json'. It then extracts the JSON data contained within this tag, parses it into a Python dictionary using `json.loads()`, and retrieves the values associated with the keys 'dateModified' and 'datePublished'. Finally, it returns these two date values.

- **get_project_information(soup)**: This function takes a BeautifulSoup object `soup` as input. It finds all `<section>` elements with the class 'work__info__section' and 'col col--right'. It then extracts the text content of each of these elements and concatenates them into a single string, representing the project information. This string is then returned.

- **get_teams(soup)**: This function takes a BeautifulSoup object `soup` as input. It finds a `<div>` element with the class 'work__info__team'. It then finds all `<li>` elements within this `<div>` and extracts the text content of each `<li>` element, representing the teams associated with the project. The function returns a list containing these team names.

- **crawler(seed, crawl_interval, crawl_depth_limit, user_agent)**: This is the main function that performs web crawling. It takes four parameters: seed (the initial URL to start crawling from), crawl_interval (the time delay between consecutive requests), crawl_depth_limit (the maximum depth to crawl), and user-agent (the user-agent string to be used in HTTP requests).

### Extracted Data

The extracted data will be stored in a structured JSON format.

### Comments on Issues During Design/Extraction

- **Identify type of site**: Not all projects under /work/project have the same structure. There were some cases where there was a lot of projects in one project URI and we had to access all of them. My solution was to differentiate if there was an h4 title identifying the project title or not.
- **Finding a static website that satisfied all requirements**: It took a lot of time to find a website to create the crawler from. I did notice that not all websites are made with good quality standards.
- **Rate Limiting**: Adjust the crawl interval to prevent overwhelming the server and getting banned.
- **Depth Limit**: Set an appropriate crawl depth limit to prevent excessive crawling.

### Ideas for Extensions for Future Work

- **Error Handling**: Implement robust error handling to handle unexpected issues during crawling.
- **Database Integration**: Store the extracted data in a database for easier management and analysis.
- **Parallel Processing**: Explore parallel processing techniques to improve the crawling efficiency and speed.

## Part 2: Named Entity Recognition and Wikipedia Summarization Tool

### Overview

This tool extracts project information from JSON data, performs Named Entity Recognition (NER) to identify and extract entities, and then fetches summarized descriptions of these entities from Wikipedia. It leverages Python libraries such as NLTK for NER and the Wikipedia API for fetching summaries.


### Code Description

#### Functions

- **`load_json_data(filepath)`**: Loads JSON data from a specified file.
- **`extract_text(data)`**: Extracts text from the JSON data under the key `project_information`.
- **`perform_ner(text)`**: Performs Named Entity Recognition on the provided text.
- **`extract_entities(chunked_sentences)`**: Extracts named entities from the NER results.
- **`detect_category(sentence)`**: Parses a sentence to determine the most descriptive noun phrase.
- **`wikipedia_summary(entity)`**: Fetches a brief summary for a given entity from Wikipedia.
- **`handle_disambiguation(e)`**: Handles disambiguation errors by attempting to summarize the first suggested option.
- **`try_auto_suggest(entity)`**: Tries fetching a summary using Wikipedia's auto-suggest feature when a PageError is encountered.
- **`get_entity_summaries(entities)`**: Aggregates and prints summaries for a set of entities.

### Main Execution Flow

1. **Load Data**: Reads JSON data from `projectData.json`.
2. **Extract Text**: Pulls relevant textual content from the data.
3. **Named Entity Recognition**: Identifies entities within the text.
4. **Entity Summarization**: Fetches and displays Wikipedia summaries for each unique entity identified in the text.

