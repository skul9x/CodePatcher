package utils

import (
	"crypto/sha256"
	"encoding/base64"
)

// TokenCipher implements exact parity with the Python TokenCipher.
// It uses XOR with a SHA256 hashed salt and base64 encoding.
type TokenCipher struct{}

var salt = []byte("TCO_PatchApplier_Secure_Salt_v3.1")

func (t *TokenCipher) getKey() []byte {
	hash := sha256.Sum256(salt)
	return hash[:]
}

// Encrypt encrypts a raw string using XOR with the hashed salt.
func (t *TokenCipher) Encrypt(rawText string) string {
	if rawText == "" {
		return ""
	}
	key := t.getKey()
	enc := make([]byte, len(rawText))
	rawBytes := []byte(rawText)
	for i := 0; i < len(rawBytes); i++ {
		enc[i] = rawBytes[i] ^ key[i%len(key)]
	}
	return base64.StdEncoding.EncodeToString(enc)
}

// Decrypt decrypts a base64 encoded string using XOR with the hashed salt.
func (t *TokenCipher) Decrypt(encText string) string {
	if encText == "" {
		return ""
	}
	encBytes, err := base64.StdEncoding.DecodeString(encText)
	if err != nil {
		return ""
	}
	key := t.getKey()
	dec := make([]byte, len(encBytes))
	for i := 0; i < len(encBytes); i++ {
		dec[i] = encBytes[i] ^ key[i%len(key)]
	}
	return string(dec)
}
