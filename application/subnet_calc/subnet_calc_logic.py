import ipaddress

class SubnetCalculator:

    def __init__(self, subnet=None, split=None):
        self.subnet = subnet
        self.split = split


    def get_subnets(self, subnet, split):
        return [subnets for subnets in ipaddress.ip_network(subnet)
            .subnets(new_prefix=int(split))]

    def get_split_subnets(self, subnet):
        return [subnets for subnets in ipaddress.ip_network(subnet).subnets()]



    def get_subnet_details(self, subnets):
        dict_of_subnets = {}

        for subnet in subnets:
            dict_of_subnets[str(subnet)] = {
                    "network": str(subnet),
                    "netmask": str(subnet.netmask),
                    "wildcard": str(ipaddress.ip_network(subnet).hostmask),
                    "usable_ips": str(list(ipaddress.ip_network(subnet)
                                           .hosts())[0]) + "-" +
                                  str(list(ipaddress.ip_network(subnet)
                                           .hosts())[-1]),
                    "num_of_hosts": str(len(list(ipaddress.ip_network(subnet).hosts())))
            }
        return dict_of_subnets
