#!/usr/bin/python3
import sys,os,os.path,argparse,re,collections

##########################################################################
##########################################################################

OutputLine=collections.namedtuple('OutputLine','label instr comment')

def main3(input_lines,f_out,options):
    opcode_column=16
    comment_column=32

    weak_re=re.compile(r'''^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\?\s*(?P<value>.*)$''')
    cpu_re=re.compile(r'''^\s*CPU\s+(?P<value>.*)$''')
    org_re=re.compile(r'''^\s*ORG\s+(?P<value>.*)$''')
    symbol_re=re.compile(r'''^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>.*)$''')
    label_re=re.compile(r'''^\.(?P<name>[A-Za-z_][A-Za-z0-9_]*)$''')
    instr_re=re.compile(r'''^\s+(?P<instr>[A-Za-z]+)(\s+(?P<operands>.*))?$''')
    if_re=re.compile(r'''^\s*IF (?P<cond>.*)$''')
    elif_re=re.compile(r'''^\s*ELIF (?P<cond>.*)$''')
    else_re=re.compile(r'''^\s*ELSE$''')
    endif_re=re.compile(r'''^\s*ENDIF$''')
    unwanted_stuff_re=re.compile(r'''^save\s+.*$''')
    
    output_lines=[]

    def add(label,instr,comment):
        output_lines.append(OutputLine(label=label,
                                       instr=instr,
                                       comment=comment))

    def get_fixed_up_cond(cond):
        if cond.startswith('_'): cond=cond[1:]
        return cond

    f_out.write('; automatically converted from: %s\n'%(options.input_path))

    unrecognised=[]
    for input_line_idx,input_line in enumerate(input_lines):
        def fatal(msg):
            sys.stderr.write('%s:%d: %s\n'%(options.input_path,
                                            input_line_idx+1,
                                            msg))
            sys.exit(1)

        if input_line.strip()=='':
            add(None,None,None)
            continue
        
        comment_index=input_line.find(';')
        if comment_index<0: comment=None
        elif comment_index==0:
            add(input_line,None,None)
            continue
        else:
            comment=input_line[comment_index:]
            input_line=input_line[:comment_index].rstrip()
            if input_line=='':
                add(None,None,comment)
                continue

        m=weak_re.match(input_line)
        if m is not None:
            name=m.group('name')
            if name.startswith('_'): name=name[1:]

            value=m.group('value')
            try: value=int(value)
            except: value=None
            if value is None: fatal('bad value: %s'%(m.group('value')))
            elif value==0: value='false'
            else: value='true'

            add(None,'.weak',None)
            add('%s=%s'%(name,value),None,comment)
            add(None,'.endweak',None)
            continue

        m=cpu_re.match(input_line)
        if m is not None:
            cpu=m.group('value')
            if cpu=='1': cpu='65c02'
            else: fatal('unrecognised CPU value: %s'%cpu)

            add(None,'.cpu "%s"'%cpu,comment)
            continue

        m=org_re.match(input_line)
        if m is not None:
            add('*=%s'%(m.group('value')),None,comment)
            continue

        m=symbol_re.match(input_line)
        if m is not None:
            add('%s=%s'%(m.group('name'),m.group('value')),None,comment)
            continue

        m=label_re.match(input_line)
        if m is not None:
            add('%s:'%(m.group('name')),None,comment)
            continue

        m=if_re.match(input_line)
        if m is not None:
            cond=get_fixed_up_cond(m.group('cond'))
            add(None,'.if %s'%cond,comment)
            continue

        m=elif_re.match(input_line)
        if m is not None:
            cond=get_fixed_up_cond(m.group('cond'))
            add(None,'.elif %s'%cond,comment)
            continue
        
        m=else_re.match(input_line)
        if m is not None:
            add(None,'.else',comment)
            continue
        
        m=endif_re.match(input_line)
        if m is not None:
            add(None,'.endif',comment)
            continue

        m=unwanted_stuff_re.match(input_line)
        if m is not None: continue

        # always do this last.
        m=instr_re.match(input_line)
        if m is not None:
            instr=m.group('instr').lower()

            if instr=='equb':
                # docs say it's for signed 8-bit values, but it seems
                # to handle the unsigned variety fine as well...
                instr='.char'
            if instr=='equw': instr='.word'
            elif instr=='equd': instr='.dint'
            elif instr=='equs': instr='.text'
            
            operands=m.group('operands')
            if operands is not None:
                if operands=='A': operands='a'
                else:
                    for suffix in [',X',',Y',',X)']:
                        if operands.endswith(suffix):
                            operands=operands[:-len(suffix)]
                            operands+=suffix.lower()
                            break

            if operands is None: add(None,instr,comment)
            else: add(None,'%s %s'%(instr,operands),comment)
            continue

        unrecognised.append((input_line_idx,input_lines[input_line_idx]))

    # peephole depessimization
    i=0
    while i<len(output_lines)-1:
        a=output_lines[i+0]
        b=output_lines[i+1]

        if (a.label is None and
            a.instr=='.endweak' and
            a.comment is None and
            b.label is None and
            b.instr=='.weak' and
            b.comment is None):
            del output_lines[i:i+2]
        else: i+=1

    for output_line in output_lines:
        text=''
        
        def pad(n):
            nonlocal text
            
            if len(text)>=n: text+=' '
            elif len(text)<n: text+=(n-len(text))*' '

        if output_line.label is not None: text+=output_line.label

        if output_line.instr is not None:
            pad(opcode_column)
            text+=output_line.instr

        if output_line.comment is not None:
            pad(comment_column)
            text+=output_line.comment

        f_out.write(text)
        f_out.write('\n')

    if len(unrecognised)>0:
        f_out.write('; %d unrecognised lines:\n'%len(unrecognised))
        for idx,text in unrecognised: f_out.write('; %d:%s\n'%(idx+1,text))

def main2(options):
    with open(options.input_path,'rt') as f:
        lines=[line.rstrip() for line in f.readlines()]

    if options.output_path is None: main3(lines,sys.stdout,options)
    else:
        with open(options.output_path,'wt') as f: main3(lines,f,options)

##########################################################################
##########################################################################

def main(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument('input_path',metavar='FILE',help='''read input from %(metavar)s''')
    parser.add_argument('-o',dest='output_path',metavar='FILE',help='''write output to %(metavar)s (stdout if not provided)''')
    main2(parser.parse_args(argv))

if __name__=='__main__': main(sys.argv[1:])
