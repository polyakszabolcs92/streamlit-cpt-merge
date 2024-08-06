import numpy as np
import pandas as pd
import plotly.graph_objects as go


def SBT(qc, Rf):
    I = ((3.47 - np.log10(qc/0.1))**2 + (np.log10(Rf) + 1.22)**2) **0.5
    return I


def plotly_lineplot(dfs, x_data, x_max, df_cptnames, d_width, d_height):

    # Diagram létrehozása
    fig = go.Figure()

    # Diagram mérete, margók
    fig.update_layout(template= 'plotly',
                      autosize= False, 
                      width= d_width, 
                      height= d_height,
                      margin= dict(l=70, r=20, t=60, b=20),
                      plot_bgcolor= "white")

    # CPT adatsorok plottolása
    for i in range(len(dfs)):
        xi = dfs[i][x_data]
        yi = dfs[i]['z']
        fig.add_trace(go.Scatter(x = xi, y = yi, mode='lines', name = df_cptnames.iloc[i][0]))

    # X tengely beállításai
    fig.update_layout(xaxis=dict(side = "top"))    # X tengely felül

    if x_data == 'qc':
        x_title = "<b> q<sub>c</sub> [MPa] <b>"
        mult_X_major = 5    
        mult_X_minor = 1    
        range_x = [0, x_max]
    elif x_data == 'Rf':
        x_title = "<b> R<sub>f</sub> [%] <b>"
        mult_X_major = 0.5    
        mult_X_minor = 0.25  
        range_x = [0, x_max]
    else:
        x_title = "<b> SBT Index [-] <b>"
        mult_X_major = 0.5    
        mult_X_minor = 0.1  
        range_x = [0, x_max]

    mult_Y_major = 1.0
    mult_Y_minor = 0.5

    # X axis properties
    fig.update_xaxes(title = dict(text= x_title,
                                  font = dict(color = "black",
                                              family='Arial',
                                              size=16),
                                  standoff = 10),
                     dtick = mult_X_major,    # főosztás távolsága
                     ticks='outside',
                     tickcolor = 'black',
                     tickfont = dict(color = "black",
                                     family='Arial',
                                     size = 12),
                     showline=True, 
                     linecolor='black',
                     showgrid=True,
                     gridcolor='lightgrey',
                     minor = dict(dtick = mult_X_minor,
                                  gridcolor = "lightgrey",
                                  griddash = "1px",
                                  ticks = "outside"),
                     maxallowed = x_max,
                     range = range_x            
                    )

    # Y axis properties
    fig.update_yaxes(title = dict(text="<b> z [mBf] <b>",
                                  font = dict(color = "black",
                                              family='Arial',
                                              size=16),
                                  standoff = 10),
                    dtick = mult_Y_major,    # főosztás távolsága
                    ticks='outside',
                    tickcolor = 'black',
                    tickfont = dict(color = "black",
                                    family='Arial',
                                    size = 12),
                    showline=True, 
                    linecolor='black',
                    gridcolor='lightgrey',
                    minor = dict(dtick = mult_Y_minor,
                                gridcolor = "lightgrey",
                                griddash = "1px",
                                ticks = "outside")
                    )

    # Legend properties
    fig.update_layout(legend = dict(bordercolor = "grey",
                                    borderwidth = 1,
                                    font = dict(color = "black",
                                                family = "Arial",
                                                size = 11)))
    

    if x_data == 'SBT':
        opacity_SBT = 0.10
        ann_position = "bottom left"


        fig.add_vline(1.3, line_dash = "dot", line_width = 1)
        fig.add_vrect(x0=0, x1=1.3, 
                      annotation_text="Dense sand to gravelly sand", 
                      annotation_position=ann_position,
                      annotation_textangle= -90,
                      annotation= dict(font_size=8, font_family="Arial"),
                      fillcolor= "darkorange", 
                      opacity=opacity_SBT, line_width=0)
        fig.add_vline(2.05, line_dash = "dot", line_width = 1)
        fig.add_vrect(x0=1.3, x1=2.05, 
                      annotation_text="Sands: clean sands to silty sands", 
                      annotation_position=ann_position,
                      annotation_textangle= -90,
                      annotation= dict(font_size=8, font_family="Arial"),
                      fillcolor= "gold", 
                      opacity=opacity_SBT, line_width=0)
        fig.add_vline(2.60, line_dash = "dashdot", line_width = 2)
        fig.add_vrect(x0=2.05, x1=2.60, 
                      annotation_text="Sand mixtures: silty sand to sandy silt", 
                      annotation_position=ann_position,
                      annotation_textangle= -90,
                      annotation= dict(font_size=8, font_family="Arial"),
                      fillcolor= "limegreen", 
                      opacity=opacity_SBT, line_width=0)
        fig.add_vline(2.95, line_dash = "dot", line_width = 1)
        fig.add_vrect(x0=2.60, x1=2.95, 
                      annotation_text="Silt mixtures: clayey silt & silty clay", 
                      annotation_position=ann_position,
                      annotation_textangle= -90,
                      annotation= dict(font_size=8, font_family="Arial"),
                      fillcolor= "seagreen", 
                      opacity=opacity_SBT, line_width=0)
        fig.add_vline(3.6, line_dash = "dot", line_width = 1)
        fig.add_vrect(x0=2.95, x1=3.6, 
                      annotation_text="Clays: clay to silty clay", 
                      annotation_position=ann_position,
                      annotation_textangle= -90,
                      annotation= dict(font_size=8, font_family="Arial"),
                      fillcolor= "royalblue", 
                      opacity=opacity_SBT, line_width=0)
        fig.add_vrect(x0=3.6, x1=x_max, 
                      annotation_text="Clay - organic soil", 
                      annotation_position=ann_position,
                      annotation_textangle= -90,
                      annotation= dict(font_size=8, font_family="Arial"),
                      fillcolor= "navy", 
                      opacity=opacity_SBT, line_width=0)

    return fig