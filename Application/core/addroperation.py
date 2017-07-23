import  struct, socket


def get_iplist(addr):
    (ip, cidr) = addr.split('/')
    cidr = int(cidr)
    if cidr==32:
        return ip
    host_bits = 32 - cidr
    i = struct.unpack('>I', socket.inet_aton(ip))[0]
    start = (i >> host_bits) << host_bits
    end = i | ((1 << host_bits) - 1)
    list=[]
    for i in range(start, end):
        list.append(socket.inet_ntoa(struct.pack('>I', i)))

