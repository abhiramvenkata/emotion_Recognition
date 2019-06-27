to execute emotion recogniion

enter 
cd emotion
python emotions.py


too run arduino code connect sensors and upload arduinosensor code into aurduino 
and connect it to the pi

and enter dev/tty* in the terminal

a line similar to
/dev/ttyACM0
/dev/ttyACM1
appears 

copy the line and paste it in the publish code on line 5

Sign in to aws

select aws iot
select test
enter 'thing01/data' in the subscribe section press subscribe

run the publish code to see relay of sensor data

 
