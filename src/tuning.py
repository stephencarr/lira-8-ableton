"""Embed temporary note selection without new saved parameters or bank edits."""
def add_tuning(p, root):
    boxes, lines = p['boxes'], p['lines']
    by = {e['box']['id']: e['box'] for e in boxes}
    names = [f'tune{i}' for i in range(1,9)] + ['pitch1','pitch2']
    def add(i, text=None, cls='newobj', **kw):
        b = dict(id=i, maxclass=cls, patching_rect=[20,1100,240,22], **kw)
        if text is not None: b['text']=text
        boxes.append({'box':b})
    def wire(a,b,o=0,i=0):
        lines.append({'patchline':dict(source=[a,o],destination=[b,i])})
    add('notetuner', cls='v8.codebox', code=(root/'src/tuning.js').read_text(),
        filename='none', numinlets=1, numoutlets=5, outlettype=['']*5, varname='notetuner')
    add('tunedefer','deferlow');wire('tunedefer','notetuner')
    for n in names:
        by[n]['saved_attribute_attributes']['valueof'].update(parameter_unitstyle=9,parameter_units='%.0f')
        by[n]['hint'] += ' · Hold Push Shift to select notes (Tune) or transpose in semitones (Pitch).'
        for edge in lines:
            pl=edge['patchline']
            if pl['source']==['send_'+n,0] and pl['destination']==['engine',0]:pl['destination']=['tunedefer',0]
        lines[:]=[e for e in lines if e['patchline']['source']!=[n,0] or e['patchline']['destination']!=['ui_set_'+n,0]]
    wire('notetuner','engine')
    for suffix,out in [('root',1),('label',2),('mirror',3)]:
        add('tuneroute_'+suffix,'route '+' '.join(names),numoutlets=len(names)+1)
        wire('notetuner','tuneroute_'+suffix,out)
        for i,n in enumerate(names):
            if suffix=='root':wire('tuneroute_'+suffix,n,i)
            elif suffix=='mirror':wire('tuneroute_'+suffix,'ui_state_'+n,i)
            else:
                add('tunelabelsend_'+n,'s #0-notelabel-'+n);wire('tuneroute_'+suffix,'tunelabelsend_'+n,i)
    add('tuneboot','live.thisdevice');add('tuneinitdefer','deferlow');add('tunesettle','delay 450')
    add('tuneinit','init',cls='message')
    wire('tuneboot','tuneinitdefer');wire('tuneinitdefer','tunesettle');wire('tunesettle','tuneinit');wire('tuneinit','notetuner')
    add('tuneclose','closebang');add('tuneshutdown','shutdown',cls='message')
    wire('tuneclose','tuneshutdown');wire('tuneshutdown','notetuner')
    wire('padcontroller','tunedefer',1)
    by['pdtrigger']['text']='t b b'
    add('tunepreset','preset',cls='message');wire('pdtrigger','tunepreset',1);wire('tunepreset','tunedefer')
    add('tunemanualrecv','r #0-note-manual');add('tunemanual','prepend manual')
    wire('tunemanualrecv','tunemanual');wire('tunemanual','tunedefer')
    add('tunestatussend','s #0-note-status');wire('notetuner','tunestatussend',4)
    popup=by['instrument']['patcher']
    for n in names:
        popup['boxes'].append({'box':dict(id='notelabel_'+n,maxclass='newobj',text='r #0-notelabel-'+n,patching_rect=[20,900,200,22])})
        popup['lines'].append({'patchline':dict(source=['notelabel_'+n,0],destination=['label_'+n,0])})
    popup['boxes'].append({'box':dict(id='notemanual',maxclass='textbutton',mode=1,text='Note tune Off',texton='Note tune On',
        presentation=1,presentation_rect=[510,14,150,26],patching_rect=[510,14,150,26],numinlets=1,numoutlets=3,
        active=1,legacytextcolor=1,usegradient=0,usebgoncolor=1,fontsize=12,
        bgcolor=[.29,.26,.29,1],bgoncolor=[.92,.56,.70,1],textcolor=[.96,.92,.94,1],textoncolor=[.1,.07,.1,1])})
    popup['boxes'].append({'box':dict(id='notemanualsend',maxclass='newobj',text='s #0-note-manual',patching_rect=[20,930,200,22])})
    popup['lines'].append({'patchline':dict(source=['notemanual',0],destination=['notemanualsend',0])})
    popup['boxes'].append({'box':dict(id='notestatusrecv',maxclass='newobj',text='r #0-note-status',patching_rect=[20,960,200,22])})
    popup['lines'].append({'patchline':dict(source=['notestatusrecv',0],destination=['footer',0])})
    for e in popup['boxes']:
        if e['box']['id']=='fullsubtitle':e['box'].update(text='PAD EDITION · eight voices',presentation_rect=[260,21,240,24])
