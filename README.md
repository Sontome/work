copy user chrome thay <User>



---------------------------------    
robocopy "C:\Users\devil\AppData\Local\Google\Chrome\User Data\Default" "C:\clone_profile" /E

  -------    

"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\clone_profile"
