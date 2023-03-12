import binascii

expected = 3796810847
exe = '"ghex"'
appname = 'GHex'
data = ''.join([exe, appname])
result = binascii.crc32(data.encode('utf8')) | 0x80000000
print (data.encode('utf8'))

print (result)
print (expected)
print (bin(result))
print (bin(expected))

#assert expected == calculator.checksum(data)

