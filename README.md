# ICP Monitor
![image](https://github.com/Fruityski/Live-Power-Usage/assets/41670430/384a4175-4435-466e-b313-9c23da806927)

1) Power Meter Pulse Sensor
      1. Photo Diode Sense
` Wiring Diagram` 
<img src="https://github.com/Fruityski/Live-Power-Usage/assets/41670430/d68ee431-63c7-48d2-968a-858c21b49a52" width="500" height="390">

In this diagram I have a `393 light sensor` wired up to the `ESP8266` 

      2. ESP 8266, running ESP Easy.
`<Install ESP EASY on Node MCU>`
1. firmware: ESP_Easy_mega_20230623_normal_ESP8266_4M1M.bin

<img src="https://github.com/Fruityski/Live-Power-Usage/assets/41670430/86577574-6274-4622-a10b-48a41db84859" width="900" height="390">


 
      1. `         • Generic - Pulse counter`
      1. `          • GPIO ← Pulse`
      1. `          • Delta`
      1. `          • Change`
      1. `         • Interval 60 Seconds.`

   ` <Insert>`


----
2. MySQL 

#### MySQL Container. 
`docker run --name MySQL -p 3306:3306 -p 33060:33060 -v /root/mysql:/var/lib/mysql -e MYSQL_ROOT_HOST=% --restart=unless-stopped -e MYSQL_ROOT_PASSWORD=some-password-d mysql`

#### Phpmyadmin Container.
`docker run --name phpmyadmin --restart=unless-stopped -e UPLOAD_LIMIT=990M -d -p 8080:80 -e PMA_HOST=192.168.1.155 phpmyadmin/phpmyadmin`


###### Note: you could do this all on a Raspberry Pi without the Node MCU, but these are just my instructions. 
----
3) Python Script
      1. Works by pulling the data from the JSON
      2. Then it puts the data into MySQL. 
      3. Needs to be triggered where that is by Cron or Node-Red etc. 
----
4) Grafana **
    1. `<can be a docker container on a Raspberry Pi>`
    2. `<Insert container instructions/ compose file>`
    3. Connect to MySQL DB. 
    4. Create a Graph. `




















