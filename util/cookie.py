import browser_cookie3

class Cookie:
    @staticmethod
    def get_cookie() -> dict:    
        '''
        Get Cookie from browser to login
        '''
        cookie = {}

        cj = browser_cookie3.chrome()
        cookie_list = list(filter(lambda x: x.name == "cpaonline", cj))

        if cookie_list:
            cookie = {cookie_list[0].name:cookie_list[0].value}

        return cookie