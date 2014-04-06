#'Kernel Text Editor' (kte) or 'Katie'
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#usage:
#kte [FILE] [FLAG,optional] [beg:end, optional] "This goes in the file"
#This version was edited 20140330:18.15Z
import sys

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
         self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def getargs():
   beginning = 0
   end = 0
   if (len(sys.argv) >= 3):
      if len(sys.argv) == 3 and sys.argv[2][0] != '[':
         return beginning, end
      elif len(sys.argv) == 4 and sys.argv[3][0] != '[':
         return beginning, end
      elif len(sys.argv) == 3 and sys.argv[2][0] == '[':
         numarg = 2
      else:
         numarg = 3
      for i in sys.argv[numarg][1:]:
         if i >= '0' and i <= '9':
            beginning *= 10;
            beginning += ord(i)-48
         elif i == ':':
            break
         else: #make sure this is right
            print 'Usage: kte [FILE] -flag [BEG:END]'
            sys.exit()
      counter = 0
      for i in sys.argv[numarg][-2::-1]:
         if i >= '0' and i <= '9':
            end += 10**counter*(ord(i)-48)
            counter += 1
         elif i == ':':
            break
         else:
            print 'Usage: kte [FILE] -flag [BEG:END]'
            sys.exit()
   return (beginning, end)

def output(filename,beg = 0, end = 0):#outputs info to the terminal
   try:ourfile = open(filename)
   except: print 'Error openning file: does it exist?'
   counter = 0
   if not beg and not end:
      (beg, end) = getargs()
   for line in ourfile:
      counter +=1
      if (counter >= beg and counter <= end) or (not end and counter >= beg):
         print counter, line,
   ourfile.close()

def append(filename):#adds text to the end of the file
   ourfile = open(filename,'a')
   if len(sys.argv) > 3:#if kte [FILE] 
      if sys.argv[3][0:1] == '-m': #multiline mode
         edit(ourfile)
      elif type(sys.argv[3]) is str:
         ourfile.write(sys.argv[3] + '\n')
      else:
         print "Usage: kte",filename,'-a "Insert this\\n"'
   elif len(sys.argv) == 3:
      ourfile.write(sys.argv[2] + '\n')
   else:
      print "Usage: kte",filename,'-a "Insert this\\n"'
   ourfile.close()
   

def delete(filename, beginning = 0, end = 0): #delets a certain n
   beginning, end = getargs()
   
   if beginning == 0 and end == 0:
      print "Usage: kte", filename, "-d [BEG:END]"
      sys.exit()
   
   try:ourfile = open(filename)
   except: print 'Error openning file: does it exist?'
   contents = ourfile.readlines()
   ourfile.close()
   if end:
      for counter in range(beginning,end):
         contents.pop(counter-1)
      contents.pop(beginning-1)
   ourfile = open(filename,"w")
   contents = "".join(contents)
   ourfile.write(contents)
   ourfile.close()

def insert(filename, beginning = 0, end = 0):
   beginning, end = getargs()
   try:ourfile = open(filename)
   except: 
      print 'Error openning file: does it exist?'
      sys.exit()
   contents = ourfile.readlines()
   ourfile.close()
   
   if(beginning):
      contents.insert(beginning-1, sys.argv[4]+'\n')
   else:
      contents.insert(beginning, sys.argv[4]+'\n')
   
   ourfile = open(filename,"w")
   contents = "".join(contents)
   ourfile.write(contents)
   ourfile.close()

#kte [FILE] -f "Querry"
def find(filename,querry=''):
   if querry == '':
      querry = sys.argv[3]
   try:ourfile = open(filename)
   except: 
      print 'Error openning file: does it exist?'
      sys.exit()
   content = ourfile.read()
   ourfile.close()
   counter = 1
   found = 0
   for i in range(len(content)-len(querry)):
      if content[i] == '\n':
         counter += 1
      if(content[i:i+len(querry)]==querry):
         print 'Querry found at line',counter
         output(filename,counter,counter)
         found = 1
   if not found:
      print 'Querry not found in document.'

def predit(current,counter,cursor):#TODO add escape chars
   print "Use w,a,s,d to navigate, q to quit, e to edit"
   for i in current:
      if cursor[0] != counter:
         print counter, i
      else:
         print counter,
         position = 1
         for j in current[i]:
            if position != cursor[1]:
               print current[i][j],
            else:
               print chr(219),
         position += 1
      counter += 1

#TODO implement 'e', 
def edit(filename,beginning=0, end=0):#edit lines in terminal,below command line
   try:ourfile = open(filename)
   except: print 'Error openning file: does it exist?'
#   import curses as c
#   c.savetty()
   
   if not beg and not end:
      (beg, end) = getargs()
   position = [beg,0]
   subject = []#for aiap, what user is modifying
   
   counter = beg
   for line in ourfile:
      if (counter >= beg and counter <= end) or (not end and counter >= beg):
         subject.append(line)
   
   getch = _Getch()
   while True:
      predit(subject,counter,position)
      ourin = getch()
      if ourin == 'q':
         break
      elif ourin == 'w':
         if position[0] > beg:
            position[0] -= 1
      elif ourin == 'a':
         if position[1] > 0:
            position[1] -= 1
      elif ourin == 's':
         if position[0] < end:
            position[0] += 1
      elif ourin == 'd':
         if position[1] < len(position[0]):
            position[1] += 1
      elif ourin == 'e':
         while True:
            editkey = getchar()
            if editkey == '\n':#ctrl-enter
               break
            if editkey == '\r':
               pass
           #if editkey in letters and numbers
              #insert
           #if
           
            #TODO Insert chars, newline, tab, break statement
      elif ourin not in ['q','e','w','a','s','d']:
         continue
   #TODO insert lines back into file, ask if save, save file
#   for line in ourfile:
#      counter +=1
#      if (counter >= beg and counter <= end) or (not end and counter >= beg):
#         print counter,
#         index = 0
#         for i in line:
#            if index == position[1]
#   while(1):
#      predit(
#   beginning, end = getargs()
#   ourfile = open(filename)
#   ourlines = []
#   for line in ourfile:
#      counter +=1
#      if (counter >= beg and counter <= end) or (not end and counter >= beg):
#         ourlines.append(line)
#   lines = predit(ourlines,beginning)
#   getch() = _Getch
#   while getch() != 27:
#      if

def gui(filename): #opens a tkinter gui for the file
   pass

funcdict = {'-o':output,'-a':append,'-d':delete,'-i':insert,'-f':find,}

if len(sys.argv) == 1:
   print "Usage: kte [FILE] [OPTIONS]j"
   sys.exit()
elif len(sys.argv) == 2:
   output(sys.argv[1])
elif len(sys.argv) == 3 and sys.argv[2] not in funcdict.keys():
   if(sys.argv[2][0] != '['):
      append(sys.argv[1])
   elif(sys.argv[2][0] == '['):
      output(sys.argv[1])
   else:
      print 'Usage: kte [FILE] [OPTIONS]a'
elif len(sys.argv) >= 3 and sys.argv[2] in funcdict.keys():
   funcdict[sys.argv[2]](sys.argv[1])
else:
   print "Usage: kte [FILE] [OPTIONS]i"
