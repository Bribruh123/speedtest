# Netgear Nighthawk Router speedtest monitoring

Python, InfluxDB and Grafana stack for monitoring speeds of a host agent, router and devices in network. 

### Dependencies

- [Docker](https://docs.docker.com/engine/install/)

- [docker compose](https://docs.docker.com/compose/install/linux/)

### Set up and install

1) Clone repository into host enviornment:

   ```
   git clone https://github.com/Bribruh123/speedtest.git
   ```

3) Modify .env file with credentials for Netgear Nighthawk Router:

   ```
   $ cat .env
   ROUTER_USERNAME=insert_username_here
   ROUTER_PASSWORD=insert_password_here
   ```

4) Build and run containers:
   ```
   $ docker compose up
   ```

5) After containers have sucessfully started, access Grafana UI and add data source

   - From a browser load grafana with url of host machine:

     http://[HOST_IP_ADDRESS]:3000/

   - Add InfluxDB data source
     - From welcome screen, select 'Add your first data source':
    
       ![image](https://github.com/Bribruh123/speedtest/assets/87781032/f3b79ce9-8140-4364-b15b-4870e74190f0)

     - Select '+ Add new data source'
     - Select ''Influx DB
     - Insert InfluxDB instance details:
       - HTTP
         - URL: http://influxdb:8086
       - Custom HTTP Headers:
         - Header: 'Authorization'
         - Value: 'Token veryverysecuretoken'
       - InfluxDB Details:
         - Database: 'Logs'
       - Select Save & test
6) Import pre build dashboard from json:
   - Navigate to Dashboards and select 'New' -> 'Import':
  
     ![image](https://github.com/Bribruh123/speedtest/assets/87781032/ca4f3c58-92dc-4aba-9762-0d364f179475)

   - Either upload [grafana_dashboard.json](https://github.com/Bribruh123/speedtest/blob/master/grafana_dashboard.json) or copy its contents into 'Import via pannel Json' field
   - Select previously configured InfluxDB data source in 'InfluxDB' dropdown
   - Select 'Import'

Enjoy!  

