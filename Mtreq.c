/* apply trace equalisation to a seismic data.*/
/*
   Copyright (C) 2018 Yi Lin 
     
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
               
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
                    
   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

   Email: linyihanchuan@gmail.com
   Reference:
     https://wiki.seg.org/wiki/Relative_trace_balancing

   Example:
   
        sftreq <in.rsf > out.rsf
        input:
            in.rsf (n1: time axis; n2: trace axis)
            out.rsf (n1: time axis; n2: trace axis)

*/

#include <rsf.h>

int main(int argc, char* argv[])
{
    int verbose;
    int nt, nx;
    int ix, it;
    float tmp;
    float** in_traces;
    float** out_traces;

    sf_file in=NULL, out=NULL;

    /* open the input, output, and delay files */
    sf_init (argc,argv);
    in = sf_input ("in");
    out = sf_output ("out");
      
    if(!sf_getint("verbose",&verbose)) verbose=1;
    /* 0 terse, 1 informative, 2 chatty, 3 debug */
  
    /* get the size of the input traces */
    sf_histint(in,"n1",&nt);
    sf_histint(in,"n2",&nx);

    /* allocate space for the input traces and output traces */ 
    in_traces = sf_floatalloc2(nt,nx);
    out_traces = sf_floatalloc2(nt,nx);

  
    /* read the input traces */ 
    sf_floatread(&(in_traces[0][0]),nt*nx,in);

    for(ix=0; ix<nx; ix++){
        tmp = 0;
        for(it=0; it<nt; it++){
            tmp += in_traces[ix][it]*in_traces[ix][it];
        }
        tmp = sqrt(tmp/nt);
        for(it=0; it<nt; it++){
            out_traces[ix][it] = in_traces[ix][it]/tmp;
        }
        
    }

    /* write the traces back out */
    sf_floatwrite(&(out_traces[0][0]),nt*nx,out);
    
    free(*out_traces);
    free(out_traces);
    free(*in_traces);
    free(in_traces);

    exit(0);
}