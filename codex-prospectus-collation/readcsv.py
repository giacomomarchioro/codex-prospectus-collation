import csv
filename = 'MS1853'
#with open('Schema catalogazione manoscritti.csv') as f:
with open(filename+'.csv') as f:
    #f = open('Schema catalogazione manoscritti.csv')
    for i in range(2):
        next(f)
    data = csv.DictReader(f,delimiter=";")
    openingBifoglio = ""
    openingBifoglioCnt = 0
    elemCount = 0
    positions = ["*"]
    listitems = []

    uniqueelements = []
    numerazioni = []
    filigrana = []
    palinsesti = []
    lato = []
    titoli = []
    for j in data:
        if j['bifoglio'] != "":
            idx = j['elemento']+j['sottoelemento']
            #TODO: attenzione per gli inserti
            # il caso in cui ci siano fogli con lo stesso numero
            if idx not in uniqueelements:
                listitems.append(j['bifoglio'])
                uniqueelements.append(idx)
                numerazioni.append(j['numerazione_A'])
                filigrana.append(j['filigrana'])
                palinsesti.append(j['palinsesti'])
                lato.append(j['lato'])
                titoli.append(j['titolo'])
            if positions[-1] != j['bifoglio']:
                positions.append(j['bifoglio'])
            if openingBifoglioCnt == 0:
                print("openingBifoglioCnt:")
                openingBifoglio = j['bifoglio']
                print(openingBifoglio)
            elemCount +=1
            if j['bifoglio'] == openingBifoglio:   
                openingBifoglioCnt +=1
            if openingBifoglioCnt == 4:   
                openingBifoglioCnt = 0
                print("COUNT:")
                print(elemCount)
                elemCount = 0
    print("Elementi non fasciolati: %s" %elemCount)

ld = listitems[::2]
ue = uniqueelements[::2]
lt = lato[::2]

spacers = []
for ind,el in enumerate(ld[1:]):
    if el == ld[ind]:
        spacers.append(ind)
        print(ind)

# aggiungo degli spazi per la piega
added = 1
for i in spacers:
    ld.insert(i+added,"*")
    ue.insert(i+added,"*")
    lt.insert(i+added,"*")
    numerazioni.insert(i*2+added*2,"*")
    numerazioni.insert(i*2+added*2,"*")
    palinsesti.insert(i*2+added*2,"*")
    palinsesti.insert(i*2+added*2,"*")
    filigrana.insert(i*2+added*2,"*")
    filigrana.insert(i*2+added*2,"*")
    titoli.insert(i*2+added*2,"*")
    titoli.insert(i*2+added*2,"*")
    added+=1

fasc = []
for ind,i in enumerate(ld):
    if i == "*":
        continue
    # caso del foglio non fascicolato
    if "bis" in i:
        fasic = dict()
        fasic['starting'] = ind + 1
        fasic['ending'] = ind + 1
        fasic['label'] = i
        fasic['pageid_i'] = ue[ind]
        fasic['pageid_f'] = ue[ind]
        fasic['numerazioni_i'] = (numerazioni[ind*2],numerazioni[ind*2+1])
        fasic['numerazioni_f'] = (numerazioni[ind*2],numerazioni[ind*2+1])
        fasic['palinsesti_i'] = (palinsesti[ind*2],palinsesti[ind*2+1])
        fasic['palinsesti_f'] = (palinsesti[ind*2],palinsesti[ind*2+1])
        fasic['filigrana_i'] = " ".join((filigrana[ind*2],filigrana[ind*2+1]))
        fasic['filigrana_f'] = " ".join((filigrana[ind*2],filigrana[ind*2+1]))
        fasic['lato_i'] = lt[ind]
        fasic['titoli_i'] = (titoli[ind*2],titoli[ind*2+1])
        fasic['titoli_f'] = (titoli[ind*2],titoli[ind*2+1])
        fasc.append(fasic)
    else:
        try:
            nextindex = ld.index(i,ind+1)
            fasic = dict()
            fasic['starting'] = ind + 1
            fasic['ending'] = nextindex + 1
            fasic['label'] = i
            fasic['pageid_i'] = ue[ind]
            fasic['pageid_f'] = ue[nextindex]
            fasic['numerazioni_i'] = (numerazioni[ind*2],numerazioni[ind*2+1])
            fasic['numerazioni_f'] = (numerazioni[nextindex*2],numerazioni[nextindex*2+1])
            fasic['palinsesti_i'] = (palinsesti[ind*2],palinsesti[ind*2+1])
            fasic['palinsesti_f'] = (palinsesti[nextindex*2],palinsesti[nextindex*2+1])
            fasic['filigrana_i'] = " ".join((filigrana[ind*2],filigrana[ind*2+1]))
            fasic['filigrana_f'] = " ".join((filigrana[nextindex*2],filigrana[nextindex*2+1]))
            fasic['titoli_i'] = (titoli[ind*2],titoli[ind*2+1])
            fasic['titoli_f'] = (titoli[nextindex*2],titoli[nextindex*2+1])
            fasic['lato_i'] = lt[ind]
            fasc.append(fasic)
            print(nextindex)
        except ValueError:
            print("ERROR")

spac = 0.4
with open(f"{filename}.svg","w") as f:
    f.write('<?xml version="1.0" standalone="no"?>'+"\n")
    f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'+"\n")
    f.write('<svg width="27cm" height="32cm"  xmlns="http://www.w3.org/2000/svg" version="1.1">'+"\n")
    f.write('<title>Collation %s</title>'%filename+"\n")
    f.write('<desc>Collation of the manuscript.</desc>'+"\n")
    f.write('<style>' +"\n")
    f.write('line {'+"\n")
    f.write('   stroke: black;' +"\n")
    f.write('}'+"\n")
    f.write('path {'+"\n")
    f.write('   stroke: black;' +"\n")
    f.write('}'+"\n")
    f.write('g.bifolio-inserto:hover {'+"\n")
    f.write('   stroke: red !important;' +"\n")
    f.write('   stroke-width: 1.3;' +"\n")
    f.write('   ' +"\n")
    f.write('}'+"\n")
    f.write('.small {'+"\n")
    f.write('  font: italic 12px sans-serif;'+"\n")
    f.write('}'+"\n")
    f.write('.normal {'+"\n")
    f.write('  font: italic 15px sans-serif;'+"\n")
    f.write('}'+"\n")
    f.write('</style>' +"\n")

    for i in fasc:
        xi = 40
        yi = 20
        c1x = 20
        c1y = 20
        c2x = 20
        c2y = 20
        xf = 40
        yf = 20
        xr = 6 # lunghezza spazio rigatura
        pr = 4 # profondità rigatura
        pgl = 50 # lunghezza pagina
        pf = 25 # posizione foro
        df = 1 # dimensione foro
        txtspc = 4
        txtspc2 = txtspc + 30
        txtspc3 = txtspc2 + 30
        txtspc4 = txtspc3 + 30
        txtspc5 = txtspc4 + 30
        txtspc6 = txtspc5 + 30
        yoffset = 100 # padding
        s = i['starting']
        e = i['ending']
        l = i['label']
        es = e - s 
        Yi = yi*s + yoffset
        Yf = yf*e + yoffset
        C1y = c1y*s+yoffset
        C2y = c2y*e+yoffset
        f.write('<g class="bifolio-inserto-t">'+"\n")
        # titoli furodi dal gruppo
        ta,tb = i['titoli_i']
        numiT = f'<tspan dy ="-5">{ta}</tspan> <tspan dy ="+5">{tb}</tspan>'
        txtt_numT = f'<text x="{xf+pgl+txtspc6}" y="{Yi}" class="small" stroke="none">{numiT}</text>'
        f.write(txtt_numT+"\n")
        f.write('<g class="bifolio-inserto">'+"\n")
        # rigatura
        #rl1 = f'<polyline points="{xf},{Yi} {xf+xr/2},{Yi-pr} {xf+xr},{Yi}" fill="none" stroke="black" />'
        #f.write(rl1+"\n")
        # linea fino al foro
        l1i = f'<line x1="{xf+xr}" y1="{Yi}" x2="{xf+pf}" y2="{Yi}" />'
        f.write(l1i+"\n")
        # linea foro
        l1f = f'<line x1="{xf+pf}" y1="{Yi}" x2="{xf+xr+pf+df}" y2="{Yi}" />'
        f.write(l1f+"\n")
        # linea conclusiva
        l1 = f'<line x1="{xf+xr+pf+df}" y1="{Yi}" x2="{xf+pgl}" y2="{Yi}" />'
        f.write(l1+"\n")

        # id del bifoglio
        txtt = f'<text x="{xf+pgl+txtspc}" y="{Yi}" class="small">{l}</text>'
        f.write(txtt+"\n")
        # id della pagina e.g. 1r
        idi = '<tspan>%s   <tspan dy ="-5">r</tspan> <tspan dy ="+10" dx ="-10">v</tspan></tspan>'%i['pageid_i'][:-1]
        txttB = f'<text x="{xf+pgl+txtspc2}" y="{Yi}" class="small">{idi}</text>'
        f.write(txttB+"\n")
        # numerazioni
        a,b = i['numerazioni_i']
        numi = f'<tspan dy ="-5">{a}</tspan> <tspan dy ="+10" dx ="-10">{b}</tspan>'
        txtt_num = f'<text x="{xf+pgl+txtspc3}" y="{Yi}" class="small">{numi}</text>'
        f.write(txtt_num+"\n")
        # palinsesti
        pa,pb = i['palinsesti_i']
        numiP = f'<tspan dy ="-5">{pa}</tspan> <tspan dy ="+10" dx ="-8">{pb}</tspan>'
        txtt_numP = f'<text x="{xf+pgl+txtspc4}" y="{Yi}" class="small">{numiP}</text>'
        f.write(txtt_numP+"\n")
        # filigrana
        fi = i['filigrana_i']
        txttFil = f'<text x="{xf+pgl+txtspc5}" y="{Yi}" class="small">{fi}</text>'
        f.write(txttFil+"\n")
        # lato
        spazio_peli = 4 # spazio tra i due peli
        lPeli = 6 # lunghezza pelo
        iP = 3 # inclinazione pelo
        if i['lato_i'] == "c":
            l1 = f'<line x1="{xf+pgl}" y1="{Yi}" x2="{xf+pgl+iP}" y2="{Yi+lPeli}" />'
            l2 = f'<line x1="{xf+pgl-spazio_peli}" y1="{Yi}" x2="{xf+pgl-spazio_peli+iP}" y2="{Yi+lPeli}"  />'
            f.write(l1+"\n")
            f.write(l2+"\n")
        if i['lato_i'] == "p":
            l1 = f'<line x1="{xf+pgl}" y1="{Yi}" x2="{xf+pgl+iP}" y2="{Yi-lPeli}" />'
            l2 = f'<line x1="{xf+pgl-spazio_peli}" y1="{Yi}" x2="{xf+pgl-spazio_peli+iP}" y2="{Yi-lPeli}"  />'
            f.write(l1+"\n")
            f.write(l2+"\n")

        # solo nell caso di bifoli
        if e != s:
            # seconda parte bifoglio
            # linea fino al foro
            l2i = f'<line x1="{xf+xr}" y1="{Yf}" x2="{xf+pf}" y2="{Yf}" />'
            f.write(l2i+"\n")
            # linea foro
            # l2f = f'<line x1="{xf+pf}" y1="{Yf}" x2="{xf+xr+pf+df}" y2="{Yf}" />'
            # f.write(l2f+"\n")
            # linea conclusiva
            l2 = f'<line x1="{xf+xr+pf+df}" y1="{Yf}" x2="{xf+pgl}" y2="{Yf}" />'
            f.write(l2+"\n")
            # id del bifoglio
            txtb = f'<text x="{xf+pgl+txtspc}" y="{Yf}" class="small">{l}</text>'
            f.write(txtb+"\n")
            r = f'<path d="M {xi} {Yi} C {-es},{C1y} {-es},{C2y} {xf} {Yf}" fill="none" />'+"\n"
            f.write(r)
            # id fogli (e.g. 1r)
            idf = '<tspan>%s   <tspan dy ="-5">r</tspan> <tspan dy ="+10" dx ="-10">v</tspan></tspan>'%i['pageid_f'][:-1]
            txtbB = f'<text x="{xf+pgl+txtspc2}" y="{Yf}" class="small">{idf}</text>'
            f.write(txtbB+"\n")
            # numerazioni
            a,b = i['numerazioni_f']
            numi = f'<tspan dy ="-5">{a}</tspan> <tspan dy ="+10" dx ="-10">{b}</tspan>'
            txtt_num = f'<text x="{xf+pgl+txtspc3}" y="{Yf}" class="small">{numi}</text>'
            f.write(txtt_num+"\n")
            # palinsesti
            pa,pb = i['palinsesti_f']
            numiP = f'<tspan dy ="-5">{pa}</tspan> <tspan dy ="+10" dx ="-8">{pb}</tspan>'
            txtt_numP = f'<text x="{xf+pgl+txtspc4}" y="{Yf}" class="small">{numiP}</text>'
            f.write(txtt_numP+"\n")
            # filigrana
            fi = i['filigrana_f']
            txttFil = f'<text x="{xf+pgl+txtspc5}" y="{Yf}" class="small">{fi}</text>'
            f.write(txttFil+"\n")
            # lato
            if i['lato_i'] == "c":
                l1 = f'<line x1="{xf+pgl}" y1="{Yf}" x2="{xf+pgl+iP}" y2="{Yf-lPeli}" />'
                l2 = f'<line x1="{xf+pgl-spazio_peli}" y1="{Yf}" x2="{xf+pgl-spazio_peli+iP}" y2="{Yf-lPeli}"  />' 
                f.write(l1+"\n")
                f.write(l2+"\n")
            if i['lato_i'] == "p":
                l1 = f'<line x1="{xf+pgl}" y1="{Yf}" x2="{xf+pgl+iP}" y2="{Yf+lPeli}" />'
                l2 = f'<line x1="{xf+pgl-spazio_peli}" y1="{Yf}" x2="{xf+pgl-spazio_peli+iP}" y2="{Yf+lPeli}"  />'
                f.write(l1+"\n")
                f.write(l2+"\n")
            # rigatura
            #rigatura
            rigatura_a_secco = False
            if rigatura_a_secco:
                rl1 = f'<polyline points="{xf},{Yf} {xf+xr/2},{Yf-pr} {xf+xr},{Yf}" fill="none" stroke="black" />'
                f.write(rl1+"\n")
            rigatura_a_inchiostro = False
            if rigatura_a_inchiostro:
                rl1 = f'<line x1="{xf}" y1="{Yf}" x2="{xf+xr}" y2="{Yf}" stroke-width="3" />' 
                f.write(rl1+"\n")
            f.write('</g>'+"\n")
             # titoli
            ta,tb = i['titoli_f']
            numiT = f'<tspan dy ="-5">{ta}</tspan> <tspan dy ="+5">{tb}</tspan>'
            txtt_numT = f'<text x="{xf+pgl+txtspc6}" y="{Yf}" class="small" stroke="none">{numiT}</text>'
            f.write(txtt_numT+"\n")
        else:
            f.write('</g>'+"\n")    
        f.write('</g>'+"\n")

    f.write(f'<text transform="translate({xf}, 5) rotate(90) " class="normal">Rigatura</text>')
    f.write(f'<text transform="translate({xf+pf}, 5) rotate(90) " class="normal">Foratura</text>')
    f.write(f'<text transform="translate({xf+pgl+txtspc}, 5) rotate(90) " class="normal">Bifolio/insert</text>')
    f.write(f'<text transform="translate({xf+pgl+txtspc2}, 5) rotate(90)" class="normal">ID folio</text>')
    f.write(f'<text transform="translate({xf+pgl+txtspc3}, 5) rotate(90)" class="normal">Numerazione</text>')
    f.write(f'<text transform="translate({xf+pgl+txtspc4}, 5) rotate(90)" class="normal">Palinsesto</text>')
    f.write(f'<text transform="translate({xf+pgl+txtspc5}, 5) rotate(90)" class="normal">Filigrana</text>')
    f.write(f'<text transform="translate({xf+pgl+txtspc6}, 5) rotate(90)" class="normal">Titoli</text>')


    f.write('</svg>')