#!/bin/bash
#https://wiki.archlinux.org/index.php/Yakuake#dbus-send_instead_of_qdbus
func_result=""

function instruct {
    cmd="qdbus org.kde.yakuake $1"
    #eval $cmd &> /dev/null
    func_result="$(eval $cmd)"
    sleep 0.5
}

# (name)
function createSession {
	echo "Adding session $1"
	instruct "/yakuake/sessions org.kde.yakuake.addSession"
	instruct "/yakuake/tabs org.kde.yakuake.setTabTitle $func_result $1"
}

# (sessionName, command)
function sendCommand {
	echo "Sending command to $1: $2"
	instruct "/yakuake/sessions runCommandInTerminal $1 '$2'"
}

function splitSessionHorizontally {
	newid=qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.splitTerminalLeftRight $1
}

function splitSessionVertically {
	newid=qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.splitTerminalTopBottom $1
}