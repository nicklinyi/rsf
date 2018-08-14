#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import m8r
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

 # Copyright (C) 2018 Yi Lin
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.
 # Guides to m8r contained in
# http://www.ahay.org/rsflog/index.php?/archives/
#    173-Extending-Python-interface.html
# http://www.ahay.org/rsflog/index.php?/archives/
#    264-Running-Madagascar-in-an-interactive-console.html

def read_axis(infile, axis=1):
    "Returns n, d, o, u, l of specified axis a from infile of type m8r.Input"
    return (infile.int("n"+str(axis)), infile.float("d"+str(axis)),
            infile.float("o"+str(axis)), infile.string("unit"+str(axis)),
            infile.string("label"+str(axis)))

def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    return figw,figh
    # ax.figure.set_size_inches(figw, figh)

if __name__ == "__main__":
    inp = m8r.Input()
    par = m8r.Par()
    # n1 = inp.int("n1")
    # n2 = inp.int("n2")
    (n1, d1, o1, u1, l1) = read_axis(inp, 1)
    (n2, d2, o2, u2, l2) = read_axis(inp, 2)
    ymax = o1 + d1*(n1-1)
    xmax = o2 + d2*(n2-1)

    data = np.zeros([n2,n1],'f')
    inp.read(data)
    inp.close()

    savefile = par.string("savefile")
    cmap = par.string("cmap", 'gray')
    figx  = par.float("figx", 3.66) # Figure x size in inches, actually 8.46 cm
    figy  = par.float("figy", 4.4)
    dpi   = par.float("dpi", 600) # DPI
    fts   = par.float("fontsize", 8) # Font size
    ylabel = par.string("ylabel")
    xlabel = par.string("xlabel")
    cbar  = par.bool("scalebar", True) # Colorbar
    xticposition = par.string("xticposition","top")
    cbarl = par.string("barlabel") # Colorbar label
    pclip = par.float("pclip", 100)  # Clip amplitude percentage from (0-100)
    # aspect = par.float("aspect", 3) # Font size
    aspect = (xmax-o2)/(ymax-o1)
    # Error/bounds checking
    if pclip < 0 or pclip > 100:
        sf_warning("pclip must be between 0 and 100, using 100")
        pclip = 100.0
    pclip /= 100.0

    # Normalize data
    for i in range(n2):
        data[i,:] /= np.max(np.abs(data[i,:]))

    # print((xmax-o2)/(ymax-o1))
    mpl.rcParams['font.sans-serif'] = "Helvetica"
    # Then, "ALWAYS use sans-serif fonts"
    mpl.rcParams['font.family'] = "sans-serif"
    mpl.rcParams.update({'font.size': fts})

    # fig = plt.figure(figsize=set_size(figx,figy), dpi=dpi)
    fig = plt.figure(figsize=(figx,figy), dpi=dpi)
    # ax = fig.subplots()
    # ax = fig.add_subplot(111, xlim=(o2, xmax), ylim=(ymax, o1))
    ax = fig.add_axes([0.15,0.1, 0.75, 0.75])

    
    img = ax.imshow(np.transpose(data),cmap=cmap,aspect=aspect,
            extent=(o2, xmax, ymax, o1),vmin=-pclip, vmax=pclip)
    plt.xlim(o2, xmax) 
    plt.ylim(ymax, o1)
    ax.set_xlabel(xlabel) 
    ax.set_ylabel(ylabel) 
    ax.xaxis.set_ticks_position(xticposition)
    ax.xaxis.set_label_position('top') 



    # ax.set_xlabel(r'%s (%s)' % (l2, u2)) if u2 else ax.set_xlabel(r'%s' % l2)
    # ax.set_ylabel(r'%s (%s)' % (l1, u1)) if u1 else ax.set_ylabel(r'%s' % l1)

    # set_size(5,10)
    # fig.tight_layout() # lead to white place at the top and bottom of the fig

    if savefile:
        # bbox_inches='tight', remove the extra padding of the output image
        plt.savefig(savefile, dpi=dpi,bbox_inches='tight')
        # plt.savefig(savefile, dpi=dpi)

    if cbar:
        fig2 = plt.figure(figsize=(figx*0.02,figy*0.5), dpi=dpi) 
        axc = fig2.add_axes([0.78,0.15, 0.8, 0.8])
        fig2.add_axes(axc)
        cb = plt.colorbar(img, cax=axc)
        cb.ax.set_ylabel(cbarl) if cbarl else None
        # Align ticklabels in matplotlib colorbar
        # https://stackoverflow.com/questions/19219963/align-ticklabels-in-matplotlib-colorbar
        ticklabs = cb.ax.get_yticklabels()
        cb.ax.set_yticklabels(ticklabs,ha='right')
        cb.ax.yaxis.set_tick_params(pad=25)  # your number may vary
        filename = savefile.split('.')[0]
        # print(filename)
        savebarfile = savefile.replace(filename+'.',filename+'_bar.')
        plt.savefig(savebarfile, dpi=dpi,bbox_inches='tight')
