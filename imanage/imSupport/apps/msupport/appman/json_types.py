import json
　
　
class instance_j:
　
    name = ""
    server_name = ""
    product_version = ""
    product_osuser = ""
    associated_server_name = ""
    cluster = ""
    profile = ""
　
    def __init__(self, name, server_name, product_version, product_osuser, associated_server_name, cluster):
        self.name = name
        self.server_name = server_name
        self.product_version = product_version
        self.product_osuser = product_osuser
        self.associated_server_name = associated_server_name
        self.cluster = cluster
　
    def set_profile(self, profilename):
        self.profile = profilename
　
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
