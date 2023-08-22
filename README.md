# Netgear Nighthawk Router speedtest monitoring

Python, InfluxDB and Grafana stack for monitoring speeds of a host agent, router and devices in network. 


![image](https://github.com/Bribruh123/speedtest/assets/87781032/3595edac-eec5-4bb3-a2ae-1827a84373f4)

### Dependencies

- [Docker](https://docs.docker.com/engine/install/)

- [docker compose](https://docs.docker.com/compose/install/linux/)

- Enable QoS on Netgear Nighthawk router:
   - From a browser, login to https://routerlogin.net/
   - Navigate to 'Quality of Service' tab:
 
      ![image](https://github.com/Bribruh123/speedtest/assets/87781032/1db24253-bf86-42d2-b1e1-688e867fe106)

   - Select 'Enable Qos' and 'Automatically update performance optimization database':

     ![image](https://github.com/Bribruh123/speedtest/assets/87781032/21600324-26a9-4977-8352-b7df3858851b)
     ![image](https://github.com/Bribruh123/speedtest/assets/87781032/93769bd1-0d51-4b15-871e-bfd597a63c06)

   - Select 'Apply' and logout of router



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

5) (Optional) Import pre-built dashboard from json:
   - Navigate to Dashboards and select 'New' -> 'Import':
  
     ![image](https://github.com/Bribruh123/speedtest/assets/87781032/92626276-aab5-40fc-a753-cae308f62019)


   - Either upload [grafana_dashboard.json](https://github.com/Bribruh123/speedtest/blob/master/grafana_dashboard.json) or copy its contents into 'Import via pannel Json' field
   - Select pre-configured InfluxDB data source in 'InfluxDB' dropdown
   - Select 'Import'

#### Enjoy!



