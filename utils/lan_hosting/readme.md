
# Generate the CA and Server Keys / Certs for LAN Hosting

## Create the CA Keys / Certs
```sh
openssl genrsa -out cave-root-ca.key.pem 4096
openssl req -x509 -new -nodes -key cave-root-ca.key.pem -sha256 -days 4096 -out cave-root-ca.crt.pem
```

## Create the Server Keys / Certs
```sh
openssl genrsa -out cave-server.key.pem 2048
openssl req -new -key cave-server.key.pem -out cave-server.csr.pem
```

## Create an acceptable IP Range:
- Modify `cave-server.ext`
- Note: CIDR Ranges / wildcards are not accepted, so each IP must be manually added.
- Note: Using wildcards with DNS lookups are supported if DNS is used.

## Create the Server Cert
```sh
openssl x509 -req \
  -in cave-server.csr.pem \
  -CA cave-root-ca.crt.pem -CAkey cave-root-ca.key.pem -CAcreateserial \
  -out cave-server.crt.pem -days 4096 -sha256 -extfile cave-server.ext
```


# Project Server Configuration

## Update the NGINX Config
Modify `utils/nginx_ssl.conf.template`:
```
server {
    listen 8000 ssl;
    listen [::]:8000 ssl http2;
    server_name localhost;
    ssl_certificate /certs/cave-server.crt.pem;
    ssl_certificate_key /certs/cave-server.key.pem;

    location / {
        proxy_pass http://${CAVE_HOST}:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

## Copy over needed files
Copy the `cave-server.crt.pem` and `cave-server.key.pem` to the `/utils/lan_hosting/` directory.
- Note this direcotry is added to the docker instance as `/certs/` with the `cave_cli`

## Run the Server on your IP address
```sh
cave run 192.168.1.10:8000
```
- Note: Substitute your desired IP and Ports


# Client Machine Configuration

## On MacOS
- Open Keychain Access
- Open the System Keychain
- Drag the cave-root-ca.crt.pem file into the System Keychain
- Double click the certificate (Named: MIT CAVE CTL)
- Expand the Trust section
- Set "When using this certificate" to "Always Trust"
- Close the window and enter your password to save the changes
- Open the website to verify that no security warnings are present

## On Windows
- Open the Microsoft Management Console (MMC)
   - `mmc.exe`
- Add the Certificates snap-in for the Local Computer account
   - File > Add/Remove Snap-in...
   - Select "Certificates" and click "Add"
   - Choose "Computer account" and click "Next"
   - Select "Local computer" and click "Finish"
- Click "OK" to close the Add/Remove Snap-in window
- Expand the "Certificates (Local Computer)" node
- Right-click on the "Trusted Root Certification Authorities" folder
- Select "All Tasks" > "Import..."
- Follow the Certificate Import Wizard
   - Select the cave-root-ca.crt.pem file
   - Choose "Place all certificates in the following store" and select "Trusted Root Certification Authorities"
   - Complete the wizard
- Restart your browser
- Open the website to verify that no security warnings are present

