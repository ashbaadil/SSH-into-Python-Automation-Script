import paramiko
import logging
import os
import shutil
import re
import sys
import time
import datetime
import timeit
from tqdm import tqdm


IPS = []
#os.system('cls')

myarr= []


errorcount=[]



data=[]
timestamp=time.strftime("%Y%m%d-%H%M%S")
count=0

print("Hello, Welcome! :)  ")
print ( "            ")

print("Please make sure that you have saved a copy of your file with the following ip's you want to print data from in the same directory as this file.Each IP must take up only ONE line.")
file=input("Please input the name of the file with all your IP Addresses")

directory=input("Where would you like to store your files today? Please type in your directory path name . " )
username=input("Please input the username for you SSH Client.")
password=input("Please input the password for your SSH Client.")

print("  ")



noip= sum(1 for line in open(file))

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())



command=input( "Please Enter all commands you want to input, seperated by a comma.Once you have finished, press enter. For example: \"xStatus,xconfig \" ."  +  "    ")

commands=command.split(",")


#take each line in ip.txt which is an ip address and input it. 
#for loop will repeat and print out each ip address's xstatus and xconfig and store it in a new file each time 



loop= tqdm(total= noip , position=0, leave=False)

for i, line in enumerate(open(file)):
    
    


    line=line.strip()

    try:

        client.connect(hostname=line, username, password)
        print('trying to connect')
        print ("Connecting to server... " + line)
        logging.info('Connecting to server...')
        

    except Exception as e:
        
        print('Connection Failed')

        

        t=str(e)
        myarr.append(t)
        print("Codec with an Error:" + line + "    " +  " \n"+ t)
        count= count + 1
        countt=str(count)
        errorcount.append(countt)
        print("Currently, there are:" + " " +  countt  + " " + "codecs with errors")
        if not os.path.exists('Errors'):
            os.makedirs('Errors')
            newFile=open(directory+"\\Errors\\ErrorFile.txt", "a")
            newFile.write( "\n" + "\n" + "\n" + timestamp + "\n" + "Codec with an Error:" + line  + "    "  + " \n" +  t + "  " + " \n" + "Currently, there are:" +  "\n".join(errorcount[-1])  + "devices with errors")
            newFile.close()
            
        else:
             
            newFile=open(directory+"\\Errors\\ErrorFile.txt", "a")
            newFile.write( "\n" + "\n" + "\n" + timestamp + "\n" + "Device with an Error:" + line  + "    "  + " \n" +  t + "  " + " \n" + "Currently, there are:" +  "\n".join(errorcount[-1])  + "devices with errors")
            newFile.close()
           
        progress=str((i+1)/noip *100)
        print("PROGRESS:")
        print( progress + "%" + " " + " devices have been read" )
        
        print("   " )
    
        loop.set_description("You have finished..".format(i))
        loop.update()
    
        print( " ", end='\r')
      
 
        continue



    print('connected to' +  " " + line  )

   
    for x in commands:
   
    
        print('shell invoked')

        shell = client.invoke_shell()
        shell.recv(1024)
        time.sleep(2)
        shell.send( x + " \n")
        time.sleep(2)
        output = (shell.recv(65535))
        output=output.decode("utf-8")
        output1 = str(output)
        data.append(output1)
        
        print(output1)
       
      
  
    client.close()
        

    
    print("     " )
    


    if not os.path.exists('Data'):
        
        os.makedirs('Data')
        newFile=open(directory+"\\Data\\" + line + '_'+ timestamp  + "_" + '.txt', "a")
       
        newFile.write( line + "\n" + "\n".join(data))
        newFile.close
           
      
    else:
         
        newFile=open(directory+ "\\Data\\" + line + '_'+ timestamp  + "_" + '.txt', "a")
       
        newFile.write( line + "\n" + "\n".join(data))
        newFile.close
    

   
   
    progress=str((i+1)/noip *100)

    print("PROGRESS:")
    print( progress + "%" + " " + " devices have been read" )
    
    
    
    print("   " )
    
  
    print("  ") 
    
    loop.set_description("You have finished..".format(i))
    loop.update()
    
    print( " ", end='\r')   

    app=str(timeit.timeit('"_".join(str(n) for n in range(100))',number=1000))
    
    print("The current running time is:" + app)




print(" You are now done! ") 
