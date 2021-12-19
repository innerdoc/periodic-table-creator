# based on https://docs.bokeh.org/en/latest/docs/gallery/periodic.html

from io import StringIO
from PIL import Image
import pandas as pd
import streamlit as st
from bokeh.io import output_file, show, save, export_png
from bokeh.plotting import figure
from bokeh.palettes import all_palettes, Turbo256 
from bokeh.transform import dodge, factor_cmap
from bokeh.models import Title
from bokeh.core.properties import value


# must be called as first command
try:
    st.set_page_config(layout="wide")
except:
    st.beta_set_page_config(layout="wide")

try:
    image = Image.open('periodic-table-creator/periodic-table-creator-icon-wide.png')
except:
    image = Image.open('periodic-table-creator-icon-wide.png')


st.sidebar.image(image, use_column_width=True) # width=200 ) #
#st.sidebar.title('Periodic Table Creator')


def try_expander(expander_name, sidebar=True):
    if sidebar:
        try:
            return st.sidebar.expander(expander_name)
        except:
            return st.sidebar.beta_expander(expander_name)
    else:
        try:
            return st.expander(expander_name)
        except:
            return st.beta_expander(expander_name)


# load data
with try_expander('Load Content', False):
    if st.checkbox('Upload your CSV', value=False):
        st.markdown('Upload your own Periodic Table CSV. Follow the example-format of "Edit CSV text" (utf-8 encoding, semicolon seperator, csv file-extension)')
        uploaded_file = st.file_uploader('Upload your CSV file', type=['csv'], accept_multiple_files=False)
    else:
        uploaded_file = None

    if uploaded_file is not None:
        bytes_data = uploaded_file.read().decode("utf-8", "strict") 
    else:
        try:
            with open('periodic-table-creator/periodic_nlp.csv', 'r') as f:
                bytes_data = f.read()
        except:
            with open('periodic_nlp.csv', 'r') as f:
                bytes_data = f.read()
        
    if st.checkbox('Edit CSV text', value=False):
        bytes_data = st.text_area('CSV file', value=bytes_data, height=200, max_chars=100000)

    data = StringIO(bytes_data)
    try:
        df = pd.read_csv(data, sep=';', header=0, encoding='utf-8', keep_default_na=False)
    except:
        df = pd.read_csv(data, sep=',', header=0, encoding='utf-8', keep_default_na=False)
    

    if st.checkbox('Show CSV data', value=False):
        st.table(df)


# edit data
df["elementname"] = df["elementname"].str.replace('\\n', '\n', regex=False)
df["groupname"] = df["groupname"].str.replace('\\n', ' ', regex=False)

df_group = pd.pivot_table(df, values='atomicnumber', index=['group','groupname'], 
    columns=[], aggfunc=pd.Series.nunique).reset_index()
df["color"] = df["color"].fillna('')

periods = [str(x) for x in set(df.period.values.tolist())]
periods_bottomrow = str(len(periods)+1)
periods += [periods_bottomrow]
df["period"] = [periods[x-1] for x in df.period]

groups = [str(x) for x in df_group.group]
groupnames = [str(x) for x in df_group.groupname]


# plot config options in sidebar
with try_expander('Text'):
    plot_title = 'Periodic Table of Natural Language Processing Tasks'
    plot_title = st.text_area('Title', value=plot_title, max_chars=100)

    plot_fonts = ['Helvetica','Times'] #,'New Baskerville','Arial','century gothic','Bodoni MT', 'Lucida Sans Unicode']
    plot_font = st.selectbox('Font', plot_fonts, index=0)

with try_expander('Color'):
    element_color = st.selectbox('Element Color', ['From datafile','Category20','Category20b','Category20c'], index=0)
    title_color = st.color_picker('Title color', '#3B3838')
    text_color = st.color_picker('Element Text color', '#3B3838')
    groupname_color = st.color_picker('Groupname color', '#757171')
    trademark_color = st.color_picker('Trademark color', '#757171')

    if element_color.startswith('Category20'):
        colors = all_palettes[element_color][len(groups)+2]
        df["color"] = df.apply(lambda x: colors[x['group']-1], axis=1)

    df["group"] = df["group"].astype(str)


with try_expander('Scaling'):
    plot_scale = st.slider('OVERALL SCALE', min_value=50, max_value=300, value=100, step=5, format='%d%%')/100.00
    
    plot_width = round(len(groups) * 100 * plot_scale)
    plot_width = st.slider('Plot width', min_value=500, max_value=3000, value=plot_width, step=100, format='%dpx')
    
    plot_height = round(len(periods) * 100 * plot_scale)
    plot_height = st.slider('Plot height', min_value=300, max_value=2000, value=plot_height, step=20, format='%dpx')

    title_size = round(48 * plot_scale)
    title_size = str(st.slider('Title', min_value=5, max_value=72, value=title_size, step=1, format='%dpx')) + 'px'
    
    element_number_size = round(11 * plot_scale)
    element_number_size = str(st.slider('Atomic Number', min_value=5, max_value=72, value=element_number_size, step=1, format='%dpx')) + 'px'
    
    element_symbol_size = round(22 * plot_scale)
    element_symbol_size = str(st.slider('Symbol', min_value=5, max_value=72, value=element_symbol_size, step=1, format='%dpx')) + 'px'
    
    element_name_size = round(11 * plot_scale)
    element_name_size = str(st.slider('Full name', min_value=5, max_value=72, value=element_name_size, step=1, format='%dpx')) + 'px'
    
    group_name_size = round(12 * plot_scale)
    group_name_size = str(st.slider('Group', min_value=5, max_value=72, value=group_name_size, step=1, format='%dpx')) + 'px'
    
    trademark_size = round(12 * plot_scale)
    trademark_size = str(st.slider('Trademark', min_value=5, max_value=72, value=trademark_size, step=1, format='%dpx')) + 'px'

    text_line_height = 0.6 if plot_scale <= 0.9 else 0.7 if plot_scale <=1.1 else 0.8 if plot_scale < 1.5 else 0.9
    text_line_height = st.slider('Text line height', min_value=0.5, max_value=1.5, value=text_line_height, step=0.1, format='%f')

    border_line_width = 2
    border_line_width = st.slider('Border line width', min_value=0, max_value=10, value=border_line_width, step=1, format='%dpx')

with try_expander('Trademark'):
    trademark_tag = st.text_input('Trademark', value="www.innerdoc.com", max_chars=100)
    location_x = str(st.number_input('Group location (x-axis)', min_value=0, max_value=len(groups), value=min(10, len(groups)) ))
    location_y = str(st.number_input('Period location (y-axis)', min_value=0, max_value=len(periods), value=min(2, len(periods)) ))

with try_expander('About'):
    st.markdown('''This Periodic Table Generator is created by [Rob van Zoest](https://www.linkedin.com/in/robvanzoest/). \
The code is available on [github.com/innerdoc](https://github.com/innerdoc/periodic-table-creator). \
It started with the idea for a blog about a [Periodic Table of Natural Language Processing Tasks](https://medium.com/innerdoc). \
With the help of Streamlit and inspired by [Bokeh](https://docs.bokeh.org/en/latest/docs/gallery/periodic.html) \
it became a dynamic creator that can be customized to your Periodic Table!''')




# define figure
TOOLTIPS = """
    <div style="width:300px; padding:10px;background-color: @color;">
        <div>
            <span style="font-size: 36px; font-weight: bold;">@symbol</span>
        </div>
        <div>
            <span style="font-size: 14px; font-weight: bold; ">@groupname</span>
        </div>
        <br>
        <div>
            <span style="font-size: 20px; font-weight: bold; margin-bottom:20px">@atomicnumber - @elementname</span>
        </div>
        <div>
            <span style="font-size: 14px; ">@excerpt</span>
        </div>
        <br>
        <div>
            <span style="font-size: 10px; ">@url</span>
        </div>
        <div>
            <span style="font-size: 10px; ">(@{group}, @{period})</span>
        </div>
"""

p = figure(plot_width=plot_width, plot_height=plot_height,
    x_range=groups,
    y_range=list(reversed(periods)),
    tools="hover",
    toolbar_location="below",
    toolbar_sticky=False,
    tooltips=TOOLTIPS)

r = p.rect("group", "period", 0.94, 0.94, 
    source=df,
    fill_alpha=0.7, 
    color="color", 
    line_width=border_line_width)

text_props = {"source": df, "text_baseline":"middle", "text_color":text_color}

# print number
p.text(x=dodge("group", -0.4, range=p.x_range), 
    y=dodge("period", 0.3, range=p.y_range),
    text="atomicnumber",
    text_align="left",
    text_font=value(plot_font),
    text_font_style="italic",
    text_font_size=element_number_size,
    **text_props)

# print symbol
p.text(x=dodge("group", -0.2, range=p.x_range),
    y=dodge("period", 0.1, range=p.y_range),
    text="symbol",
    text_font=value(plot_font),
    text_font_style="bold",
    text_font_size=element_symbol_size,
    **text_props)

# print element name
p.text(x=dodge("group", 0.0, range=p.x_range),
    y=dodge("period", -0.25, range=p.y_range),
    text="elementname",
    text_align="center",
    text_line_height=text_line_height,
    text_font=value(plot_font),
    text_font_size=element_name_size,
    **text_props)

# print title
p.add_layout(Title(text=plot_title,
    align="center",
    vertical_align="middle",
    text_line_height=1.5,
    text_color=title_color,
    text_font=plot_font,
    text_font_style="bold",
    text_font_size=title_size
    ), "above")

# print groupnames on x-axis
p.text(x=groups,
    y=[periods_bottomrow for x in groups],
    text=[x.replace(u' ', u'\n') for x in groupnames],
    text_align="center", 
    text_line_height=text_line_height,
    text_baseline="middle",
    text_font=value(plot_font),
    text_font_size=group_name_size,
    text_color=groupname_color
    )

# print trademark
p.text(x=[location_x],
    y=[location_y], 
    text=[trademark_tag], 
    text_align="center",
    text_baseline="hanging",
    text_color=trademark_color,
    text_font=value(plot_font),
    text_font_size=trademark_size
    )

p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.visible = False
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.hover.renderers = [r] # only hover element boxes

# Set autohide to true to only show the toolbar when mouse is over plot
p.toolbar.autohide = True

st.bokeh_chart(p)


