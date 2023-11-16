#Email Slicer Program

#Fetches users email address
email = input("What is your email address?: ").strip()
#Slices out username
user_name = email[:email.index("@")]
#Slices out domain name
domain_name = email[email.index("@")+1:]
#Format Message
output = "Your username is '{}' and your domain name is '{}'".format(user_name,domain_name)
#Prints output to display
print(output)