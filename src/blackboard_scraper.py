from win32.win32process import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import(
    NoSuchElementException, NoSuchWindowException)
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import time
import os
import re
import sys

ignore_links = [
   r'discussion',
   r'video',
   r'.mov'
]
accepted_files = [
    r'pdf',
    r'powerpoint',
    r'ppt',
    r'txt',
    r'xlsx',
    r'file',
    r'excel',
    r'handout',
    r'review',
    r'sas',
    r'py',
    r'java',
    r'cc',
    r'cpp',
    r'slides',
    r'chapter'
]
# Elements added to adhere to robots.txt
left_window_ign = [
    r'policy',
    r'library',
    r'technical',
    r'accessibility',
    r'calendar',
    r'contribution',
    r'syllabus',
    r'carey',
    r'announcements'
    r'troubleshoot',
    r'tools',
    r'discussion',
    r'announcements',
    r'faculty'
]


class DriverManager:
    def __init__(self, username, password, grades_only, classes_to_scrape):
        self._u = username
        self._p = password
        self.driver = None
        self.msg_transferer = None
        self.grades_only = grades_only
        self.classes_to_scrape = str(classes_to_scrape)

    def _msgPrint(self, txt='', original_msg_obj=None):
        if original_msg_obj:
            self.msg_transferer = original_msg_obj
        else:
            self.msg_transferer.configure(text=txt)

    def _normalizer(self, saved_url):
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        while str(self.driver.title).lower() != saved_url:
            time.sleep(1)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.find_elements_by_tag_name('body')[0].click()
        time.sleep(1)

    def tabNormalize(self, saved_url):
        try:
            self._normalizer(saved_url)
        except NoSuchWindowException:
            time.sleep(3)
            self._normalizer(saved_url)

    def postOrder_dirScan(self, root):
        time.sleep(3)
        try:
            main_content = self.driver.find_element_by_id('content')
        except NoSuchElementException:
            pass
        all_links = main_content.find_elements_by_tag_name('a')
        _lastpage_check = str(self.driver.title).lower()
        for link in all_links:
            _f_link = str(link.text).lower()
            _f_href = str(link.get_attribute("href"))
            actions = ActionChains(self.driver)
            if(  # found a downloadable file
                (bool(re.search('|'.join(accepted_files), _f_link)) or
                    'bbcswebdav' in _f_href) and
                (_f_link != '') and
                (not bool(re.search('|'.join(ignore_links), _f_link))) and
                ((link.get_attribute("onclick") is None) or
                    str(link.get_attribute("onclick")).find(
                        'file') > -1) and
                _f_link.find('.com') == -1
            ):
                (actions
                    .key_down(Keys.CONTROL)
                    .click(link)
                    .key_up(Keys.CONTROL).perform())
                time.sleep(4)
            elif(  # found a sub folder (recurse)
                bool(re.search(r'webapps/blackboard/content', _f_href)) and
                _f_link != ''
            ):
                root_dir = str(self.driver.title).lower()
                (actions
                    .key_down(Keys.CONTROL)
                    .click(link)
                    .key_up(Keys.CONTROL).perform())
                time.sleep(3)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.postOrder_dirScan(root_dir)
                self.tabNormalize(root_dir)
        self.driver.close()
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def grade_handler(self):
        time.sleep(3)
        grade_bin = self.driver.find_element_by_id('grades_wrapper')
        _exempt = [r'quiz', r'exam', r'test']
        graded_links = grade_bin.find_elements_by_tag_name('a')
        link_names = [i.text for i in graded_links]
        fil_tests = [
            i for i, x in enumerate(link_names)
            if not bool(re.search('|'.join(_exempt), x)) and
            x != ''
        ]
        num_assigns = len(fil_tests)
        _i = 0
        while _i < num_assigns:
            cur_bin = self.driver.find_element_by_id('grades_wrapper')
            sub_links = cur_bin.find_elements_by_tag_name('a')
            proper_i = fil_tests[_i]
            sub_links[proper_i].click()
            time.sleep(3)
            downloads = self.driver.find_elements_by_class_name('dwnldBtn')
            for d_href in downloads:
                d_href.click()
                time.sleep(1)
            self.driver.execute_script("window.history.go(-1)")
            _i += 1
            time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(3)

    def class_content(self):
        time.sleep(3)
        nav_bar = self.driver.find_element_by_class_name('navPaletteContent')
        weeks = nav_bar.find_elements_by_tag_name('li')
        if self.grades_only:
            hrefs = [str(week.text).lower() for week in weeks]
            grade_href = (
                [i for i, href in enumerate(hrefs)
                    if bool(re.search('grade', href))])
            grades = weeks[grade_href[0]].find_element_by_tag_name('a')
            actions = ActionChains(self.driver)
            (actions.key_down(Keys.CONTROL)
                    .click(grades)
                    .key_up(Keys.CONTROL).perform())
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.grade_handler()
            messagebox.showinfo(
                'Grades Completed!', 'You may now close all windows.')
            driver.quit()

        fixed_amt = [i for i, week in enumerate(weeks) if not bool(
                        re.search('|'.join(
                            left_window_ign), str(week.text).lower()))]
        pages_to_hit = len(fixed_amt) - 1
        i = 0
        while i <= pages_to_hit:
            fixed_i = fixed_amt[i]
            try:
                href = weeks[fixed_i].find_element_by_tag_name('a')
            except NoSuchElementException:
                i += 1
                continue
            _f_string = str(href.text).lower()
            _last_sub_left_menu = (
                    str(self.driver.title).lower())
            actions = ActionChains(self.driver)
            (actions.key_down(Keys.CONTROL)
                    .click(href)
                    .key_up(Keys.CONTROL).perform())
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            if _f_string.find('grade') > -1:
                self._msgPrint("Scraping Grades!")
                self.grade_handler()
            else:
                self.postOrder_dirScan(_last_sub_left_menu)
                self.tabNormalize(_last_sub_left_menu)
            self._msgPrint(f"Scraped {_f_string}")
            i += 1
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()

    def search_each_class(self, courses):
        all_classes_location = str(self.driver.title).lower()
        # early error warning due to tkinter mainloop thread
        _v_node = False
        for i, class_elem in enumerate(courses):
            self.driver.switch_to.window(self.driver.window_handles[0])
            if bool(re.search(self.classes_to_scrape, class_elem.text)):
                _v_node = True
                self._msgPrint(f"Scraping Class:\n{str(class_elem.text)[:7]}")
                actions = ActionChains(self.driver)
                (actions
                    .key_down(Keys.CONTROL)
                    .click(class_elem)
                    .key_up(Keys.CONTROL).perform())
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.class_content()
                self.tabNormalize(all_classes_location)
                self._msgPrint("Scraping Class Successful!")
            elif (i == (len(courses)-1)) and not _v_node:
                messagebox.showerror(
                    "Error", "No classes found..")
                self.driver.quit()
                return None
        self.driver.close()
        messagebox.showinfo(
            'Scrape Completed!', 'You may now close all windows.')

    def start_driver(self):
        global g_messenger
        self._msgPrint(original_msg_obj=g_messenger)
        chrome_profile = Options()
        # create a folder for each class download (if not exists)
        new_folder_name = f'{self.classes_to_scrape}_downloads'
        downloads_dir = os.path.join(
            os.getcwd(),
            new_folder_name
        )
        if not os.path.exists(downloads_dir):
            os.mkdir(new_folder_name)
        profile = {
            "download.default_directory": downloads_dir,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        if getattr(sys, 'frozen', False):
            driver_path = os.path.join(sys._MEIPASS, 'chromedriver.exe')
        else:
            driver_path = 'chromedriver.exe'
        chrome_profile.add_experimental_option("prefs", profile)
        self._msgPrint("Driver Initialized!")
        self.driver = webdriver.Chrome(
            executable_path=driver_path,
            options=chrome_profile
        )
        self.driver.get('https://myasucourses.asu.edu/')
        self._msgPrint("Going to Blackboard..")
        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")
        username.send_keys(self._u)
        password.send_keys(self._p)
        self.driver.find_element_by_class_name('submit').click()
        time.sleep(3)
        self.driver.get(
            # INSERT BLACKBOARD URL HERE
        )
        time.sleep(3)
        try:
            parent_div = self.driver.find_element_by_id(
                '_27_1termCourses_noterm')
        except NoSuchElementException:
            messagebox.showerror(
                "Login Failed", "Please try again with proper credentials.")
            quit()
        li_elements = parent_div.find_elements_by_tag_name("li")
        self.search_each_class(li_elements)


class GUI:
    def __init__(self, *args, **kwargs):
        self.window = Tk()
        self.window.title("Blackboard Scraper")
        self.window.geometry('275x230')
        self.form_labels = ['Username', 'Password', 'Class Number']
        self.form_objects = {}
        self.grades_only = None

    def cred_submit(self):
        global g_messenger
        g_messenger.configure(text="Driver Starting..")
        _u = self.form_labels[0]
        _p = self.form_labels[1]
        _cl = self.form_labels[2]
        my_u = self.form_objects[_u]['input'].get()
        my_p = self.form_objects[_p]['input'].get()
        my_cl = self.form_objects[_cl]['input'].get()
        grades_res = self.grades_only.get()
        main_runner = DriverManager(my_u, my_p, grades_res, my_cl)
        scanner = threading.Thread(target=main_runner.start_driver)
        try:
            # main_runner.start_driver(g_messenger)
            scanner.start()
        except:
            messagebox.showerror(
                "System Error", "Closing all threads..")
            quit()

    def init_creator(self):
        global g_messenger
        col = 0
        rows = len(self.form_labels)
        for i, elem in enumerate(self.form_labels):
            ceiling = 5
            if i == 0:
                ceiling = 20
            self.form_objects[elem] = {'label': None, 'input': None}
            a = Label(self.window, text=elem)
            a.grid(row=i, column=col, pady=(ceiling, 0), padx=(20, 20))
            self.form_objects[elem]['label'] = a
        col += 1
        for i, elem in enumerate(self.form_labels):
            _s = ''
            if elem.find('Pass') > -1:
                _s = '*'
            e = Entry(self.window, show=_s)
            e.grid(row=i, column=col)
            self.form_objects[elem]['input'] = e
        self.grades_only = IntVar()
        grades_check = Checkbutton(
            self.window, text="Grades Only?", variable=self.grades_only
        )
        grades_check.grid(row=rows+1, column=0, pady=(10, 0))
        submit_row = rows + 2
        submitButton = (ttk.Button(
            self.window, text="Start Scraper", command=self.cred_submit))
        submitButton.grid(row=submit_row, column=1, pady=(5, 20))
        updater = Label(self.window, text=elem)
        g_messenger = Label(self.window, text='')
        g_messenger.grid(
            row=submit_row+1, column=0, pady=(0, 0), padx=(20, 0))
        self.window.mainloop()

# global messenger required due  to threading
g_messenger = None
interface = GUI()
interface.init_creator()
