"""Embed native DeviceIO audio routing; keep Push enums and banks fixed."""
def add_audio_routing(p, root):
    boxes, lines = p['boxes'], p['lines']
    def add(i, text=None, cls='newobj', **kw):
        b = dict(id=i, maxclass=cls, patching_rect=[10,1000,200,22], **kw)
        if text is not None: b['text'] = text
        boxes.append({'box':b})
    def wire(a,b,ao=0,bi=0):
        lines.append({'patchline':dict(source=[a,ao],destination=[b,bi])})
    add('audiorouter', cls='v8.codebox', code=(root/'src/audio-input.js').read_text(),
        filename='none', numinlets=1, numoutlets=2, outlettype=['',''])
    add('audioboot','live.thisdevice'); add('audiodefer','deferlow')
    add('audiosettle','delay 750'); add('audioinit','init',cls='message')
    wire('audioboot','audiodefer');wire('audiodefer','audiosettle');wire('audiosettle','audioinit');wire('audioinit','audiorouter')
    for n,selector in [('extsource','source'),('exttap','tap')]:
        add('audiosend_'+n,'prepend '+selector);wire(n,'audiosend_'+n);wire('audiosend_'+n,'audiorouter')
    wire('audiorouter','engine')
    add('audiostatussend','s #0-audio-status');wire('audiorouter','audiostatussend',1)
    add('audioclose','closebang');add('audioshutdown','shutdown',cls='message')
    wire('audioclose','audioshutdown');wire('audioshutdown','audiorouter')
    popup=next(e['box']['patcher'] for e in boxes if e['box']['id']=='instrument')
    popup['boxes'].append({'box':dict(id='audiostatusrecv',maxclass='newobj',text='r #0-audio-status',patching_rect=[540,800,170,22])})
    popup['lines'].append({'patchline':dict(source=['audiostatusrecv',0],destination=['audio_status',0])})
