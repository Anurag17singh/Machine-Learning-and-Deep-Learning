import sys
import chilkat

# This example assumes the Chilkat API to have been previously unlocked.
# See Global Unlock Sample for sample code.

privKeyHex = "1498b5467a63dffa2dc9d9e069caf075d16fc33fdd4c3b01bfadae6433767d93"
pubKeyHex = "b7a3c12dc0c8c748ab07525b701122b88bd78f600c76342d27f25e5f92444cde"

privKey = chilkat.CkPrivateKey()
# This example shows only one way of loading an Ed25519 private key.
# Chilkat can load other formats (JWK, PEM, ASN.1 DER, etc.)  
# You may do so by calling LoadAnyFormat or LoadAnyFormatFile.
success = privKey.LoadEd25519(privKeyHex,pubKeyHex)
if (success == False):
    print(privKey.lastErrorText())
    sys.exit()

# The data to be signed...
bd = chilkat.CkBinData()
bd.AppendString("Message for Ed25519 signing","utf-8")

eddsa = chilkat.CkEdDSA()
hexSig = eddsa.signBdENC(bd,"hexlower",privKey)

print("signature = " + hexSig)

# The expected output is: 6dd355667fae4eb43c6e0ab92e870edb2de0a88cae12dbd8591507f584fe4912babff497f1b8edf9567d2483d54ddc6459bea7855281b7a246a609e3001a4e08

# Verify the signature..
pubKey = chilkat.CkPublicKey()
success = pubKey.LoadEd25519(pubKeyHex)
if (success == False):
    print(pubKey.lastErrorText())
    sys.exit()

bVerified = eddsa.VerifyBdENC(bd,hexSig,"hexlower",pubKey)
if (bVerified == False):
    print(eddsa.lastErrorText())
    print("Failed to verify the signature.")
    sys.exit()

print("The Ed25519 signature is verified!")
