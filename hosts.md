# Local Development Host Configuration

For local development of PovoDB, you need to set up your hosts file to map the development domain names to your local machine. This allows you to access the application through the configured domains like `app.povodb.test` instead of using localhost:port.

## Host Entries to Add

Add the following lines to your hosts file:

```
127.0.0.1 app.povodb.test
127.0.0.1 api.povodb.test
127.0.0.1 db.povodb.test
```

## Instructions by Operating System

### Windows

1. Open Notepad as Administrator (right-click Notepad and select "Run as administrator")
2. Open the file: `C:\Windows\System32\drivers\etc\hosts`
3. Add the lines from above at the end of the file
4. Save the file

### macOS / Linux

1. Open Terminal
2. Edit the hosts file with your preferred editor (needs sudo):
   ```
   sudo nano /etc/hosts
   ```
3. Add the lines from above at the end of the file
4. Save the file:
   - For nano: Press Ctrl+O, then Enter to save, and Ctrl+X to exit
   - For vim: Press Esc, then type `:wq` and press Enter

## Verifying the Configuration

After adding the hosts entries and starting the Docker containers:

1. Open your browser and navigate to http://app.povodb.test
2. You should see the PovoDB frontend application
3. Visit http://api.povodb.test/api/v1/docs to see the API documentation

If these URLs don't work, please check:
- The Docker containers are running (`docker-compose up`)
- You've properly added the hosts entries
- You've restarted your browser (sometimes needed to clear DNS cache)

## Troubleshooting

If you're having issues:

1. Try flushing your DNS cache:
   - Windows: `ipconfig /flushdns` in Command Prompt as Administrator
   - macOS: `sudo killall -HUP mDNSResponder` in Terminal
   - Linux: Depends on your distribution, often `sudo systemd-resolve --flush-caches`

2. Ensure you didn't make a typo in the hosts file

3. Make sure the NGINX container is running and properly configured