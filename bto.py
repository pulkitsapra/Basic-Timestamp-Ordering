# Pulkit Sapra, B15123 *
# Jonty Purbia
# Avnish Kumar
# Pramod Jonwal
# Group- 4 , Basic Timestamp Ordering

from random import randint, choice
from optparse import OptionParser

# argument parsing
parser = OptionParser()
parser.add_option("-x", dest="ntx", default="1")
parser.add_option("-i", dest="nint", default="1")
parser.add_option("-t", dest="ntime", default="5")
parser.add_option("-v", "--nvar", dest="nvar", default="3")
options, parser = parser.parse_args()

# parameters
ntx = int(options.ntx)
nint = int(options.nint)
ntime = int(options.ntime)
nvar = int(options.nvar)

operations = ['W', 'R']

print(ntx)
d={}
for i in range(ntx):
	d["T{0}".format(i)]=[]

OP=[]

###############################

# initialize all variables to 0
val =[]

for i in range(nvar):
	val.append(-1)
###############################

# Creating a transaction table

# Name of transaction | Operation |  variable on which operation performed | new value of variable in case of write (if read this column isn't there) | time of occurance of a transaction | status of transaction (active = 1 , inactive/aborted = -1)

# Transaction Timestamps

Tx_TS = [-1]*ntx

#Randomly generating Transactions

for i in range(ntime):
	j = randint(0,ntx-1)
	desctx=[]
	desctx.append(j)
	if(Tx_TS[j]== -1):
		Tx_TS[j]=i
	operat = choice(operations)
	desctx.append(operat)
	var =randint(0,nvar-1)
	desctx.append(var)
	if operat == 'W':
		print "Timestamp : {0}".format(i)
		print "Variable: {0}".format(var)
		data= input("For transaction T{0} , Enter the value you want to write : ".format(j))
		desctx.append(data)
	desctx.append(i)
	d["T{0}".format(j)].append(desctx)
	desctx.append(1)
	OP.append(desctx)

print OP
print Tx_TS

#Some specific Transactions : same as specified in readme

#Eg-1 in Readme

# OP=[[1, 'W', 0, 6, 0, 1], [0, 'W', 0, 4, 1, 1], [1, 'R', 0, 2, 1], [0, 'W', 0, 3, 3, 1], [1, 'W', 0, 7, 4, 1]]
# Tx_TS[0]=1
# Tx_TS[1]=0
# nvar=1

#Eg-2 in Readme

# OP =[[1, 'W', 1, 5, 0, 1], [1, 'R', 1, 1, 1], [1, 'R', 0, 2, 1], [0, 'W', 0, 4, 3, 1], [1, 'R', 1, 4, 1]]
# Tx_TS[0]=3
# Tx_TS[1]=0
# nvar=2

# Another Sample example

# OP = [[0, 'W', 1, 6, 0, 1], [0, 'R', 0, 1, 1], [1, 'R', 1, 2, 1], [1, 'W', 0, 4, 3, 1], [0, 'R', 0, 4, 1]]
# Tx_TS[0]=0
# Tx_TS[1]=2
# nvar =2

# Intitalizing Read And Write timestamp values

ReadTS=[]
WriteTS=[]

for i in range(nvar):
	ReadTS.append(-1);
	WriteTS.append(-1);


# Performing basic timestamp ordering
i=0
while i < len(OP):
	print "i={0}".format(i)
	transc = OP[i][0]
	if OP[i][1]=='R' and OP[i][4]!=-1:
		if(WriteTS[OP[i][2]] > Tx_TS[transc]):
			#abort and rollback
			print "aborting.. Transaction T{0} and restoring \n".format(OP[i][0]) 
			tno = OP[i][0]
			varw = [-1]*nvar
			varr = [-1]*nvar
			for index in range(len(OP)):
				# Invalidating the transacation
				if(OP[index][0]==tno):
					if(OP[index][1]=='R'):
						OP[index][4]=-1
					else:
						OP[index][5]=-1

			ReadTS = [-1]*nvar
			WriteTS = [-1]*nvar	

			for index in range(Tx_TS[tno]-1,-1,-1):
				if OP[index][1]=='W' and varw[OP[index][2]]==-1:
					varw[OP[index][2]]=OP[index][3]
					WriteTS[OP[index][2]]=Tx_TS[OP[index][0]]
				elif OP[index][1]=='R' and varr[OP[index][2]]==-1:
					ReadTS[OP[index][2]]=Tx_TS[OP[index][0]]
					varr[OP[index][2]]=1
			val = varw
			i=Tx_TS[tno]-1
			


		else:
			print " Reading value of variable {0} as {1} by T{2}\n".format(OP[i][2],val[OP[i][2]], OP[i][0])
			ReadTS[OP[i][2]] = Tx_TS[transc]
			
	
	elif OP[i][1]=='W' and OP[i][5]!=-1:
		if WriteTS[OP[i][2]] > Tx_TS[transc]  or ReadTS[OP[i][2]] > Tx_TS[transc]:
			#abort and rollback
			print "aborting.. Transaction T{0} and restoring \n".format(OP[i][0]) 
			tno = OP[i][0]
			# val = [0]*nvar
			OPnew=[]
			

			varw = [-1]*nvar
			varr = [-1]*nvar
			for index in range(len(OP)):
				# Invalidating the transacation
				if(OP[index][0]==tno):
					if(OP[index][1]=='R'):
						OP[index][4]=-1
					else:
						OP[index][5]=-1

			ReadTS = [-1]*nvar
			WriteTS = [-1]*nvar	


			for index in range(Tx_TS[tno]-1,-1,-1) :
				if OP[index][1]=='W' and varw[OP[index][2]]==-1:
					varw[OP[index][2]]=OP[index][3]
					WriteTS[OP[index][2]]=Tx_TS[OP[index][0]]
				elif OP[index][1]=='R' and varr[OP[index][2]]==-1:
					ReadTS[OP[index][2]]=Tx_TS[OP[index][0]]
					varr[OP[index][2]]=1


			val = varw
 			i=Tx_TS[tno]-1
		else:
			print " Writing value of variable {0} as {1} by T{2}\n".format(OP[i][2],OP[i][3],OP[i][0])
			val[OP[i][2]]= OP[i][3]
			WriteTS[OP[i][2]] = Tx_TS[transc]
	i = i+1
			
print val



	