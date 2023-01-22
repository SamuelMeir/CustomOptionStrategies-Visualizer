#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

def option_graphs_by_samuel(user):

    oplist = user.replace(' ',"")
    oplist = oplist.replace('"',"")
    oplist = oplist.lower()
    oplist = oplist.split(',')

    for i in range(len(oplist)):
        if 'short' in oplist[i]:
            oplist[i]=oplist[i].replace('short','-')

    for i in range(len(oplist)):
        if 'long' in oplist[i]:
            oplist[i]=oplist[i].replace('long','+')

    for i in range(len(oplist)):
        if 'puts' in oplist[i]:
            oplist[i]=oplist[i].replace('puts', 'p')

    for i in range(len(oplist)):
        if 'calls' in oplist[i]:
            oplist[i]=oplist[i].replace('calls', 'c')

    for i in range(len(oplist)):
        if 'put' in oplist[i]:
            oplist[i]=oplist[i].replace('put', 'p')

    for i in range(len(oplist)):
        if 'call' in oplist[i]:
            oplist[i]=oplist[i].replace('call', 'c')


    pindex=0     #to find index postion of puts
    cindex=0     #to find index position of calls
    n=0          #number of puts or calls with same strike
    dindex=0     #to find index position of $ cost of a put or call
    premium=0    #total premium for multiple options of same type & strike
    strike=0     #strike of a put or call
    net=0        #total cost of entire custom strategy,not needed for this program but nice to have
    k=[]         #list of all strikes
    y=[]         #list of corrosponding total profits to stock prices
    stock = []   #list of stock prices (x-axis)
    sindex=0     #index position of a stock price
    spinex=0     #index position of stock price in relation to put

    floatlist =np.arange(0,1000,0.1)  #create stock prices list from 0-1000 (0.1 ticks)
    for i in floatlist:
        stock.append(round(i,2))      #append to list of stock prices round 2decimal
                                      #because python is very annoying w/ floats
    for i in stock:
        null=0
        y.append(null)                #create a list of 0 profit at every stock price

    for i in oplist:
        if 'p' in i:                #loop and find the letter "p" in user input
            y1=[]                   #empty list for profits of puts w/ same strike
            pindex = i.find('p')    #find index position of letter 'p'
            n = int(i[:pindex])     #value to the left of 'p' is the quantity
            dindex = i.find('$')    #find the index position of $ value
            premium = float(i[dindex+1:])   #value to the right of '$' is the cost
            strike = float(i[pindex+1:dindex]) #value between 'p' and '$' is the strike

            net+= n*premium        #add cost*quantity to net premium (just to have, not needed)
            k.append(strike)       #add strike to list of strikes
            for i in stock:
                spindex=stock.index(i)
                y1.append(n*max(strike-i,0) -n*premium)
                y[spindex]=y[spindex]+y1[spindex]

    for i in oplist:
        if 'c' in i:
            y2=[]
            cindex = i.find('c')
            n = int(i[:cindex])
            dindex = i.find('$')
            premium = float(i[dindex+1:])
            strike = float(i[cindex+1:dindex])

            net+= n*premium
            k.append(strike)
            for i in stock:
                sindex=stock.index(i)
                y2.append(n*max(i-strike,0) -n*premium)
                y[sindex]=y[sindex]+y2[sindex]

    #profits at strikes
    payk=[]
    for i in k:
        kindex=stock.index(i)
        payk.append(y[kindex])


    # MAX and MIN profits
    y=np.array(y)
    low = round(min(y),2)
    high = round(max(y),2)
    print(f'this is the net cost {net}')

    #Breakeven points
    be=[]
    for i,j in enumerate(y):  #because numpy.array can't be indexed - use enumerate
        if -0.01<j<0.01:
            bindex=i
            be.append(stock[bindex])

    #Graph
    plt.clf()
    plt.title("Profit Pattern for Stock Prices 0 to 1000")
    plt.xlabel("Stock Price")
    plt.ylabel("Profit Per 1/100th of a contract")

    plt.plot(stock, y, label='Profit Pattern', c='b', alpha=0.5, linewidth=2.25)
    plt.axhline(0, color='black', linestyle='--', linewidth=2.25)

    plt.fill_between(stock, y, 0, alpha=0.25, where=y>0, facecolor='green', interpolate=True)
    plt.fill_between(stock, y, 0, alpha=0.25, where=y<0, facecolor='red', interpolate=True)

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()

    #Slopes and Inflection Points
    hlimit=0
    llimit=0
    highlimit=0
    lowlimit=0
    dy=[]
    dx =[]
    slope=[]
    for i in np.diff(y):
        dy.append(i)
    for i in np.diff(stock):
        dx.append(i)
    for i in range(len(dx)):
        slope.append(round((dy[i]/dx[i]),0))

    inflection=[]
    for i in range(1, len(slope)):
        if slope[i]!=slope[i-1]:
            inflection.append(y[i])

    if len(inflection)!=0:
        hlimit =max(inflection)
        llimit=min(inflection)
    else:
        hlimit=max(max(y),min(y))
        llimit=min(max(y),min(y))
    print(f'INFLECTIONS: {inflection}')
    print(f'llimit/hilimit {llimit}/{hlimit}')
    print(f'inflection llimit/hlimit {llimit}/{hlimit}')
    hindex=0
    lindex=0
    for i,j in enumerate(y): #finding index positions of highest and lowest inflection points
        if j==hlimit:
            hindex=i

    for i,j in enumerate(y):
        if j==llimit:
            lindex=i

    #finding optimal x-limits for best presentation of graph

    right=0
    left=0
    rightscale = 1.25
    leftscale =1/rightscale
    if len(k)>1:
        diff = max(k)-min(k)
        right = max(k)*rightscale

        if diff==0:
            left=min(k)*leftscale
        else:
            left=max(min(k)-(right-max(k)),0)

    elif len(k)==1 and y[hindex]<0:
        if y[0]<0:                             #for single long call
            right=k[0]*1.5
            left=k[0]*0.75
        else:                                  #for single long put
            right=k[0]*1.1
            left=k[0]*0.5

    elif len(k)==1 and y[hindex]>0:
        if y[0]>0:                         #for single short call
            right=k[0]*1.5
            left=k[0]*0.75
        else:
            right=k[0]*1.1     #for single short put
            left=k[0]*0.5

    leftindex=stock.index(round(left,0))
    rightindex=stock.index(round(right,0))

    if y[leftindex]<5:
        left=left*0.75
    if y[rightindex]<5:
        right=right*1.25

    plt.xlim(left, right)
    print(f'these are the xlimits left/right: {left}/{right}')

    #finding optimal y-limits for best presentation of graph
    if max(k)>150:
        extra = 50
    else:
        extra=2

    if len(k)>1 and y[hindex]!=y[lindex]:  #multiple strikes w/ different profits at infliction
        if len(inflection)!=0:
            highlimit=hlimit+4
            lowlimit=llimit-4

        if y[hindex]<5:
            highlimit=highlimit*1.5

        elif len(inflection)==0 and y[leftindex]<0:     #synthetic long stock
            lowlimit=y[leftindex]-2
            highlimit= -1*y[leftindex]+2

        elif len(inflection)==0 and y[leftindex]>0:     #synthetic short stock
            lowlimit=-1*y[leftindex]-2
            highlimit= y[leftindex]+2

    elif len(k)>1 and y[hindex]==y[lindex]:  #multiple strikes w/ same profit at infliction
        if len(inflection)==0 and hlimit==llimit and hlimit>0:     #flat line above zero
            highlimit=hlimit+2
            lowimit = llimit-llimit-2

        elif len(inflection)==0 and hlimit==llimit and hlimit<0:  #flat line below zero
            highlimit=hlimit-hlimit+2
            lowlimit = hlimit-2


        elif y[leftindex]>0 and hlimit==llimit and hlimit<0:  #long straddle/strangle, edge>0
            highlimit=y[leftindex]+2
            lowlimit= llimit-2

        elif y[leftindex]<0 and hlimit==llimit and hlimit<0:  #long straddle/strangle, edge<0
            if len(be)>0:
                left=0
                right=max(be)*1.5
                highlimit=y[0]-llimit*1.5
                lowlimit= llimit-2
            else:
                lowlimit=y[leftindex]*1.5
                highlimit=hlimit-hlimit*0.5

        elif y[leftindex]<0 and hlimit==llimit and hlimit>0:  #short straddle/strangle, edge<0
            highlimit=hlimit+2
            lowlimit= y[leftindex]-2

        elif y[leftindex]>0 and hlimit==llimit and hlimit>0:  #short straddle/strangle, edge>0
            if len(be)>0:
                left=0
                right=max(be)*1.5
                lowlimit=y[0]-hlimit*1.5
                highlimit= hlimit+2
            else:
                highlimit=y[leftindex]*1.5
                lowlimit = llimit*0.5

        elif y[leftindex]==0 and hlimit==llimit and hlimit<0:  #straddle/strangle, edge=0
            highlimit=-1*llimit*1.25
            lowlimit=llimit*1.25

        elif y[leftindex]==0 and hlimit==llimit and hlimit>0:
            lowlimit=-1*hlimit*1.25
            highlimit=hlimit*1.25

    elif len(k)==1:                         #single strike (hlimit=llimit)
        if y[hindex]>0:                     #infliction above 0 (short call or short put)
            highlimit = y[hindex]+2
            lowlimit = -y[lindex]-extra-1

        elif y[hindex]<0:                   #infliction below 0 (long call or long put)
            lowlimit= y[hindex]-2
            highlimit=-y[lindex]+extra

    if sum(y)==0 and sum(slope)==0:
        be=[0]
        y=[0,0,0,0,0,0,0,0,0,0]
        x=[1,2,3,4,5,6,7,8,9,10]
        right=10
        left=0
        highlimit=10
        lowlimit=-10

    print(f'lowlimit/highlimit: {lowlimit}/{highlimit}')

    #limits for both axis
    plt.ylim(lowlimit, highlimit)
    plt.xlim(left, right)

    #Making the legend text look legit
    if low<0:
        label1=f'MAX LOSS   -${low*-1}'
    else:
        label1=f'MAX LOSS   ${low}'
    if high>0:
        label2=f'MAX PROFIT  ${high}'
    else:
        label2=f'MAX PROFIT -${high*-1}'

    if net<0:
        netlabel=f'Recieved: ${net*-1}'
    elif net==0:
        netlabel=f'ZERO COST'
    else:
        netlabel=f'Paid: ${net}'

    plt.plot([], [], ' ', label=netlabel)
    plt.plot([], [], ' ', label=label1)
    plt.plot([], [], ' ', label=label2)
    plt.plot([], [], ' ', label=f'BE at {be}')
    legend_properties = {'weight':'bold'}
    plt.legend(prop=legend_properties)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig('/home/SamuelMeir/mysite/static/plot.png')

