import sys, os
from flask import Flask, render_template, url_for
import yaml
from yaml import Loader, Dumper
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import glob

app = Flask(__name__, static_url_path='/static')
pages = FlatPages(app)
freezer = Freezer(app)

#load in all the css file names. 
#glob.glob saves all the css file names in a list
css_files_names = glob.glob('static/css/*.css')
for i in range(len(css_files_names)):
    temp = css_files_names[i].find("/")
    css_files_names[i] = css_files_names[i][temp+1:]

#loads in all the yaml file names
all_files_names = glob.glob('static/yaml/*.yaml')
temp_files_names = []

all_files_data = {}

def get_data(name):

    with open(f'static/yaml/{name}_data.yaml', "r") as info:
        temp_data = yaml.load(info, Loader=Loader)

    new_data = []   
    for i in range(len(temp_data)):
        new_data.append(temp_data[i])

    return new_data 

#removes the file path from the yaml file names, and loads in the 
#data from each file and stores it in a dict.
path = "static/yaml/"
for i in range(len(all_files_names)):
    all_files_names[i] = all_files_names[i][len(path): len(all_files_names[i])-10]
    all_files_data[all_files_names[i]] = get_data(all_files_names[i])
    
    if (all_files_names[i].find("each") == -1):
        temp_files_names.append(all_files_names[i])

#render the template for the home web-page
@app.route("/")
def home():
    all_data = get_data('home')
    
    return render_template("general_page.html", title="Home | Open Science Chain", 
                           css_file_names=css_files_names, data=all_data)

# go through all the YAML files and render a static HTML file for them
@app.route("/<string:file_names>/")
def all_pages(file_names):
    more_data = {}
    
    if ("each_" + file_names in all_files_names):
        more_data = all_files_data["each_" + file_names]
    
    if ("about" == file_names):
        more_data = all_files_data["each_events"]

    return render_template("general_page.html", 
                           title=file_names.title() + " | Open Science Chain", 
                           css_file_names=css_files_names, 
                           data=all_files_data[file_names], 
                           more_data=more_data) 

@freezer.register_generator
def all_pages():
    for i in range(0, len(temp_files_names)):
        yield {'file_names': temp_files_names[i]}

if __name__ == "__main__":
    freezer.run(debug=True)