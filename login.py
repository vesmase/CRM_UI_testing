__Author__ = 'Jade Makdessi'

# GLOBAL LIBRARIES
from drivers import Drivers
from VSS_loggers import VSS_START
from utilities.VSS_DB import VSS_DB
from VSS_web_helpers import VSSDriver
from params import VSS_params as params
from functions.VSS_functions import Functions
from settings import VSS_settings as settings
from utilities.common_utilities import CommonUtilities as Utilities

class Login(object):
    """
    This class has login methods and is invoked by the set_up.py
    """
        
    def __init__(self):
        
        VSS_START.info('LAUNCH setUP...')        
        
        # GENERIC METHODS
        db = VSS_DB()
        
        # CLASSES
        self.driver = Drivers()
        VSS_START.info('Starting driver...') 
        self.driver = self.driver.driver
        VSS_START.info('Starting vssdriver...') 
        self.vssdriver = VSSDriver(self.driver)
        self.utilities = Utilities(db)       
        self.functions = Functions(self.driver, self.vssdriver, db)
        
        
    def login_AIL(self):
        """
        Login to AIL, returns a list with methods and other stuff needed in 
        setUp file.
        """
        
        # REMOVE WHEN SCHEMA IS AVAILABLE IN AIL
        if params.SCHEMA == 'VSS_EETEST':
            params.SCHEMA = 'VIASAT_EETEST'
                  
        VSS_START.info('Log in to AIL({0})'.format(params.SCHEMA))
                
        # CHECKS IF PRODUCTION SERVER
        if '102.82' in settings.AILURL:
            raise Exception('refusing to run on production environment') 
                   
        self.driver.implicitly_wait(10) 
               
        # NAVIGATES TO AIL   
        self.driver.get(settings.AILURL)
                
        # USERNAME
        self.vssdriver.try_send_text_by_element('ail_username_tb', params.USERNAMEAIL,'value') 
               
        # PASSWORD
        self.vssdriver.try_send_text_by_element('ail_password_tb', params.PASSWORDAIL,'value')
                
        # ELEMENT
        s = self.vssdriver.get_element("ail_master_partner_cmb","login_AIL: 's' 1")
        
        # SCHEMA
        FOUND = False
        for option in s.find_elements_by_tag_name('option'):
            if params.SCHEMA in option.text:
                option.click()
                FOUND = True                                      
                break 
        if not FOUND:
            raise Exception('Schema {0} not found, check OS environ schema'.format(params.SCHEMA))
        
        # LOGIN
        self.vssdriver.try_click_by_element('ail_login_bt')
                   
        self.driver.implicitly_wait(5)
                
        VSS_START.info('Logged in to AIL({0})'.format(params.SCHEMA))   
        
        return (self.driver, self.vssdriver, self.functions, self.utilities)
                
    def login_CRM(self):
        """
        Login to CRM, returns a list with methods and other stuff needed in 
        setUp file.
        """        
        
        VSS_START.info('Log in to CRM({0})'.format(params.SCHEMA))        
        
        # CHECKS IF PRODUCTION SERVER              
        if '102.82' in settings.CRMURL:
            raise Exception('refusing to run on production environment')    
              
        self.driver.implicitly_wait(10)   
             
        # NAVIGATES TO CRM
        self.driver.get(settings.CRMURL)  
              
        # USERNAME
        self.vssdriver.try_send_text_by_element('crm_username_tb', params.USERNAMECRM,'value') 
               
        # PASSWORD
        self.vssdriver.try_send_text_by_element('crm_password_tb', params.PASSWORDCRM,'value')
                
        # CLICK SELECT OTHER SCHEMAS
        self.vssdriver.try_click_by_element('crm_select_unit_lnk')
        
        self.driver.implicitly_wait(5)
        
        if params.SCHEMA == 'VSS_LTUPG' or params.SCHEMA == 'VSS_NOUPG' or params.SCHEMA == 'VSS_EEUPG' or params.SCHEMA == 'VSS_FIUPG' or params.SCHEMA == 'VIASAT_SETEST':
                  
            # ELEMENT
            s = self.vssdriver.get_element("crm_master_partner_cmb", "login_CRM: 's' 1")
                    
            # SCHEMA
            for option in s.find_elements_by_tag_name('option'):
                if params.SCHEMA in option.text:
                    option.click()                
                    break
                
        elif params.SCHEMA == 'VIASAT_EE':
            
            # ATTRIBUTE
            s = self.vssdriver.find_attribute('crm_master_partner_tb', 'value')
            if s != params.SCHEMA:
                raise Exception('refusing to run on other schema than {0}'.format(params.SCHEMA))
                      
        self.driver.implicitly_wait(5)
                
        # LOGIN
        self.vssdriver.try_click_by_element('crm_login_bt')   
             
        VSS_START.info('Logged in to CRM({0})'.format(params.SCHEMA))  
        
        return (self.driver, self.vssdriver, self.functions, self.utilities)

