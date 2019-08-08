'''
    Class to get HTTPS proxy servers from websites.

    For proper usage see get_proxy method.
'''

from requests_html import HTMLSession


class Proxy:

    def is_fast_enough(self, ip_port, timeout=1, v=False):
        '''check if proxy is fast enough'''
        proxies = {"http": f"http://{ip_port}",
                   "https": f"https://{ip_port}"
                   }

        try:
            for i in range(1):
                # self.s = HTMLSession()
                # breakpoint()

                r = self.s.get("https://www.example.com",
                               proxies=proxies, timeout=timeout)
                # check that website really loaded
                if r.html.find("title")[0].text != "Example Domain":

                    print("something is wrong with proxy server")
                    return False
            # breakpoint()
            return True

        except Exception as e:
            if v:
                print(e)
                print("timed out")
            # breakpoint()
            return False

    def get_from_free_proxy_list(self, elite_only):
        url = "https://free-proxy-list.net/"

        r = self.s.get(url)
        sel = 'table#proxylisttable tbody tr'
        rows = r.html.find(sel)

        data = []

        if elite_only:
            for row in rows:
                tds = [i.text for i in row.find("td")]

                if tds[4].strip() == "elite proxy" and tds[6] == "yes":
                    ip, port = tds[:2]
                    # print(f'{ip}:{port}')
                    data.append(f'{ip}:{port}')
        else:
            for row in rows:
                tds = [i.text for i in row.find("td")]

                if tds[6] == "yes":
                    ip, port = tds[:2]
                    # print(f'{ip}:{port}')
                    data.append(f'{ip}:{port}')
        return data

    # NOT USEFUL #
    # def get_from_ssl_proxies_list(self):
    #     url = "https://www.sslproxies.org/"

    #     r = self.s.get(url)

    #     sel = "#proxylisttable tbody tr"
    #     rows = r.html.find(sel)

    #     data = set()

    #     for row in rows:
    #         if row.text.split("\n")[-4] == "elite proxy":
    #             first_two = row.text.split("\n")[:2]

    #             add_me = ":".join([i.strip() for i in first_two])
    #             data.add(add_me)

    #     return data

    def get_from_us_proxy_org(self, elite_only=True):
        url = "https://www.us-proxy.org"

        r = self.s.get(url)

        sel = "#proxylisttable tbody tr"
        rows = r.html.find(sel)

        data = set()

        for row in rows:

            if elite_only:
                if row.text.split("\n")[4] == "elite proxy"  \
                                          and row.text.split("\n")[6] == "yes":
                    first_two = row.text.split("\n")[:2]

                    add_me = ":".join([i.strip() for i in first_two])
                    data.add(add_me)
            else:
                if row.text.split("\n")[6] == "yes":
                    first_two = row.text.split("\n")[:2]

                    add_me = ":".join([i.strip() for i in first_two])
                    data.add(add_me)

        return data

    def get_all_proxies_list(self, elite_only=True):
        data = set()
        self.s = HTMLSession()

        '''
        get all proxies list from site and assign to self.working_proxies
        '''
        # first source
        data.update(self.get_from_free_proxy_list(elite_only=elite_only))

        # second source
        data.update(self.get_from_us_proxy_org(elite_only=elite_only))

        data = list(data)

        return data

    def get_proxy(self, num=1, timeout=0.5,
                  elite_only=True, as_dict=False, v=False):
        '''
        get one or more proxies(default timeout=0.5).
        result may not contain as much as we wanted working proxies
        with given timeout, so check result's length when needed

        set as_dict to True, to get dictionary, that can be directly used
        in requests library.
        '''
        proxies = []

        for ip in self.get_all_proxies_list(elite_only=elite_only):
            if self.is_fast_enough(ip, timeout=timeout, v=v):
                print(ip)
                proxies.append(ip)

                if len(proxies) == num:
                    break

        if as_dict:
            proxies = [{"http": f"http://{ip_port}"} for ip_port in proxies]
        elif num == 1:
            proxies = proxies[0]

        return proxies
