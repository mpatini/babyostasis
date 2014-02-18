babyostasis
===========
Hack for 2014 Spring PennApps. Using a Lilypad Arduino and a temperature sensor, and an electric imp, we configued
the Lilypad to relay temperature information to the electric imp, the imp to upload that info to a server in json
format, and the server (source code here) to read that json and, if the temperature went above a certain threshhold,
use the twilio and sendgrid apis to text and email the parent.
