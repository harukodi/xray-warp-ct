
class Warp:
    @staticmethod
    def read_wgcf_profile():
        with open("./wgcf/wgcf-profile.conf", "r") as wgcf_profile:
            data = wgcf_profile.readlines()
            stripped_lines = [line.strip("\n") for line in data]
        return stripped_lines
    @staticmethod
    def warp_private_key():
        for line in Warp.read_wgcf_profile():
            if line.startswith("PrivateKey ="):
                private_key = line.split("=", 1)[1].strip()
                return private_key
    @staticmethod
    def warp_ipv4():
        for line in Warp.read_wgcf_profile():
            if line.startswith("Address ="):
                warp_ipv4 = line.split("=", 1)[1].split(",")[0].strip()
                return warp_ipv4
    @staticmethod
    def warp_ipv6():
        for line in Warp.read_wgcf_profile():
            if line.startswith("Address ="):
                warp_ipv6 = line.split("=", 1)[1].split(",")[1].strip()
                return warp_ipv6
    @staticmethod
    def warp_public_key():
        for line in Warp.read_wgcf_profile():
            if line.startswith("PublicKey ="):
                public_key = line.split("=", 1)[1].strip()
                return public_key