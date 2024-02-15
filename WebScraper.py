from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import relative_locator as RL
from selenium.common.exceptions import NoSuchElementException
import datetime
import time
import random
import textwrap

class SeleniumError(Exception):
    def __init__(self, msg: str = ''):
        Exception.__init__(self, msg)
        
        
class BrowserError(SeleniumError):
    def __init__(self, msg: str = ''):
        SeleniumError.__init__(self, msg)
        

class Web:
    """This class creates a instance of the Selenium WebDriver and
    simplifies working with some of the more common methods providing basic
    web scraping and automation capabilities. Please make sure that you have
    permission to scrape a site before using this tool!
    """

    def __init__(self, browser: str = 'Firefox', timeout: int = 0) -> None:
        """Initialize the Web object.
        
        Keyword arguments:
        browser --  The name of the browser to use for this session.
                    Valid browsers are: 'firefox' (default), 'chrome',
                    'edge', 'ie', 'safari'.
        timeout --  Sets an implicit wait for this session which will
                    act as the default timeout value, in seconds, for 
                    all future element requests made by the driver.
                    (default 0)
                    
        Exceptions:
        BrowserError -- This exception is raised when an invalid browser
                        has been passed.
        """
        #Will hold all open window handles in the order opened.
        self.tabs = []
        try:
            if browser.lower() == 'firefox':
                self.browser = 'firefox'
                self.driver = webdriver.Firefox()
            elif browser.lower() == 'chrome':
                self.browser = 'chrome'
                self.driver = webdriver.Chrome()
            elif browser.lower() == 'edge':
                self.browser = 'edge'
                self.driver = webdriver.Edge()
            elif brower.lower() == 'ie':
                self.browser = 'ie'
                self.driver = webdriver.Ie()
            elif browser.lower() == 'safari':
                self.browser = 'safari'
                self.driver = webdriver.Safari()
            else:
                raise BrowserError("Invalid Browser")
        except BrowserError as error:
            print(error.msg)
            raise
        except:
            raise
        else:
            self.driver.implicitly_wait(timeout)
            self.tabs.append(self.driver.current_window_handle)
    
    def getPage(self, url: str) -> None:
        """Attempt to load the specified URL on the active tab.
        
        Keyword arguments:
        url --  The URL of the page to be visited. Only sites that start
                with 'http://' or 'https://' are allowed.
        """
        try:
            assert(url.startswith('https://') or url.startswith('http://'))
        except AssertionError:
            url = 'http://' + url
        url = url.strip()
        try:
            self.driver.get(url)
        except:
            raise
    
    def getElement(self, value: str, by=By.ID, 
            scope: WebElement = None) -> WebElement:
        """Search scope and return the first matching element.
        
        Search the specified scope using the locator strategy, by, for
        the first element matching value. Since IDs are guaranteed to be
        unique, this is the recommended and default locator strategy.
        Locating elements without unique IDs can be accomplished with
        multiple calls to this method or with an XPath locator.
        
        Keyword arguments:
        value   --  The search value to match.
        by      --  Takes a locator of the By object which indicates the
                    strategy to search with. Valid locators are:
            CLASS_NAME      --  Locates elements whose class name 
                                contains the search value. 
                                (compound class names are not permitted)
            CSS_SELECTOR    --  Locates elements matching a CSS 
                                selector.
            ID              --  Locates elements whose ID attribute 
                                matches the search value. (default)
            NAME            --  Locates elements whose NAME attribute 
                                matches the search value.
            LINK_TEXT       --  Locates anchor elements whose visible 
                                text matches the search value.
            PARTIAL_LINK_TEXT   --  Locates anchor elements whose 
                                    visible text contains the search 
                                    value.
            TAG_NAME        --  Locates elements whose tag name matches
                                the search value.
            XPATH           --  Locates elements matching an XPath 
                                expression.
        scope   --  Reference to another element which will provide the
                    scope to search. If None is provided the entire DOM
                    object of the active page will be used. (Optional)
                    (default None)
        Exceptions:
        NoSuchElementException  --  This exception is raised when an
                                    element matching the search criteria
                                    cannot be found within the scope.
        """
        try:
            if scope:
                return scope.find_element(by, value)
            else:
                return self.driver.find_element(by, value)
        except NoSuchElementException as error:
            print(error.msg)
            return None
        except:
            raise
    
    def getElements(self, value: str, by=By.ID, 
            scope: WebElement = None) -> list[WebElement]:
        """Search scope and return a list of all matching elements.
        
        Functionality, arguments, and exceptions are the same the 
        getElement method except that a list containing all matching 
        elements within the scope is returned.
        
        Keyword arguments:
        value   --  The search value to match.
        by      --  Takes a locator of the By object which indicates the
                    strategy to search with. See getElement() for valid
                    locators. (default By.ID)
        scope   --  Reference to another element which will provide the
                    scope to search. If None is provided the entire DOM
                    object of the active page will be used. (Optional)
                    (default None)
        Exceptions:
        NoSuchElementException  --  This exception is raised when an
                                    element matching the search criteria
                                    cannot be found within the scope.
        """
        try:
            if scope:
                return scope.find_elements(by, value)
            else:
                return self.driver.find_elements(by, value)
        except NoSuchElementException as error:
            print("Couldn't locate {value} {by}")
            return []
        except:
            raise

    def locate(self, value: str, by: By, position: str, 
            element: WebElement) -> WebElement:
        """Locate and return a WebElement relative to another WebElement.
        
        When it is difficult to locate an element on the page directly
        for some reason, this method can be used to find an element
        based on the relative location to another element which is 
        easier to locate. Returns a reference to the first matching
        element if found
        
        Keyword arguements:
        value       --  The search value to match.
        by          --  Takes a locator of the By object which indicates
                        the strategy to search with. See getElement() 
                        for valid locators.
        position    --  The location relative to the provided element
                        to be searched. Valid positions are: 'above', 
                        'below', 'near', 'left', 'right'.
        element     --  A reference to another WebElement which will be 
                        used as a starting point to start the search.           
        """
        #Create relative locator
        locator = RL.locate_with(by, value)
        #Use the relative locator and the correct positional method
        #along with the known element location to create a RelativeBy
        #object. Return the first element found with the Relative By
        #object.
        match position:
            case 'above':
                return self.driver.find_element(locator.above(element))
            case 'below':
                return self.driver.find_element(locator.below(element))
            case 'near':
                return self.driver.find_element(locator.near(element))
            case 'left':
                return self.driver.find_element(locator.to_left_of(element))
            case 'right':
                return self.driver.find_element(locator.to_right_of(element))
            case _:
                print('Invalid position')
                
    
    def newTab(self, url: str = None) -> None:
        """Open a new tab and load the specified URL.
        
        If no URL is provided, a blank tab is opened instead.
        
        Keyword Arguments:
        url --  The address of web page to be loaded on the newly opened
                tab. (Optional)
        """
        self.driver.switch_to.new_window('tab')
        self.tabs.append(self.driver.current_window_handle)
        if url:
            self.getPage(url)
        
    def closeTab(self, tab = None) -> None:
        """Close a tab.
        
        Keyword Arguments:
        tab --  The handle of the tab to be closed. If this argument is
                not provided, the active tab is closed instead. 
                (Optional)
        """
        if tab:
            try:
                self.tabs.remove(tab)
            except ValueError:
                print("Invalid tab handle provided")
                return
            else:
                self.driver.switch_to.window(tab)
        self.driver.close()
        if len(self.tabs) == 0:
            self.newTab()
        else:
            self.driver.switch_to.window(self.tabs[0])
        
    def switchTab(self, tab = 0) -> None:
        """Switch active tabs.
        
        Keyword Arguments:
        tab --  The handle of the tab to switch to. If this argument is
                omitted, the first tab in the tabs list is used by
                default. (default self.tabs[0])
        """
        if tab == 0:
            self.driver.switch_to.window(self.tabs[0])
        else:
            self.driver.switch_to.window(tab)
    
    def scrape(self, element: WebElement = None) -> str:
        """Return text found within the page or element.
        
        Keyword Arguments:
        element --  A WebElement reference to be scraped. All text found
                    within the element will be returned. If this
                    argument is omitted, the entire DOM will be scraped
                    instead. (Optional)
        """
        if not element:
            element = self.getElement('html', By.TAG_NAME)
        return element.text
    
    def quit(self) -> None:
        """Quit the current WebDriver session.
        """ 
        self.driver.quit()

            
if __name__ == "__main__":
    """
    The following is an example of how this script could be used to
    scrape and format text from the site books.toscrape.com. A random
    book category from the site is chosen at runtime and formatted text
    from the first 3 books is saved in a new file.
    """
    #Create a new web session with Firefox as the browser.
    session = Web('Firefox', 5)
    try:
        #Path where info will be downloaded.
        folder = 'D:\\Projects\\Python\\Web_Scraper\\Books\\'
        stamp = datetime.datetime.now()
        date = stamp.strftime('%m-%d-%y')
        file = f'{folder}Books {date}.txt'
        maxBooks = 3
        #Create a file to hold today's books and open a file stream
        #to write to it.
        output = open(file, 'wt')
        #Load the site in the active window.
        session.getPage('books.toscrape.com')
        #Fetch the categories element on the page by class name.
        categories = session.getElement('side_categories', By.CLASS_NAME)
        #Fetch a list of all links in the categories element.
        categories = session.getElements('a', By.TAG_NAME, categories)
        #Select a random category to scrape for the day.
        link = categories[random.randrange(1, len(categories))]
        #Write the chosen category and date to the output stream.
        header = f'{link.text} - {date}'
        output.write(f'{header:^79s}\n')
        output.write(f'{"----------":^79s}\n')
        #Open the category link in a new tab.
        link = link.get_attribute('href')
        session.getPage(link)
        #Fetch the list of books in this category.
        books = session.getElements('product_pod', By.CLASS_NAME)
        for i in range(len(books)):
            if i >= maxBooks:
                break
            #Fetch the link to the current book and open it in a new tab.
            link = session.getElement('a', By.TAG_NAME, books[i])
            link = link.get_attribute('href')
            session.newTab(link)
            #Fetch book title, description, and product information.
            title = session.getElement('product_main', By.CLASS_NAME)
            title = session.getElement('h1', By.TAG_NAME)
            description = session.getElement('product_description', By.ID)
            description = session.locate('p', By.TAG_NAME, 'below', 
                    description)
            information = session.getElements('//table//tr', By.XPATH)
            #Write the title, description, and product information to the file.
            output.write(f'--{title.text}--\n')
            output.write('Description:\n')
            output.write(f'{textwrap.fill(description.text, 79)}\n\n')
            output.write('Product Information:\n')
            for row in information:
                head = session.getElement('th', By.TAG_NAME, row)
                data = session.getElement('td', By.TAG_NAME, row)
                output.write(f'{head.text:20s}: {data.text}\n')
            output.write(f'{"----------":^79s}\n')
            #Close the current tab and loop to the next book.
            session.closeTab()
        #Close the output stream.
        output.close()
    except:
        raise
    finally:
        #Finally statement ensures that quit method is called to close
        #appropriate ports and clean up memory stack.
        session.quit()