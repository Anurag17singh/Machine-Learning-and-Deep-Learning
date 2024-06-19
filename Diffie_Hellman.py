import sys
import chilkat

# This example requires the Chilkat API to have been previously unlocked.
# See Global Unlock Sample for sample code.

# Create two separate instances of the DH object.
dhBob = chilkat.CkDh()
dhAlice = chilkat.CkDh()

# The DH algorithm begins with a large prime, P, and a generator, G.  
# These don't have to be secret, and they may be transmitted over an insecure channel.  
# The generator is a small integer and typically has the value 2 or 5.

# The Chilkat DH component provides the ability to use known
# "safe" primes, as well as a method to generate new safe primes.

# This example will use a known safe prime.  Generating
# new safe primes is a time-consuming CPU intensive task
# and is normally done offline.

# Bob will choose to use the 2nd of our 8 pre-chosen safe primes.  
# It is the Prime for the 2nd Oakley Group (RFC 2409) -- 
# 1024-bit MODP Group.  Generator is 2. 
# The prime is: 2^1024 - 2^960 - 1 + 2^64 * { [2^894 pi] + 129093 }
dhBob.UseKnownPrime(2)

# The computed shared secret will be equal to the size of the prime (in bits).
# In this case the prime is 1024 bits, so the shared secret will be 128 bytes (128 * 8 = 1024).
# However, the result is returned as an SSH1-encoded bignum in hex string format.
# The SSH1-encoding prepends a 2-byte count, so the result is going  to be 2 bytes
# longer: 130 bytes.  This results in a hex string that is 260 characters long (two chars
# per byte for the hex encoding).

# Bob will now send P and G to Alice.
p = dhBob.p()
g = dhBob.get_G()

# Alice calls SetPG to set P and G.  SetPG checks
# the values to make sure it's a safe prime and will
# return False if not.
success = dhAlice.SetPG(p,g)
if (success != True):
    print("P is not a safe prime")
    sys.exit()

# Each side begins by generating an "E"
# value.  The CreateE method has one argument: numBits.
# It should be set to twice the size of the number of bits
# in the session key.

# Let's say we want to generate a 128-bit session key
# for AES encryption.  The shared secret generated by the Diffie-Hellman
# algorithm will be longer, so we'll hash the result to arrive at the
# desired session key length.  However, the length of the session
# key we'll utlimately produce determines the value that should be
# passed to the CreateE method.

# In this case, we'll be creating a 128-bit session key, so pass 256 to CreateE.
# This setting is for security purposes only -- the value
# passed to CreateE does not change the length of the shared secret
# that is produced by Diffie-Hellman.  
# Also, there is no need to pass in a value larger
# than 2 times the expected session key length.  It suffices to
# pass exactly 2 times the session key length.

# Bob generates a random E (which has the mathematical
# properties required for DH).

eBob = dhBob.createE(256)

# Alice does the same:

eAlice = dhAlice.createE(256)

# The "E" values are sent over the insecure channel.
# Bob sends his "E" to Alice, and Alice sends her "E" to Bob.

# Each side computes the shared secret by calling FindK.
# "K" is the shared-secret.

# Bob computes the shared secret from Alice's "E":
kBob = dhBob.findK(eAlice)

# Alice computes the shared secret from Bob's "E":
kAlice = dhAlice.findK(eBob)

# Amazingly, kBob and kAlice are identical and the expected
# length (260 characters).  The strings contain the hex encoded bytes of
# our shared secret:
print("Bob's shared secret:")
print(kBob)
print("Alice's shared secret (should be equal to Bob's)")
print(kAlice)

# To arrive at a 128-bit session key for AES encryption, Bob and Alice should
# both transform the raw shared secret using a hash algorithm that produces
# the size of session key desired.   MD5 produces a 16-byte (128-bit) result, so
# this is a good choice for 128-bit AES.

# To produce the session key:
crypt = chilkat.CkCrypt2()

crypt.put_EncodingMode("hex")
crypt.put_HashAlgorithm("md5")

sessionKey = crypt.hashStringENC(kBob)

print("128-bit Session Key:")
print(sessionKey)

# Encrypt something...
crypt.put_CryptAlgorithm("aes")
crypt.put_KeyLength(128)
crypt.put_CipherMode("cbc")

# Use an IV that is the MD5 hash of the session key...

iv = crypt.hashStringENC(sessionKey)

# AES uses a 16-byte IV:
print("Initialization Vector:")
print(iv)

crypt.SetEncodedKey(sessionKey,"hex")
crypt.SetEncodedIV(iv,"hex")

# Encrypt some text:

crypt.put_EncodingMode("base64")
cipherText64 = crypt.encryptStringENC("The quick brown fox jumps over the lazy dog")
print(cipherText64)

plainText = crypt.decryptStringENC(cipherText64)

print(plainText)
