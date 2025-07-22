from src.main import baldw64

passwd = 'password'
email = 'testuser@gmail.com'

reg_data = baldw64(message=passwd.encode(), token=email)

message = input("Enter your passwd: ")
verf_str = input("Enter your email for verification: ")
hashed_message = baldw64(message=message.encode(), token=verf_str)

hash_size = reg_data[:4]
size = int(hash_size, 16)

if hashed_message[4:size // 8] == reg_data[4:size // 8]:
    print("Welcome, user!")
    print(reg_data)
    print(hashed_message)
else:
    print("Incorrect data!")
