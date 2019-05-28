## ASU Blackboard Scraper

### Stable as of: May 2019

<hr/>

ASU is moving away from blackboard meaning that the students will no longer have access to all their submitted assingments or class materials. ASU suggests that we download and backup these files but us juniors and seniors have taken over 30 courses via Blackboard. Therefore, downloading all these files would probably take around 5 hours...

This scraper was built to address that problem. Blackboard closes on June 30th so I do hope this scraper helps some ASU students! 

**Windows Support Only**

  However, if you know how to run python (pretty simple), you can run the source code (./src) and it should still work. 
  
  Cross-platform is difficult, as ASU does not allow headless-requests, so we have do manually run a chrome app and control it. Therefore, the commands utilized are platform native and may not apply in mac. Please report an issue if any occurs and I will try my best to address your issue.

Running The Scraper
---
1. Download and unzip this file

  ``` 
      git clone https://github.com/justahuman1/Blackboard_scraper.git
  ```
2. Open the ```blackboard_scraper``` folder and go into the ```dist``` folder

  ```
      cd ./blackboard_scraper/dist
  ```
3. Run the ```blackboard_scraper.exe```

  ```
      cmd /K ./blackboard_scraper.exe
  ```
4. The application will now pop-up and ask you for you ASU credentials.



<hr />
**Stack**
* Tkinter
* Selenium
* ActionChains
