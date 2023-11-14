import csv
# the name of the csv file to be loaded
filename = 'TESTSO'

with open(filename+'.csv') as f:
    # we skip the first two lines of the file.
    for i in range(2):
        next(f)
    # here we set the delimiter note that CSV should be comma separated but
    # often semicolon is used.
    # We read the data into a dictionary
    data = csv.DictReader(f,delimiter=",")

    openingBifoglio = ""
    openingBifoglioCnt = 0
    elemCount = 0
    # keep track of the current bifolios, starts with *
    positions = ["*"] # UNUSED
    # Bifolio ID e.g. ['1','1','2','2','1','1']
    bfId = []
    # pageId e.g. ['1r,'1v','2r'...]
    pageId = []
    # side type flesh or hair e.g. ['p,'c','c','p'...]
    side = []
    numerazioni = []
    filigrana = []
    palinsesti = []

    titoli = []
    for j in data:
        if j['sottoelemento'] == "g":
            pass
        if j['bifoglio'] != "":
            # this is the id  of the page for instance 3v, 5r
            idx = j['elemento']+j['sottoelemento']
            #TODO: case when we have the same id, e.g. some foldout or an "inserto"
            # otherwise:
            if idx not in pageId:
                bfId.append(j['bifoglio'])
                pageId.append(idx)
                numerazioni.append(j['numerazione_A'])
                filigrana.append(j['filigrana'])
                palinsesti.append(j['palinsesti'])
                side.append(j['lato'])
                titoli.append(j['titolo'])
            # if we change the bifoglio we change position of the page
            if positions[-1] != j['bifoglio']:
                positions.append(j['bifoglio'])
            # this is the first bifoglio found.
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

ld = bfId[::2]
ue = pageId[::2]
lt = side[::2]

spacers = []
# we need these spacers when we have a bended bifolio.
for ind,el in enumerate(ld[1:]):
    # if the bifolio id is the same for two consecutive id we record the index
    # where we have to add the spacer
    if el == ld[ind]:
        spacers.append(ind)
        print(ind)

# we insert * to be able to track when we have to add an extra space
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

# fasc will contain our data structure
fasc = []
# we are iterating of the even bifolios indexes bfId[::2]
for ind,i in enumerate(ld):
    # case we have to skip.
    if i == "*":
        continue
    # case of an added bifolio e.g. 3bis
    if "bis" in i:
        fasic = dict()
        fasic['tipo'] = "pagina singola" # type of obejct
        fasic['starting'] = ind + 1
        fasic['ending'] = ld.index("*",ind)
        fasic['label'] = i # e.g. 3 bifolio id
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
            fasic['tipo'] = "bifolio"
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
with open(f"{filename}_2.svg","w") as f:
    f.write('<?xml version="1.0" standalone="no"?>'+"\n")
    f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'+"\n")
    f.write('<svg width="27cm" height="32cm"  xmlns="http://www.w3.org/2000/svg" version="1.1">'+"\n")
    f.write('<title>Collation %s</title>'%filename+"\n")
    f.write('<desc>Collation of the manuscript.</desc>'+"\n")
    # this add the CSS functionality of the highlighting on hover
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
    yr = 120

    rectfil = f'<rect x="40" y="{yr}" width="500" height="10" fill="black"></rect>'
    f.write(rectfil+"\n")
    for i in fasc:
        xi = 40
        yi = 20
        c1x = 20
        c1y = 20
        c2x = 20
        c2y = 20
        xf = 40
        yf = 20
        xr = 6 # ruling space
        pr = 4 # ruling depth
        pgl = 50 # page length
        pf = 25 # hole position
        df = 1 # hole dimension
        txtspc = 4
        txtspc2 = txtspc + 30
        txtspc3 = txtspc2 + 30
        txtspc4 = txtspc3 + 30
        txtspc5 = txtspc4 + 30
        txtspc6 = txtspc5 + 30
        yoffset = 150 # padding
        s = i['starting']
        e = i['ending']
        l = i['label']
        es = e - s
        Yi = yi*s + yoffset
        Yf = yf*e + yoffset
        C1y = c1y*s+yoffset
        C2y = c2y*e+yoffset
        f.write('<g class="bifolio-inserto-t">'+"\n")
        # titles
        ta,tb = i['titoli_i']
        numiT = f'<tspan dy ="-5">{ta}</tspan> <tspan dy ="+5">{tb}</tspan>'
        txtt_numT = f'<text x="{xf+pgl+txtspc6}" y="{Yi}" class="small" stroke="none">{numiT}</text>'
        f.write(txtt_numT+"\n")
        f.write('<g class="bifolio-inserto">'+"\n")
        # ruling
        rl1 = f'<polyline points="{xf},{Yi} {xf+xr/2},{Yi-pr} {xf+xr},{Yi}" fill="none" stroke="black" />'
        f.write(rl1+"\n")
        # line connecting the holes
        l1i = f'<line x1="{xf+xr}" y1="{Yi}" x2="{xf+pf}" y2="{Yi}" />'
        f.write(l1i+"\n")
        # linea foro
        # l1f = f'<line x1="{xf+pf}" y1="{Yi}" x2="{xf+xr+pf+df}" y2="{Yi}" />'
        # f.write(l1f+"\n")
        # linea conclusiva
        l1 = f'<line x1="{xf+xr+pf+df}" y1="{Yi}" x2="{xf+pgl}" y2="{Yi}" />'
        f.write(l1+"\n")
        # id bifolium
        txtt = f'<text x="{xf+pgl+txtspc}" y="{Yi}" class="small">{l}</text>'
        f.write(txtt+"\n")
        # id page e.g. 1r
        idi = '<tspan>%s   <tspan dy ="-5">r</tspan> <tspan dy ="+10" dx ="-10">v</tspan></tspan>'%i['pageid_i'][:-1]
        txttB = f'<text x="{xf+pgl+txtspc2}" y="{Yi}" class="small">{idi}</text>'
        f.write(txttB+"\n")
        # numbering
        a,b = i['numerazioni_i']
        numi = f'<tspan dy ="-5">{a}</tspan> <tspan dy ="+10" dx ="-10">{b}</tspan>'
        txtt_num = f'<text x="{xf+pgl+txtspc3}" y="{Yi}" class="small">{numi}</text>'
        f.write(txtt_num+"\n")
        # palimpsests
        pa,pb = i['palinsesti_i']
        numiP = f'<tspan dy ="-5">{pa}</tspan> <tspan dy ="+10" dx ="-8">{pb}</tspan>'
        txtt_numP = f'<text x="{xf+pgl+txtspc4}" y="{Yi}" class="small">{numiP}</text>'
        f.write(txtt_numP+"\n")
        # watermark
        fi = i['filigrana_i']
        txttFil = f'<text x="{xf+pgl+txtspc5}" y="{Yi}" class="small">{fi}</text>'
        f.write(txttFil+"\n")
        # side
        spazio_peli = 4 # space between hair
        lPeli = 6 # hair length
        iP = 3 # har dimension
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

        if i['tipo'] == "pagina singolaA":
            # Bezier
            #r = f'<path id="test" d="M {xi} {Yi} C {-es},{C1y} {-es},{C2y} {xf} {Yf}" fill="none" />'
            r = f'<line x1="{xi}" y1="{Yi}" x2="{xi-20}" y2="{Yi+20}"  />'
            f.write(r+"\n")

        if i['tipo'] == "pagina singolaB":
            # Bezier
            r = f'<path id="test" d="M {xi} {Yi} C 10,{C1y} 10,{C1y+5} {xf} {Yi+5}" fill="none" />'
            f.write(r+"\n")

        if i['tipo'] == "pagina singolaC":
            # Bezier
            r = f'<path id="test" d="M {xi} {Yi} C 10,{C1y} 10,{C1y-5} {xf} {Yi-5}" fill="none" />'
            f.write(r+"\n")

        if i['tipo'] == "pagina singola":
            # Bezier
            r = f'<path id="test" d="M {xi} {Yi} C 10,{C1y} 10,{C1y-5} {xf} {Yi-5}" fill="none" />'
            f.write(r+"\n")

        # only in case of bifolium type
        if i['tipo'] == "bifolio":
            #  bifolioum
            # ending line
            of = -5
            l2i = f'<line x1="{xf+xr}" y1="{Yf+of}" x2="{xf+pf}" y2="{Yf+of}" />'
            f.write(l2i+"\n")
            # line to the hole
            # l2f = f'<line x1="{xf+pf}" y1="{Yf}" x2="{xf+xr+pf+df}" y2="{Yf}" />'
            # f.write(l2f+"\n")
            # linea conclusiva
            l2 = f'<line x1="{xf+xr+pf+df}" y1="{Yf+of}" x2="{xf+pgl}" y2="{Yf+of}" />'
            f.write(l2+"\n")
            # id  bifolium
            txtb = f'<text x="{xf+pgl+txtspc}" y="{Yf}" class="small">{l}</text>'
            f.write(txtb+"\n")
            # Bezier
            r = f'<path d="M {xi} {Yi} C {-es},{C1y} {-es},{C2y} {xf} {Yf}" fill="none" />'
            f.write(r+"\n")
            # id fogli (e.g. 1r)
            idf = '<tspan>%s   <tspan dy ="-5">r</tspan> <tspan dy ="+10" dx ="-10">v</tspan></tspan>'%i['pageid_f'][:-1]
            txtbB = f'<text x="{xf+pgl+txtspc2}" y="{Yf}" class="small">{idf}</text>'
            f.write(txtbB+"\n")
            # numbering
            a,b = i['numerazioni_f']
            numi = f'<tspan dy ="-5">{a}</tspan> <tspan dy ="+10" dx ="-10">{b}</tspan>'
            txtt_num = f'<text x="{xf+pgl+txtspc3}" y="{Yf}" class="small">{numi}</text>'
            f.write(txtt_num+"\n")
            # palimpsest
            pa,pb = i['palinsesti_f']
            numiP = f'<tspan dy ="-5">{pa}</tspan> <tspan dy ="+10" dx ="-8">{pb}</tspan>'
            txtt_numP = f'<text x="{xf+pgl+txtspc4}" y="{Yf}" class="small">{numiP}</text>'
            f.write(txtt_numP+"\n")
            # watermarks
            fi = i['filigrana_f']
            txttFil = f'<text x="{xf+pgl+txtspc5}" y="{Yf}" class="small">{fi}</text>'
            f.write(txttFil+"\n")
            rectangle = True
            if rectangle:
                rectfil = f'<rect x="{xf+2}" y="{Yf-2}" width="{pgl-4}" height="10" fill="gray"></rect>'
                f.write(rectfil+"\n")

            # side
            if i['lato_i'] == "c":
                l1 = f'<line x1="{xf+pgl}" y1="{Yf+of}" x2="{xf+pgl+iP}" y2="{Yf-lPeli+of}" />'
                l2 = f'<line x1="{xf+pgl-spazio_peli}" y1="{Yf+of}" x2="{xf+pgl-spazio_peli+iP}" y2="{Yf-lPeli+of}"  />' 
                f.write(l1+"\n")
                f.write(l2+"\n")
            if i['lato_i'] == "p":
                l1 = f'<line x1="{xf+pgl}" y1="{Yf+of}" x2="{xf+pgl+iP}" y2="{Yf+lPeli+of}" />'
                l2 = f'<line x1="{xf+pgl-spazio_peli}" y1="{Yf+of}" x2="{xf+pgl-spazio_peli+iP}" y2="{Yf+lPeli+of}"  />'
                f.write(l1+"\n")
                f.write(l2+"\n")
            # ruling
            rigatura_a_secco = False
            if rigatura_a_secco:
                rl1 = f'<polyline points="{xf},{Yf+of} {xf+xr/2},{Yf-pr} {xf+xr},{Yf+of}" fill="none" stroke="black" />'
                f.write(rl1+"\n")
            rigatura_a_inchiostro = True
            if rigatura_a_inchiostro:
                rl1 = f'<line x1="{xf}" y1="{Yf+of}" x2="{xf+xr}" y2="{Yf+of}" stroke-width="3" />' 
                f.write(rl1+"\n")
            f.write('</g>'+"\n")
            # titles
            ta,tb = i['titoli_f']
            numiT = f'<tspan dy ="-5">{ta}</tspan> <tspan dy ="+5">{tb}</tspan>'
            txtt_numT = f'<text x="{xf+pgl+txtspc6}" y="{Yf}" class="small" stroke="none">{numiT}</text>'
            f.write(txtt_numT+"\n")
            f.write('</g>'+"\n")
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