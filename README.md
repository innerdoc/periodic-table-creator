# Periodic Table Creator

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/innerdoc/periodic-table-creator/main/periodic-table-creator/periodic_table_creator.py)

## About
This Periodic Table Generator started with the idea for a blog about a [Periodic Table of Natural Language Processing Tasks](https://medium.com/innerdoc). With the help of Streamlit and inspired by this Bokeh [gallery example](https://docs.bokeh.org/en/latest/docs/gallery/periodic.html) it became a dynamic creator that can be customized to your Periodic Table!


## The result
[Open the demo app!](https://share.streamlit.io/innerdoc/periodic-table-creator/main/periodic-table-creator/periodic_table_creator.py)

Below an example of a customized Periodic Table. In this case: for Natural Language Processing Tasks!

![alt text](periodic-table-generator-nlp-example.png "An example of a customized Periodic Table for Natural Language Processing Tasks!")


## Install and run
```
pip install -r requirements.txt
cd periodic-table-creator
streamlit run periodic_table_creator.py
```


## Load your own content
Create your own Periodic Table by loading your content via your own CSV file. Look at the "Edit CSV text" section for an example of the CSV format:
- header column names: atomicnumber;group;period;symbol;elementname;groupname;color
- semicolon or comma seperated
- csv extension
- utf-8 encoding

![alt text](periodic-table-generator-load-content.png "Load your own content by creating a CSV file!")


## Customize the figure
Customize your own content in the sidebar. You can edit the Title, Font, Color, Scaling and Trademark.

![alt text](periodic-table-generator-customize-content.png "Customize your own content in the sidebar!")