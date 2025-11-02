import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SimpleInstagramUnfollower:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.username = None
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 3)
        
    def login_with_session(self, session_id):
        try:
            print("Logging in...")
            self.driver.get("https://www.instagram.com/")
            
            self.driver.add_cookie({
                'name': 'sessionid',
                'value': session_id,
                'domain': '.instagram.com',
                'path': '/',
                'secure': True,
                'httpOnly': True
            })
            
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/']/div"))
            )
            print("Login successful!")
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
            
    def get_following_count(self):
        try:
            profile_url = f"https://www.instagram.com/{self.username}/"
            self.driver.get(profile_url)
            time.sleep(3)
            
            selectors = [
                "//a[contains(@href, '/following')]/span/span",
                "//a[contains(@href, '/following')]//span[contains(text(), 'following')]",
                "//a[contains(@href, '/following')]"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        text_content = element.text
                        if 'following' in text_content.lower():
                            numbers = re.findall(r'\d+', text_content.replace(',', ''))
                            if numbers:
                                count = int(numbers[0])
                                print(f"Following count: {count}")
                                return count
                except:
                    continue
                    
            print("Could not extract following count")
            return 0
        except Exception as e:
            print(f"Could not get following count: {e}")
            return 0
            
    def unfollow_users(self, count=None):
        try:
            following_url = f"https://www.instagram.com/{self.username}/following/"
            self.driver.get(following_url)
            time.sleep(3)
            
            unfollowed = 0
            scroll_cycle = 0
            processed_usernames = set()
            
            total_to_unfollow = count if count else self.get_following_count()
            if total_to_unfollow == 0:
                total_to_unfollow = 9999
            
            print(f"Will attempt to unfollow {total_to_unfollow} accounts")
            print("-" * 40)
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            while True:
                if count and unfollowed >= count:
                    break
                
                if unfollowed > 0 and unfollowed % 12 == 0:
                    print(f"[Scrolling to load more accounts...] ({unfollowed} processed)")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    scroll_cycle += 1
                
                following_buttons = []
                attempts = 0
                
                while not following_buttons and attempts < 3:
                    following_buttons = self.driver.find_elements(By.XPATH, "//button[.//div[text()='Following']]")
                    if not following_buttons:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1.5)
                        attempts += 1
                
                if not following_buttons:
                    print("Loading more accounts...")
                    for i in range(5):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                        following_buttons = self.driver.find_elements(By.XPATH, "//button[.//div[text()='Following']]")
                        if following_buttons:
                            break
                
                if not following_buttons:
                    print("Checking for remaining accounts...")
                    time.sleep(3)
                    following_buttons = self.driver.find_elements(By.XPATH, "//button[.//div[text()='Following']]")
                    if not following_buttons:
                        print("\nNo more accounts to unfollow")
                        break
                
                processed_this_round = 0
                for button in following_buttons:
                    if count and unfollowed >= count:
                        break
                    
                    try:
                        username = "unknown"
                        try:
                            parent_div = button.find_element(By.XPATH, "./../../..")
                            username_link = parent_div.find_element(By.XPATH, ".//a[contains(@href, '/')]")
                            href = username_link.get_attribute("href")
                            if href:
                                username = href.rstrip('/').split('/')[-1]
                        except:
                            pass
                        
                        if username in processed_usernames:
                            continue
                            
                        processed_usernames.add(username)
                        
                        self.driver.execute_script("arguments[0].click();", button)
                        
                        try:
                            confirm_btn = self.driver.find_element(By.XPATH, "//button[text()='Unfollow']")
                            self.driver.execute_script("arguments[0].click();", confirm_btn)
                        except:
                            pass
                        
                        unfollowed += 1
                        remaining = total_to_unfollow - unfollowed
                        print(f"Unfollowed @{username} ({unfollowed}) | Remaining: {remaining}")
                        
                        processed_this_round += 1
                        time.sleep(0.3)
                        
                        if processed_this_round >= 5:
                            break
                            
                    except Exception as e:
                        if username not in processed_usernames:
                            processed_usernames.add(username)
                            unfollowed += 1
                        time.sleep(0.3)
                
                if processed_this_round == 0:
                    print("[Forcing scroll to load new accounts...]")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                if unfollowed > 0 and scroll_cycle > 100:
                    print("Safety break - too many scroll cycles")
                    break
                    
            print(f"\nSuccessfully processed {unfollowed} accounts")
        except Exception as e:
            print(f"Error in unfollow process: {e}")
            import traceback
            traceback.print_exc()

    def close(self):
        if self.driver:
            self.driver.quit()

def main():
    print("Simple Instagram Unfollower")
    print("=" * 30)
    
    unfollower = SimpleInstagramUnfollower()
    unfollower.setup_driver()
    
    try:
        session_id = input("Enter Instagram session ID: ").strip()
        unfollower.username = input("Enter your Instagram username: ").strip()
        
        if not session_id or not unfollower.username:
            print("Missing authentication information")
            return
            
        if not unfollower.login_with_session(session_id):
            print("Login failed")
            return
            
        confirm = input("Type 'UNFOLLOW' to proceed: ")
        if confirm.upper() != 'UNFOLLOW':
            print("Cancelled")
            return
            
        count = unfollower.get_following_count()
        print(f"You are following {count} accounts")
        
        count_input = input("How many to unfollow? (Enter for all): ").strip()
        unfollow_count = None
        if count_input:
            try:
                unfollow_count = int(count_input)
                if unfollow_count <= 0:
                    print("Invalid count, will unfollow all")
                    unfollow_count = None
            except ValueError:
                print("Invalid number, will unfollow all")
        
        print("Starting unfollow process...")
        unfollower.unfollow_users(unfollow_count)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        unfollower.close()
        print("Browser closed")

if __name__ == "__main__":
    main()
