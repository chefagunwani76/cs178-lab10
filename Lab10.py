import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Songs')

def create_song():
    user_input = input("Enter a song title: ")

    response = table.get_item(Key = {"Title":user_input})
    item = response.get("Item")

    if item:
        print("Song already exists in this database")

    else:
        new_movie = {
            "Title"   : user_input,
            "Artists" : []
        }
        table.put_item(Item=new_movie)
        print("creating a movie")
    

def print_song(song):
    """Print a single song's details in a readable format."""
    title = song.get("Title", "Unknown Title")
    artist = song.get("Artist", "Unknown Artist")
    year = song.get("Release Year", "Unknown Release Year")
    genre = song.get("Genre", "Unknown Genre")
    #rating_str = ", ".join(f"{k}: {v}" for k, v in ratings.items()) if ratings else "No ratings"
    
    print(f"  Title : {title}")
    print(f"  Artist: {artist}")
    print(f"  Release Year  : {year}")
    print(f"  Genre: {genre}")
    print()



def print_all_songs():
    """Scan the entire Songs table and print each item."""
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No songs found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} song(s):\n")
    for song in items:
        print_song(song)

class TitleNotFound(Exception):
    pass
class EmptyList(Exception):
    pass

def update_artist(): #incorrect artist or add more artists on a title
    try:
        title = input("What is the song you would like to update? ")
        response = table.get_item(Key={"Title": title})
        if "Item" not in response:
            raise TitleNotFound("Song title was not found in database.")

        update_kind = input("Would you like to ADD an artist or REPLACE current artist?: ")
        if update_kind.upper() == 'ADD':
            artist = input("Enter the artist would you like to add: ")
            table.update_item(
                Key={"Title": title},
                UpdateExpression="SET Artist = list_append(Artist, :a)",
                ExpressionAttributeValues={':a': [artist]})

        if update_kind.upper() == 'REPLACE':
            artist = input("Enter the correct artist to replace the current one: ")
            table.update_item(
                Key={"Title": title},
                UpdateExpression="SET Artist = :a",
                ExpressionAttributeValues={':a': [artist]})

    except TitleNotFound as e:
        print("Custom error:", e)
    else:
        print("updating artist(s)...")

def delete_song():
    try:
        title = input("What is the song you would like to delete? ")
        response = table.get_item(Key={"Title":title})
        if "Item" not in response:
            raise TitleNotFound("Song title was not found in database.")
        table.delete_item(
            Key={'Title': title,})
    except TitleNotFound as e:
        print("Custom error:", e)
    else: 
        print("deleting song...")

def query_song(): #which song was released first
    try:
        title1 = input("What is the first song you would like to query? ")
        title2 = input("What is the second song you would like to query? ")

        response1 = table.get_item(Key={'Title': title1})
        if "Item" not in response1:
            raise TitleNotFound("Song title 1 was not found in database.")
        song1 = response1["Item"]
        response2 = table.get_item(Key={'Title': title2})
        if "Item" not in response2:
            raise TitleNotFound("Song title 2 was not found in database.")
        song2 = response2["Item"]

        song1_year = int(song1["Release Year"])
        song2_year = int(song2["Release Year"])

        if not song1 or not song2:
            raise EmptyList("There are not enough years to compare.")
        if song1_year>song2_year:
            older_song = song2
            older_title = title2
            older_year = song2_year
        else:
            older_song=song1
            older_title=title1
            older_year=song1_year

    except TitleNotFound as e: 
        print("Custom error:", e)
    except EmptyList as x:
        print("Custom error:", x)

    else:
        print("query-ing songs...")
        print(f"\nBetween {title1} and {title2}, the song with the earlier release date is {older_title} released in {older_year}")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (correct artist or add co-artists)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_all_songs()
        elif input_char.upper() == "U":
            update_artist()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_song()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
