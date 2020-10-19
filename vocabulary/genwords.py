#coding: utf-8
#!/usr/bin/env python


# This is choosing learning English words
# from TeX file, but in a random sequence,
# to prepare learning English well for XiaoXiao

# And as an enhancement, I let it also support
# YuWen output, for speed up HanZi Learning!

import getopt
import random
import re
import sys

glbDbg = 0


def usage():
    print 'genwords.py -f words.tex/--file=words.tex'
    print '            -y/--yuwen  : extract HanZi word list'
    print '            -s/--sente  : English sentence mode'
    return

def demo_global_usage():
    global Name
    print 'the global name is %s' %(Name)
    Name += 'goo'
    return

def extract_word(data):
    ok = 0
    word = 'N/A'

    ret = re.search(r'\s{0,}\{name=\{(.*?)\}', data)
    if ret != None:
        ok = 1
        word = ret.group(1)
    else:
        #print 'Pity, not matched'
        ret = 0 # actually, not matched at all

    return (ok, word)

def extract_yuwen_word(data):
    ok = 0
    word = 'N/A'

    ret = re.search(r'^\\indexentry\{(.*?)\|', data)
    if ret != None:
        ok = 1
        word = ret.group(1)
    else:
        print 'Pity'
    return (ok, word)

def parse_tex(fn, wlist, yuwen=None):
    try:
        fd = open(fn)

        line = fd.readline()
        while line:
            if yuwen is None:
                (ret, w) = extract_word(line.strip())
                if ret == 1:
                    wlist.append(w)
            else:
                (ret, w) = extract_yuwen_word(line.strip())
                if ret == 1:
                    wlist.append(w)

            line = fd.readline()

        fd.close()
    except:
        print '%s || %s' %(sys.exc_clear()[0], sys.exc_info()[1])
    return 0

######################################################
# Shutffle the @wlist, stored to @target
def output_words(wlist, target):
    wdcnt = len(wlist)
    if glbDbg == 1:
        print 'totally %d words in the original list' %(wdcnt)

    for i in range(0, wdcnt):
        idx = random.randint(0, wdcnt - 1) # randint is [m,n], not like the range!

        if glbDbg == 1:
            print 'the random index=%d' %(idx)
            print 'and the value is %s' %(wlist[idx])
            if wlist[idx] in target:
                print 'Wow, already existed'
            else:
                print 'Bingo, safe to add'

        # make sure always get a valid random chars
        while wlist[idx] in target:
            if glbDbg == 1:
                print 'keep get another shuffle random index'
            idx = random.randint(0, wdcnt - 1)

        target.append(wlist[idx])

    return 0

######################################################
# to make it simpler, cols MUST be 4
def write_tex_table(fd, wdlist, cols):
    idx = 0 # the N.O. of whole word list

    if glbDbg == 1:
        print 'the cols is %d' %(cols)

    for i in range(0, len(wdlist)/cols):
        linefmt = ''
        for j in range(0, cols):
            if j != 0:
                linefmt += '&'
            sec = '{' + str(idx + 1 + j) + '} &'
            linefmt += sec

            sec = '{' + wdlist[idx + j] + '}'
            linefmt += sec

        linefmt += "\\\\ \n"
        fd.write(linefmt)
        idx += cols
    # take care of reamining stuff
    if (len(wdlist) - idx) > 0:
        linefmt = ''
        for i in range(0, (len(wdlist) - idx)):
            if i != 0:
                linefmt += '&'
            sec = '{' + str(idx + 1 + i) + '} &'
            linefmt += sec

            sec = '{' + wdlist[idx + i] + '}'
            linefmt += sec
        linefmt += "\\\\ \n"
        fd.write(linefmt)

    return 0

######################################################
# get pretty output format,
# check https://segmentfault.com/q/1010000000345748
#
#for a, b in data:
# print('%-20s%-20s' % (a, b))
#
def pretty_output(cols, wdlist):
    idx = 0
    print '====================================='
    for i in range(0, len(wdlist) / cols):
        fmt = ''
        for j in range(0, cols):
            fmt += '%-15s' %(wdlist[idx + j])

        print fmt
        idx += cols
    # try output the reamining stuff...
    if glbDbg == 1:
        print '  [DEBUG LOG]idx is %d while full len is %d' % (idx, len(wdlist))

    if (len(wdlist) - idx) > 0:
        fmt = ''
        for i in range(0, (len(wdlist) - idx)):
            fmt += '%-15s' %(wdlist[idx + i])

        print fmt
    print '====================================='
    return 0

# this is make Chinese >2 chars to a tail,
# and made single word to head
def float_single_words(wdlist):
    long_words = []
    extra_long = []

    for it in wdlist:
        if len(it.decode('utf-8')) > 2:
            extra_long.append(it)
        elif len(it.decode('utf-8')) > 1:
            long_words.append(it)

    for it in long_words:
        wdlist.remove(it)
        wdlist.append(it)

    for it in extra_long:
        wdlist.remove(it)
        wdlist.append(it)

    return 0

######################################################
# @pdftex : the PDF tex, which generated based on @template
# @template : the template TeX file name
# @cols : the columns of the whole word list
# @wdlist : the word list data
def create_print_pdf(pdftex, template, cols, wdlist):
    fmt = ''
    startinsertion = 0 # 1 - begin, 2 - finished

    # JUST console output
    pretty_output(cols, wdlist)

    # above is just console output, next will
    # generate PDF file...
    try:
        ftemplate = open(template)
        fd = open(pdftex, 'w')

        if glbDbg == 1:
            print 'can we get the log?'

        line = ftemplate.readline()
        while line:

            if 'CHANGE BEGIN' in line:
                startinsertion = 1
                if glbDbg == 1:
                    print 'added the new code'

            elif 'CHANGE END' in line:
                startinsertion = 2 # let it finished
                if glbDbg == 1:
                    print 'finished the new code'
            else:
                fd.write(line)

            if startinsertion == 1:
                write_tex_table(fd, wdlist, cols)

            line = ftemplate.readline()

        ftemplate.close()
        fd.close()

    except:
        print '%s || %s' %(sys.exc_info()[0], sys.exc_info()[1])

    return 0

def do_with_search(data):
    ret = re.search(r"\\begin{abc}.*end{abc}", data, re.S)
    if ret != None:
        print("===>matched")
        print(ret.group(0))
    else:
        print("PITY")
    return 0

def foo():
    datafile = "test.data"
    with open(datafile) as f:
        block_txt = f.read()
        print(block_txt)
        do_with_search(block_txt)
#ret = re.search("begin\{abc\}.*end\{abc\}", block_txt)
#ret = re.search(r"\\begin{abc(.*?)abc}", block_txt, re.S)
        ret = re.findall(r"\\begin{abc}.*?{abc}", block_txt, re.S)
        print ret
        ret = re.findall(r"\\begin{abc}(.*?){abc}", block_txt, re.S)
        print ret
#if ret != None:
#            print("===>matched")
#            print(ret.group(0))
#        else:
#            print("bad match")
    return 0

### English Super Sentence
class SuperSentence:

    __TEMPLATE_TEX = "\\documentclass[a4paper]{article}\n" \
    "\\title{foo}\n" \
    "\\usepackage{tipa} % MUST defined before fontspec\n" \
    "\\usepackage{fontspec,xunicode,xltxtra,makeidx,xecolor}\n" \
    "\\usepackage{indentfirst}\n" \
    "\\usepackage{amsmath,amsfonts,amssymb}\n" \
    "\\usepackage{tikz}\n" \
    "\\usetikzlibrary{arrows,shapes,trees,calc,fit,automata,positioning,intersections,through}\n" \
    "\\usetikzlibrary{datavisualization}\n" \
    "\\usetikzlibrary{datavisualization.formats.functions}\n" \
    "\\usetikzlibrary{datavisualization.polar}\n" \
    "\\usetikzlibrary{angles,shadows}\n" \
    "\\usetikzlibrary{patterns}\n" \
    "\\usepackage{listings}\n" \
    "\\usepackage{xeCJK}\n" \
    "\\usepackage{xpinyin}\n" \
    "\\usepackage{tkz-base}\n" \
    "\\usepackage{soul}\n" \
    "\\usepackage{exsheets}\n" \
    "\\usepackage{tasks}\n" \
    "\\setmainfont{DejaVu Sans} % let 'Exercies' be bold\n" \
    "\\setCJKmainfont{WenQuanYi Micro Hei}\n" \
    "\\newfontfamily\\thekai{STKaiti}\n" \
    "\\setlength\marginparwidth{2cm}\n" \
    "\\makeatletter\n" \
    "\\long\def\@ympar#1{\n" \
    "  \\@savemarbox\\@marbox{\\thekai\\footnotesize #1}\n" \
    "  \\global\\setbox\\@currbox\\copy\\@marbox\n" \
    "  \\@xympar}\n" \
    "\\makeatother\n" \
    "\\setlength{\parindent}{2em}\n" \
    "\\setlength{\parskip}{0.5\\baselineskip}\n" \
    "\\newcounter{printdemonum}\n" \
    "\\newenvironment{printdemosample}{\\stepcounter{printdemonum} " \
    "\\tikz {baseline={([yshift=-.8ex]current bounding box.center)}] {\\node[rectangle]{\\includegraphics[scale=0.10]{../latex/images/huawen.EPS}}} " \
    "{\kai{例句} \\theprintdemonum{}} \\vspace{-0.41cm} \\begin{quotation}} {\\end{quotation}}\n" \
    "\\begin{document}\n" \
    "\\maketitle\n"

    __TEMPLATE_TEX_END = "\\end{document}"

      # I try note down all samples on hard-code file list...
    __input_fn = ["ch_concrete_eng.tex", "cards.tex"]
    __demo_list = []

    def fan_in(self, alldata):
        for it in alldata:
            self.__demo_list.append(it)
        return 0

    def extract_demo(self, fn):
        with open(fn) as f:
            block_txt = f.read()
            ret = re.findall(r"\\begin{printdemosample.*?end{printdemosample}", block_txt, re.S)
            print ret
            self.fan_in(ret)
        return 0

    def run(self):
        print("GO!")
        for it in self.__input_fn:
            self.extract_demo(it)
# foo()
        print("now, totally %d demo samples" %(len(self.__demo_list)))
        fd = open("./supersentence.tex", "w")
        fd.write(self.__TEMPLATE_TEX)
        for it in self.__demo_list:
            fd.write(it)
        fd.write(self.__TEMPLATE_TEX_END)

        return 0

## Wrapper for a new from scratch feature.
#  It can collect all words from a index file.
class Vocabulary:
    __DEBUG = False
#    __DEBUG = True

    __input_fn = "cards.idx"

    __advanced_list = [
      "hydrogen",
      "inorganic",
      "organic", "oxygen",
    ]

    __mediate_list = [
      "announcement",
      "celebration", "crowded",
      "embarrassed", "exhausted",
      "forever",
      "journalist",
      "similar",
      "tourism",
      "volunteer",
    ]

    __simple_list = [
      "a", "about", "after", "all", "am", "an", "and", "any", "are", "aren't", "as", "ask", "at",
      "bad", "be", "bed", "big", "bird", "book", "box", "boy", "bring", "bus", "but", "busy", "buy", "by",
      "cake", "can", "car", "cat", "clean", "close", "cold", "cool", "come", "cut",
      "dance", "day", "do", "does", "dog", "down", "did", "draw",
      "egg", "every", "English",
      "fast", "father", "find", "fish","five", "fly", "foot", "football", "for", "from",
      "get", "girl", "give",  "go", "good", "green",
      "happy", "hand", "has", "have", "he", "help", "her", "here", "his", "home", "hot", "how",
      "if", "in", "is", "isn't", "it", "I",
      "jump",
      "leg", "let", "lesson", "like", "listen", "little", "look", "long", "Let's",
      "man", "many", "me", "morning", "mother", "my", "must", "Me too", "Miss Thin", "Mr Chan", "Mrs Ship",
      "name", "new", "next", "no", "not",
      "of", "off", "old", "on", "one", "only", "open", "or", "our", "out",
      "pen", "pig", "play", "please", "put",
      "quick", "quickly",
      "read", "red", "right", "run",
      "say", "school", "see", "she", "shopping", "should", "sing", "sister", "sit", "six", "sleep", "slow", "slowly","so", "some", "soon", "stand", "stop", "sun",
      "tell", "than", "that", "the", "there are", "there is", "they", "this", "time", "to", "today", "too", "tooth", "two",
      "up", "us",
      "very",
      "wait", "was", "water", "we", "what", "when", "who", "why", "will", "with", "woman",  "work", "write",
      "yes", "you", "your",
      "zoo"
    ]

    _TEX_TEMPLATE = "\\documentclass[a4paper]{article}\n" \
                    "\\usepackage[margin=2cm]{geometry}\n" \
                    "\\begin{document}\n" \
                    "\\large\n"

    _TEX_TEMPLATE_END = "\\end{document}\n"

    def __init__(self):
        print("default ctr")

    def logout(self, fmt):
        if self.__DEBUG == True:
            print(fmt)

    def set_input(self, input):
        print("customize ctr")
        self.__input_fn = input

    # This is use regexp to extract target words
    def extract(self, linetxt):
        wd = ""

        ret = re.search(r"^\\indexentry{(.*)\|", linetxt)
        if ret != None:
            print("%s === Yes-->%s" %(linetxt, ret.group(1)))
            wd = ret.group(1)
            if wd.startswith("\\glossar"):
                wd = ""

        return wd

    def collect_all_words(self):
        all_lists = []
        fd = open(self.__input_fn)
        line = fd.readline()
        while line:
            w = self.extract(line.strip())
            if w != "":
                all_lists.append(w)
            line = fd.readline()

        fd.close()
        return all_lists

    def preprocess_table(self, fd):
        fd.write("\n\n\\begin{tabular}{|r|l|r|l|r|l|r|l|}\n")
        fd.write("\\hline\n")
        fd.write("{N.O.} & {word} & {N.O.} & {word} & {N.O.} & {word} & {N.O.} & {word}\\\\\n\\hline\n")
        return 0

    def postprocess_table(self, fd):
        fd.write("\\hline\n\\end{tabular}\n")
        return 0

    # put all words in col_num x col_num
    def spread_words(self, data, col_num, fd, index = 0, page_num = 0, page_count = 50, last_one = False):
        #2018-01-06 FIX this BUG!!
        idx = page_num * page_count

        traverse_len = 0

        self.logout("the index=%d" %(idx))
        self.preprocess_table(fd)

        if last_one == True:
            # 2018-01-08 below is rewrite the last index,
            # 180 is hard code, it is not a good code
            idx = page_num * 180
            self.logout("do this for last remaining words..")
            traverse_len = page_count
        else:
            traverse_len = page_count/col_num

        for i in range(0, traverse_len):
            self.logout("processing %d" %(idx + i))
            linefmt = ""
            for j in range(0, col_num):
                if j != 0:
                    linefmt += "&"
                self.logout("word index:%d" %(idx + j))
                if (idx + j) > (len(data) - 1):
                    self.logout("exceed the limit, break")
                    break

                sec = "{" + str(idx + 1 + j) + "} &"
                linefmt += sec

                sec = "{" + data[idx + j] + "}"
                linefmt += sec
            linefmt += "\\\\ \n"

            fd.write(linefmt)

            idx += col_num

        self.postprocess_table(fd)

        return 0

    # dump @data words list into target TeX file
    def dump_into_tex(self, data):
        fd = open("vol.tex", "w")
        fd.write(self._TEX_TEMPLATE)
        pagecount = 180 # NOTE - try separate each in each page

        segs = len(data) / pagecount
        print("There are toally %d segments..." %(segs))

        for i in range(0, segs):
            self.spread_words(data, 4, fd, i*pagecount, i, pagecount)
            index = i*pagecount

        delta = len(data) - segs*pagecount
        self.logout("segs:%d pagecount:%d" %(segs, pagecount))
        self.logout("remaining %d words..." %(delta))
        if delta > 0:
            self.logout("index=%d, page_num=%d" %(segs*pagecount, i + 1))
            self.spread_words(data, 4, fd, segs*pagecount, i + 1, delta, True)


        fd.write(self._TEX_TEMPLATE_END)

        fd.close()
        return 0

    # public entry API
    def run(self):
        word_list = self.collect_all_words()
        print("Totally %d words" %(len(word_list)))
        word_list = list(set(word_list))
        random.shuffle(word_list)
        print("After redundant remove, totally %d words" % (len(word_list)))

        # Next, will remove too easy word, if you like
        if True:
            print("remove easy word, you can set False to get full list")
            print("Totally %d simple words" %(len(self.__simple_list)))

            remove_count = 0;
            remove_list = []
            for it in word_list:
                for i in self.__simple_list:
                    if i == it:
                        remove_count = remove_count + 1
                        #word_list.remove(it)
                        remove_list.append(it)
                        #break
            print("the to delete word:%d" %(len(remove_list)))
            for it in remove_list:
                word_list.remove(it)
            print("After simple elimination, %d words remained(removed %d)\n" %(len(word_list), remove_count))

        self.dump_into_tex(word_list)

        return

# main entry
if __name__ == '__main__':

    yuwenmode = 0
    senmode = 0
    vocabulary = 0

    # if not specified via command line...
    inputtex = 'primary_words.tex'
    yuwentex = 'yuwen.idx'

    try:
        opts,args = getopt.getopt(sys.argv[1:],
                                  "vyhf:s", ["vocabulary","yuwen","help","file=","sentence"])
        for o,a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit(0)
            elif o in ('-y', '--yuwen'):
                yuwenmode = 1
            elif o in ('-s', '--sentence'):
                senmode = 1
            elif o in ('-v', '--vocabulary'):
                print("=====currently, I WILL NOT add words here")
                print("All new words SHOULD put in new cards.tex file!(locked at 461 words)\n\n")

                print("Vocalubary Mode")
                vocabulary = 1

    except getopt.GetoptError:
        print 'exception hanpend in getopt'

    print 'Start extracting Words...'

    wdlist=[]
    if yuwenmode == 1:
        parse_tex(yuwentex, wdlist, yuwenmode)
    elif vocabulary == 1:
        obj = Vocabulary()
        obj.run()
        sys.exit(0) # directly return after finish processing the vocabulary
    elif senmode == 1:
        print("Sentence mode.")
        obj = SuperSentence()
        obj.run()
        sys.exit(0)
    else:
        parse_tex(inputtex, wdlist)

    if glbDbg == 1:
        print 'After parsing, totally %d words found' %(len(wdlist))

    # exclude the redundant items...
    wdlist = list(set(wdlist))
    print 'totally %d exclusive words found' % (len(wdlist))
    # so easy of shuffling the word list!
    random.shuffle(wdlist)

    if yuwenmode == 1:
        float_single_words(wdlist)

    if glbDbg == 1:
        print '==================\nWell, after shuffle, the words are:\n\n'

    if yuwenmode == 1:
        create_print_pdf('a.tex', 'wordstemplates.part', 4, wdlist)
    else:
        create_print_pdf('a.tex', 'eng.wordstemplates.part', 4, wdlist)
