#!/bin/sh

#json file generator for homekit2mqtt

HASS_DIR='../hass'
#mkdir -p -- "$HASS_DIR"
FILE="$HASS_DIR/configuration.yaml"

if [ -z $4 ]; then
    echo "ERR no accessory input"
    exit 1
fi

ACCESSORY='
# Configure a default setup of Home Assistant (frontend, api, etc)
default_config:

# Uncomment this if you are using SSL/TLS, running in Docker container, etc.
# http:
#   base_url: example.duckdns.org:8123

# Text to speech
tts:
  - platform: google_translate

group: !include groups.yaml
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

mqtt:
  broker: "172.17.0.1"
  port: 1883
  birth_message:
    topic: "/hass/status"
    payload: "start"
  will_message:
    topic: "/hass/status"
    payload: "offline"
'
touch $FILE

########## accessories ###########################

lamp() {
LAMP='
light '$1':
  - platform: mqtt
    command_topic: "'$2'"
    state_topic: "'$3'"
    payload_on: "1"
    payload_off: "0"
'
ACCESSORY="$ACCESSORY$LAMP"
sleep .1
}

outlet() {
OUTLET='
switch '$1':
  - platform: mqtt
    command_topic: "'$2'"
    state_topic: "'$3'"
    payload_on: "1"
    payload_off: "0"
'
ACCESSORY="$ACCESSORY$OUTLET"
}

dimm_lamp() {
DIMM_LAMP='
light '$1':
  - platform: mqtt
    #brightness_command_topic: "'$2'"
    #brightness_state_topic: "'$3'"
    #on_command_type: "brightness"
    #brightness_scale: 255
    command_topic: "'$2'"
    state_topic: "'$3'"
    payload_on: "125"
    payload_off: "0"
'
ACCESSORY="$ACCESSORY$DIMM_LAMP"
}

rgb_lamp() {
RGB_LAMP='
'
ACCESSORY="$ACCESSORY$RGB_LAMP"
}

fan() {
FAN='
fan '$1':
  - platform: mqtt
    command_topic: "'$2'"
    state_topic: "'$3'"
    payload_on: "1"
    payload_off: "0"
'
ACCESSORY="$ACCESSORY$FAN"
}

blinds() {
BLINDS='
cover '$1':
  - platform: mqtt
   command_topic: "'$2'"
   state_topic: "'$3'"
'
ACCESSORY="$ACCESSORY$BLINDS"
}

temp() {
TEMP='
sensor:
  - platform: mqtt
    state_topic: "'$3'"
    unit_of_measurement: "°C"
'
ACCESSORY="$ACCESSORY$TEMP"
}

hum() {
HUM='
sensor:
  - platform: mqtt
    state_topic: "'$3'"
    unit_of_measurement: "%"
'
ACCESSORY="$ACCESSORY$HUM"
}

term() {
TERM='
sensor:
  - platform: mqtt
    state_topic: "'$3'"
    unit_of_measurement: "°C"
'
ACCESSORY="$ACCESSORY$TERM"
}

switch() {
SWITCH='
switch '$1':
  - platform: mqtt
    command_topic: "'$2'"
    state_topic: "'$3'"
    payload_on: "1"
    payload_off: "0"
'
ACCESSORY="$ACCESSORY$SWITCH"
}

leak() {
LEAK='
binary_sensor '$1':
  - platform: mqtt
    state_topic: "'$3'"
    payload_on: "1"
    payload_off: "0"
'
ACCESSORY="$ACCESSORY$LEAK"
}

motion() {
MOTION='
binary_sensor '$1':
  - platform: mqtt
    state_topic: "'$3'"
    payload_on: "1"
    payload_off: "0"
'
ACCESSORY="$ACCESSORY$MOTION"
}


###################################################

while $@     # /bin/sh
do
    if [ "$1" != "" ]; then
        echo "create: $1 $2 $3 $4"
        $1 $2 $3 $4
        shift 4
    else
        break
    fi
done

#################################################

echo "$ACCESSORY" > $FILE

LINE=`cat $FILE | wc -l`
echo "line = $LINE in file $FILE"
echo "OK"
exit 0
#cat $FILE



























