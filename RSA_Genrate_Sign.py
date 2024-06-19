import chilkat

# This example assumes the Chilkat API to have been previously unlocked.
# See Global Unlock Sample for sample code.

rsa = chilkat.CkRsa()

# Generate a 2048-bit RSA key.
success = rsa.GenerateKey(2048)

# To return the signature in hex.
rsa.put_EncodingMode("hex")

strData = "ANURAG"

# Sign the SHA256 hash of the string.
hexSig = rsa.signStringENC(strData,"sha256")

print(hexSig)
print(rsa.lastErrorText())

# Now verify the signature:
success = rsa.VerifyStringENC(strData,"sha256",hexSig)
if (success == True):
    print("Signature verified!")
else:
    print(rsa.lastErrorText())

# Try it with an invalid signature:
success = rsa.VerifyStringENC(strData,"sha256","not a valid sig")
if (success == True):
    print("Signature verified!")
else:
    print(rsa.lastErrorText())

# Try it with invalid data:
success = rsa.VerifyStringENC("Not the original data","sha256",hexSig)
if (success == True):
    print("Signature verified!")
else:
    print(rsa.lastErrorText())

# Try it with the wrong hash algorithm:
success = rsa.VerifyStringENC(strData,"sha-1",hexSig)
if (success == True):
    print("Signature verified!")
else:
    print(rsa.lastErrorText())