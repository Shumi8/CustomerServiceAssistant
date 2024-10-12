def get_tracking_history(TrackTraceNumber, ShippingSupplier, ShippingName, ZipCode, shipping_category):
    
    driver = get_chrome_driver()
    if ShippingSupplier == '':
        logging.info('Extracting Tracking History from the website of Burd')
        driver.get(f"")
        wait = WebDriverWait(driver, 10)
        tracking_status = wait.until(EC.presence_of_element_located((By.ID, 'orderStatus'))).text
        latest_timestamp = " ".join(tracking_status.split("\n")[0].split()[:2]).replace(" kl.", "")
        latest_tracking_date = datetime.strptime(latest_timestamp, "%d/%m/%Y")

    elif ShippingSupplier == '':
        logging.info('Extracting Tracking History from the website of DAO')
        driver.get(f"")
        wait = WebDriverWait(driver, 10)
        tracking_status = ""

        for i in range(1, 7):
            try:
                xpath = f"/html/body/section/div/div/section[2]/div/div/div[2]/div[{i}]"

                try:
                    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    element_text = str(element.get_attribute('innerText')).strip()
                    lines = element_text.split('\n')
                    if len(lines) >= 3:
                        tracking_status += f"{lines[0]} {lines[1]} {lines[2]}\n{lines[3]}\n\n"
                    else:
                        tracking_status += f"{element_text}\n\n"
                except NoSuchElementException:
                    break
             
            except:
                try:
                    xpath = f"/html/body/section/div/div/section[2]/div/div/div/div[2]/div[{i}]"
                    try:
                        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                        element_text = str(element.get_attribute('innerText')).strip()
                        lines = element_text.split('\n')
                        if len(lines) >= 3:
                            tracking_status += f"{lines[0]} {lines[1]} {lines[2]}\n{lines[3]}\n\n"
                        else:
                            tracking_status += f"{element_text}\n\n"
                    except NoSuchElementException:
                        break
                except:
                    break
        # Danish to English month mapping
        month_map = {'januar': 'Jan', 'februar': 'Feb', 'marts': 'Mar', 'april': 'Apr', 'maj': 'May', 'juni': 'Jun', 'juli': 'Jul', 'august': 'Aug',
            'september': 'Sep', 'oktober': 'Oct', 'november': 'Nov', 'december': 'Dec'
        }

        latest_timestamp = tracking_status.split('\n')[0]
        for danish, english in month_map.items():
            latest_timestamp = latest_timestamp.replace(danish, english)
        
        latest_timestamp = datetime.strptime(latest_timestamp, "%d. %b. %Y %H:%M:%S")
        latest_tracking_date = latest_timestamp.strftime("%d/%m/%Y")
        latest_tracking_date = datetime.strptime(latest_tracking_date, "%d/%m/%Y")
        if shipping_category == 'Privatadresse':
            tracking_status = '\n'.join(tracking_status.split('\n')[:2])
        else:
            pass

    elif ShippingSupplier == '':
        logging.info('')
        driver.get(f"https://tracking.postnord.com/en/?id={TrackTraceNumber}")
        wait = WebDriverWait(driver, 10)
        cookie_accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_accept_button.click()
        locate_root_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div > pn-widget")))
        time.sleep(2)
        try:
            driver.execute_script(
                'arguments[0].shadowRoot.querySelector("main > div > div > div > div > div.delivery-route > div > pn-button > button > div.pn-button-bg").click()',
                locate_root_element)
        except Exception:
            pass

        configure_shadow_root = wait.until(lambda driver: driver.execute_script(
            'return arguments[0].shadowRoot.querySelector("main > div > div > div > div > div.delivery-route")',
            locate_root_element))
        postnord_status_tracking_history = wait.until(
            lambda driver: driver.execute_script("return arguments[0].textContent;", configure_shadow_root))
        postnord_status_tracking_history = postnord_status_tracking_history.replace("Delivery Route", "").replace(
            "View less", "")
        postnord_status_tracking_history = postnord_status_tracking_history.replace("DK", "DK ")
        tracking_status = postnord_status_tracking_history.replace(".", ".\n")
        latest_time_shadow_root = wait.until(lambda driver: driver.execute_script(
            'return arguments[0].shadowRoot.querySelector("main > div > div > div > div > div.delivery-route > div > ul > li:nth-child(1) > div > div > p")',
            locate_root_element))
        latest_time = wait.until(
            lambda driver: driver.execute_script("return arguments[0].textContent;", latest_time_shadow_root))
        if 'Today' in latest_time:
            # Replace 'Today' with the current date in the format 'd M'
            latest_time = latest_time.replace('Today', datetime.now().strftime('%d %b'))
            now = datetime.now()
            latest_date = datetime.strptime(latest_time, "%d %b %H:%M")
            latest_tracking_date = latest_date.replace(year=now.year)

        elif 'Yesterday' in latest_time:
            # Replace 'Yesterday' with the previous date in the format 'd M'
            latest_time = latest_time.replace('Yesterday', (datetime.now() - timedelta(days=1)).strftime('%d %b'))
            now = datetime.now()
            latest_date = datetime.strptime(latest_time, "%d %b %H:%M")
            latest_tracking_date = latest_date.replace(year=now.year)

        else:
            now = datetime.now()
            latest_date = datetime.strptime(latest_time, "%d %b, %H:%M")
            latest_tracking_date = latest_date.replace(year=now.year)

    elif ShippingSupplier == '' or ShippingName == '' or ShippingSupplier == '':
        logging.info('Extracting Tracking History from the website of GLS')
        driver.get(f"")
        wait = WebDriverWait(driver, 10)
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, 's-all-bn')))
        cookie_button.click()
        search_bar = wait.until(EC.element_to_be_clickable((By.ID, 'witt002_details_postalcode_input')))
        search_bar.send_keys(ZipCode)
        search_bar.send_keys(Keys.RETURN)
        trigger = wait.until(EC.element_to_be_clickable((By.ID, 'witt002_details_accordion_history_trigger')))
        trigger.click()
        gls_tracking_status_history = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'history-list'))).text
        format_status_history = gls_tracking_status_history.split("\n")
        formatted_status_history = []
        i = 0
        while i < len(format_status_history):
            timestamp = format_status_history[i]
            message = format_status_history[i + 1]
            location = format_status_history[i + 2]
            country = format_status_history[i + 3]
            formatted_status_history.append(f"{timestamp}\n{message}\n{location}: {country}")
            i += 4
        tracking_status = "\n\n".join(formatted_status_history)
        latest_timestamp = formatted_status_history[0].split("\n")[0]
        latest_tracking_date = datetime.strptime(latest_timestamp.split(' ')[0], "%d.%m.%Y")

    elif ShippingSupplier == '':
        logging.info('Extracting Tracking History from the website of Instabox')
        driver.get(f"")

        wait = WebDriverWait(driver, 7)

        try:
            input_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/form/div/div[1]/div/input')))
            input_element.send_keys(ZipCode)
            time.sleep(2)
            input_element.send_keys(Keys.RETURN)
        except TimeoutException:
            pass

        try:
            button_1in7dsyb = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[5]/div[1]/div[2]/div/button')))
            button_1in7dsyb.click()
        except:
            try:
                time.sleep(6)
                button_1in7dsyb = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[5]/div[1]/div[2]/div/button')))
                button_1in7dsyb.click()
            except:
                try:
                    element_to_click = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                '//*[@id="__next"]/div/main/div/div/div/div[1]/div[1]/div/div[1]/article/div/div[3]/div/div/div[2]/div/p[1]')))
                    element_to_click.click()
                except NoSuchElementException:
                    pass

        try:
            time.sleep(2)
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_wuo76bk')))
            tracking_status = ""
            for element in elements:
                tracking_status += element.text
            lines = tracking_status.split('\n')

            # Remove the first line if it doesn't start with a date
            if not re.match(r'(\d{1,2} \w+|Idag)', lines[0]):
                lines = lines[1:]

            # Convert the date in the first line to the desired format
            now = datetime.now()
            match = re.search(r'(\d{1,2} \w+|Idag), kl. \d{2}:\d{2}', lines[0])
            if match is not None:
                latest_time = match.group(0)
                # Map Swedish month names to English
                month_map = {'januari': 'Jan', 'februari': 'Feb', 'mars': 'Mar', 'april': 'Apr',
                            'maj': 'May', 'juni': 'Jun', 'juli': 'Jul', 'augusti': 'Aug',
                            'september': 'Sep', 'oktober': 'Oct', 'november': 'Nov', 'december': 'Dec'}
                # Replace Swedish month names with English month abbreviations
                for swedish, english in month_map.items():
                    latest_time = latest_time.replace(swedish, english)

                if 'Idag' in latest_time:
                    latest_time = latest_time.replace('Idag', datetime.now().strftime('%d %b'))
                    latest_date = datetime.strptime(latest_time, "%d %b, kl. %H:%M")
                else:
                    latest_date = datetime.strptime(latest_time, "%d %b, kl. %H:%M")

                latest_tracking_date = latest_date.replace(year=now.year)
            else:
                logging.info("Date Pattern Didn't Match")
                pass
        except:
            elements = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div[1]/div[1]/div/div[1]/article/div/div[3]/div')))
            tracking_history = ""
            for element in elements:
                tracking_history += element.text
            lines = tracking_history.split('\n')
            filtered_lines = [line for line in lines if 'DK' not in line]

            # Add an empty line after every two lines
            lines_with_spaces = []
            for i in range(0, len(filtered_lines), 2):
                lines_with_spaces.extend(filtered_lines[i:i + 2])
                lines_with_spaces.append('')

            tracking_status = '\n'.join(lines_with_spaces)

            first_line = tracking_status.split('\n')[0]

            date_time_match = re.search(r'\d{1,2} \w+ kl. \d{2}:\d{2}', first_line)
            if date_time_match:
                date_time_str = date_time_match.group()

            # Map Swedish month names to English
            month_map = {'januari': 'January', 'februari': 'February', 'mars': 'March', 'april': 'April',
                        'maj': 'May', 'juni': 'June', 'juli': 'July', 'augusti': 'August',
                        'september': 'September', 'oktober': 'October', 'november': 'November', 'december': 'December'}

            for swedish, english in month_map.items():
                date_time_str = date_time_str.replace(swedish, english)

            date_time_str = date_time_str.replace('kl. ', '')

            now = datetime.now()
            latest_date = datetime.strptime(date_time_str, "%d %B %H:%M")
            latest_tracking_date = latest_date.replace(year=now.year)

    else:
        tracking_status = "Invalid Shipping Supplier"

    driver.quit()
    return tracking_status, latest_tracking_date
