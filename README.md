## ASU Blackboard Scraper

### Stable as of: May 2019

<img src="https://i.imgur.com/9ckRlex.gif" />

<hr/>

ASU is moving away from blackboard meaning that the students will no longer have access to all their submitted assingments or class materials. ASU suggests that we download and backup these files but us juniors and seniors have taken over 30 courses via Blackboard. Therefore, manually downloading all these files would probably take around 5 hours...

This scraper was built to address that problem. Blackboard closes on June 30th so I do hope this scraper helps some ASU students! 

Requirements
---
- Windows OS
- Latest version of Chrome (v74.*)

Running The Scraper
---
1. Download and unzip this file

  ``` 
  git clone https://github.com/justahuman1/Blackboard_scraper.git
  ```
2. Open the ```blackboard_scraper``` folder and navigate into the ```dist``` folder

  ```
  cd ./blackboard_scraper/dist
  ```
3. Run the ```blackboard_scraper.exe```

  ```
  cmd /K ./blackboard_scraper.exe
  ```
4. The application will now pop-up and ask you for you ASU credentials.

<img src="https://i.imgur.com/c1Sv1Z6.jpg" />

5. Enter your asurite username and password. The class number field takes a class number. The grades only option will allow you to only download your submitted assignments in the 'My Grades' tabs. 

Ex:

    Username: asu_user
    Password: ********
    Class Number: 415 
    Grades Only: *checked*

> NOTE: if you have multiple classes with the same number, specify the three digit class name as well, "CLS 300"

6. Click Start to run the program. Do not mess with the running instance (or it will break).
  

**Windows Support Only**

However, if you know how to run a Python file, you can run and modify the source code ```(./src)```. 
  
Cross-platform is difficult, as ASU does not allow headless-requests, so we have to manually run a chrome instance and control it. Therefore, the commands utilized are platform native and may not apply on a mac. Please report an issue if any occurs and I will try my best to address it.


Developer Notes
---
This scraper utilities a depth first search method to recursively visit all nodes. Headless requests did not work and we cannot query for pdf files before visitng that folder, so DFS was the optimal approach. As a result, the scraper will take a while.

If you know Python, feel free to modify the source code to refine the file types and other options.

Advice: take a break during the scraping and let the scraper finish before using your computer (~10 minutes / class).

Via the scraper, I have downloaded 2 GB of school assignments and PDFs within an hour. 

Tested with 3 accounts, each in different ASU schools. 


<hr />

**Stack**

* Tkinter
* Selenium
* ActionChains
