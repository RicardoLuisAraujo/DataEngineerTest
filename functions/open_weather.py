"""

This document has one several functions that get the information to parse
the OpenWeatherAPI from an ini config file and creates a ready-to-use pandas dataframe.
The doc has various functions that can be reused later in a similar similar task if needed.
All functions are explained in further detail below.

"""

import configparser
import json
import pandas as pd
import requests

def string_to_list(string: str):
    """
    Turns string into list.
    
    Parameters
    ---------------
    string: string
        The string to be turned into a list
        
    Returns
    ---------------
    li_from_str: list
        The 'string' turned into list by the separator ', '
    """
    
    li_from_str = string.split(", ")
    return li_from_str

def connect_api(url: str, key: str, city: str):
    """
    Connects to API. for a certain city
    
    Parameters
    ---------------
    url: string
        The base url to the API.
        
    key: string
        Key to access the API.
        
    city: string
        City that the user wants to take out the data
        
    Returns
    ---------------
    complete_url: string
        The complete url: includes the base url, key and city 
        to access the API.
    """

    complete_url = url + "appid=" + key + "&q=" + city

    return complete_url

def parsing_ow_json(api_fields: configparser.SectionProxy, json_data: dict, city: str):
    """
    Parses the OpenWeatherAPI and stores the data in a dictionary.

    Parameters
    ---------------
    api_fields: configparser.SectionProxy
        A section from the config file. This section includes all 
        the data that the user wants to take out. Works similar
        to a dictionary.

    json_data: dict
        Dictionary with all the data from the city the user chose.
        The data is presented in a dicationary.

    city: string
        City that the user wants to take out the data

    Returns
    ---------------
    cities_dict: dict
        Dictionary with all the data from the city and ready to be
        turned/added into a Pandas dataframe.
    """
    # Creating an empty dict that will be populated with a certain city's data. 
    cities_dict = {}
    cities_dict['city'] = city

    # For each key value pair in the api_fields section,
    # turn the values into list.
    for key, value in api_fields.items():
                fields = string_to_list(value)
            
            # Iterate over each value in values
                for field in fields:
                    
                    # Get data from the API JSON and storing it in the dict
                    if key == 'other':
                        cities_dict[field] = json_data[field]
                    else:
                        if type(json_data[key]) == list:
                            cities_dict[key + "_" + field] = json_data[key][0][field]
                        else:
                            cities_dict[key + "_" + field] = json_data[key][field]
                            
    return cities_dict
                        
            
def get_weather(url: str, api_key: str, cities: list, api_fields: configparser.SectionProxy):
    
    """
    Makes the connection to the API for each city and makes the
    request to the OpenWeather API. It also aggregates all the dicts
    in a single dataframe ready be used.

    Parameters
    ---------------
    url: string
        The base url to the API.

    api_key: string
        Key to access the API.
        
    api_fields: configparser.SectionProxy
        A section from the config file. This section includes all 
        the data that the user wants to take out.

    cities: list
        A list of cities that the user wants to take out the data

    Returns
    ---------------
    weather_df: pandas.core.frame.DataFrame
        Pandas Dataframe with all the data from the city and ready to be
        used.
    """
    
    # Creating a new empty dataframe
    weather_df = pd.DataFrame()
    
    for city_name in cities:

        # Completing the url to connect to the API
        complete_url = connect_api(url, api_key, city_name)
        
        # get method of requests module
        # return response object
        response = requests.get(complete_url)

        # json method of response object 
        # convert json format data into
        # python format data
        x = response.json()
        
        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is different to
        # "404", means city is found otherwise,
        # city is not found
        if x["cod"] != "404":
            
            # Getting the information from the API into a dict
            cities_dict = parsing_ow_json(api_fields, x, city_name)

            # Appeding to the dataframe the dictionary with the data from one city 
            weather_df = weather_df.append(cities_dict, ignore_index=True)
        else:
            print(" City Not Found ")
            
    return weather_df  
