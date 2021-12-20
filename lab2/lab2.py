class DH_Endpoint():
	def __init__(self, public_key1, public_key2, private_key):
		self.public_key1 = public_key1
		self.public_key2 = public_key2
		self.private_key = private_key
		self.full_key = None
		
	def generate_partial_key(self):
		partial_key = self.public_key1 ** self.private_key
		partial_key = partial_key % self.public_key2
		return partial_key

	def generate_full_key(self, partial_key_r):
		full_key = partial_key_r ** self.private_key
		full_key = full_key % self.public_key2
		self.full_key = full_key
		return full_key

	def encrypt_message(self, message):
		encrypted_message = ""
		key = self.full_key

		for c in message:
			encrypted_message += chr(ord(c) + key)
		return encrypted_message

	def decrypt_message(self, encrypted_message):
		decrypted_message = ""
		key = self.full_key
		for c in encrypted_message:
			decrypted_message += chr(ord(c) - key)
		return decrypted_message

first_public = 210
first_private = 352
second_public = 122
second_private = 314
# third_public = 135
# third_private = 321
sample_message = "Sample encrypted message"

Alice = DH_Endpoint(first_public, second_public, first_private)
Bob = DH_Endpoint(first_public, second_public, second_private)
# Eve = DH_Endpoint(first_public, third_public, third_private)

Alice.generate_full_key(Bob.generate_partial_key())
Bob.generate_full_key(Alice.generate_partial_key())

message_from_alice = Alice.encrypt_message(sample_message)
print(message_from_alice)
decrypted_message = Bob.decrypt_message(message_from_alice)
print(decrypted_message)
