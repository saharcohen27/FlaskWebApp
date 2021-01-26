from DataBase import Database
Database().ask("DELETE FROM Streamers WHERE Username != 'a'")
Database().ask("DELETE FROM Passcodes WHERE Username != 'a'")
Database().ask("DELETE FROM Users WHERE Username != 'a'")
Database().ask("DELETE FROM SessionsAndCookies WHERE Username != 'a'")

# _id = "9"
# sql = f"SELECT * FROM SessionsAndCookies WHERE CookieID = '{_id}';"
# data = Database().ask(sql)
# print(data)

# email = "saharcohen456@gmail.com"
# print(Database().ask(f"SELECT Username From Users WHERE EmailAddress='{email}' AND googleUser IS NOT NULL;")[0][0])
# _id = "5f9a1211-05e5-439d-a6d6-c90e78768f5"
# print(Database().ask(f"SELECT Username FROM SessionsAndCookies WHERE SessionID = '{_id}' OR CookieID = '{_id}';")[0])
