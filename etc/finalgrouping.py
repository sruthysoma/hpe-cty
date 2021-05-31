import re
string="""10.1.18228.8176
26.20.100.7925
26.20.100.7870
2.30 (Windows 10)
2.30 (Microsoft Windows 2019)
2.30 (Microsoft Windows 2016)
2.12.0.0
4.6.0.0
1.0.0.0
10.1.18
1.0.0.0
1.2.126.843
26.20.100.7925
8.1 15.45.31.5127
26.20.100.8141
16.8.3.1003
14.8.16.1063"""

pattern="[0-9]+\.[0-9]+"

groups =[]
def group(string):
    #print(string)
    if len(groups)==0:
      groups.append([string])
      return     
    
    else:
            matched=re.search(pattern,string)
            if(bool(matched)==0):
              return
            else:
              pat=matched.group(0)
              #print("AAAAA.",pat) 
              pat=pat.replace('.', '\.')             
              for i in range(len(groups)):       
                check=re.search( pat, groups[i][0])
                #print(groups[i][0],pat)
                if(bool(check)==1):
                  #print("BBBBB.",pat,string,check.group(0))
                  groups[i].append(string)
                  return 
              groups.append([string])
                  

               


T = [t.strip() for t in string.split("\n") if t]

for i in T:
    group(i)
print(groups)


#--------------------------------------------------------------------------------------------------------------------#

# groups =[]
# def group(string):
#     if len(groups)==0:
#       groups.append([string])
#       return     
    
#     else:
#         for i in groups:
#             small=len(i[0])>len(string)
#             if small==True:
#               val=len(string)
#             else:
#               val=len(i[0])
#             for j in range(val):
#                 num=0
#                 if i[0][j]==string[j]:
#                     if(string[j]=="."):
#                         num+=1
#                 #print(string,num)
#             if(num==2):
#                 i.append(string)
#                 break
#             else:
#                groups.append([string])
               


# T = [t.strip() for t in string.split("\n") if t]

# for i in T:
#     group(i)
# print(groups)
